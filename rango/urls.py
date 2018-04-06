from django.conf.urls import url
from django.views.generic import TemplateView, ListView
from . import views

#app_name = 'Rango' 
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # New!
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'), # NEW MAPPING!
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
#    url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='goto'),
#    url(r'^profile/$', TemplateView.as_view(template_name='profile.html')),
    url(r'^profile/$', views.profile, name='profile'),
    #url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),

]
