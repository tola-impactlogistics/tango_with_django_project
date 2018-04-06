# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Page, UserProfile
from .forms import CategoryForm, UserForm, UserProfileForm, EditUserForm, EditUserProfileForm
from .forms import PageForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.bing_search import run_query
#from .processText import searchInPDF
# Create your views here.

def about(request):

    return render(request, 'rango/about.html', {})

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    userslist = User.objects.all()[:10]

    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5]

       

    context_dict = {'categories': category_list, 'pages': page_list, 'userslist': userslist, }
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
# 	        if (datetime.now() - last_visit_time).days > 0: The sample code only increments the counter at least one whole day after a user revisits the Rango homepage 
# 	        if (datetime.now() - last_visit_time).seconds > 5: Here you can only wait for five secongs to see your visits cookie increment

            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    # User submit a search begins
 
#    context_dict['pages'] = pages
    
    # User submit a search ENDS

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict = {'category_name': category.name, 'category_name_url': category_name_slug}

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        
        #pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    context_dict['result_list'] = None
    context_dict['query'] = None

    if request.method == 'POST':
        query = request.POST.get('query', 'No Value').strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    if not context_dict['query']:
        context_dict['query'] = category.name
    # Go render the response and return it to the client.

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

from rango.forms import PageForm

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat,}

    return render(request, 'rango/add_page.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()


            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                #request.session["_auth_user_id"] = user.id   #------ADD BY TOLA

                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):

    context_dict = {"echo": "Since you're logged in, you can see this text!"}
    
    return render(request, 'rango/restricted.html', context_dict)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

@login_required
def profile(request):
    if request.session.has_key("_auth_user_id"):
        _auth_user_id = request.session["_auth_user_id"]
        UserDetails = User.objects.get(id =_auth_user_id)
        ProfileDetails = UserProfile.objects.get(user_id=UserDetails.id)
        
        
        
#    updated = False
#    if request.method == 'POST':
#        user_form = UserForm(request.POST, instance=UserDetails)
#        profile_form = UserProfileForm(request.POST, request.FILES, instance = ProfileDetails)

#        if user_form.is_valid() and profile_form.is_valid():
#            user =user_form.save()
 #           profile = profile_form.save(commit=False)
 #           profile.user = user
        #if 'picture' in request.FILES:
        #    profile.picture = request.FILES['picture']

        # Now we save the UserProfile model instance.
  #          profile.save()
  #          updated = True
            #return HttpResponseRedirect('/rango/')

#        else:
#            print user_form.errors, profile_form.errors

        #userDetails.username = request.POST['user.username']
        #userDetails.email = request.POST['user.email']
        #userDetails.save()
        #return HttpResponseRedirect('/index/')
    
    return render(request, "profile.html", {'user':UserDetails, 'profile': ProfileDetails, }) #'user_form': user_form, 'profile_form': profile_form, 	


#@login_required
#def edit_profile(request):
#    if '_auth_user_id' in request.session:
#        userId = request.session['_auth_user_id']
#        new_profile_user = UserProfile.objects.get(user_id=userId)
#        userDetails = User.objects.get(pk=userId)
#        if request.method == 'POST':
#            userDetails.firstname = request.POST['firstname']
#            userDetails.email = request.POST['email']
#            userDetails.save()
#        template_var= { 'new_profile_user': new_profile_user }
#    return render( request, 'edit_user.html', template_var)

#def edit_profile(request):

#	if request.method == 'POST':
#	    form = ProfileForm(data=request.POST, instance=request.user)
#	    if form.is_valid():
#	        user_profile = form.save(commit=False)
#	        user_profile.save()
#	        return redirect('index')
#	    else:
#	        form = ProfileForm(instance=request.user)
#	    return render(request, template_name,{'form': form})

@login_required
def profile_edit(request): 
    if request.session.has_key("_auth_user_id"):
        _auth_user_id = request.session["_auth_user_id"]
        userinstance = get_object_or_404(User, pk=_auth_user_id)
        profileinstance = get_object_or_404(UserProfile, user_id=userinstance.id)
        user_form = EditUserForm(request.POST or None, instance=userinstance)
        profile_form = EditUserProfileForm(request.POST or None, request.FILES or None, instance=profileinstance)
        updated = False
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            user =user_form.save()            
            profile.user = user
            #if 'picture' in request.FILES:
             #   profile.picture = request.FILES['picture']

        # Now we save the UserProfile model instance.
            profile = profile.save()
            updated = True  
            return redirect('profile')
  	return render(request, 'rango/profile_edit.html', {'userform': user_form, 'profileform': profile_form, 'user':userinstance, 'profile': userinstance })


@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
                cat_list = Category.objects.filter(name__istartswith=starts_with)

        if cat_list and max_results > 0:
                if cat_list.count() > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list

def suggest_category(request):

    cat_list = []
    starts_with = ''
    if request.method == 'GET':
            starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cat_list': cat_list })



