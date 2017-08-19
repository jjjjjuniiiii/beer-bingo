from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),

url(r'^index/$', views.index, name='index'),

url(r'^about/$', views.about, name='about'),
url(r'^beer-listing/$', views.beer_listing, name='beer_listing'),
url(r'^beer-details/$', views.beer_details, name='beer_details'),
url(r'^contact/$', views.contact, name='contact'),
url(r'^write/$', views.write, name='write'),
url(r'^login/$', views.login, name='login'),
#url(r'^post/new/$', views.post_new, name='post_new'),
#url(r'^$', views.post_list, name='post_list'),
#url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
url(r'^crawl/$', views.crawl_view, name='crawl'),
#url(r'^beer-details/$', views.find_beer, name='find_beer'),
url(r'^search/$', views.search_beer, name='search_beer'),
url(r'^path/$', views.photo_album),
url(r'^search-filtering/$', views.search_filtering, name='search_filtering'),
url(r'^contact/$', views.contact, name='contact'),
url(r'^auto/$', views.auto, name='auto'),
url(r'^regbeer/$', views.regbeer, name='regbeer'),
url(r'^auto_complete/$', views.auto_complete, name='auto_complete'),
url(r'^contact/thanks/$', views.contact_email, name='contact_email'),
#url(r'^profile/(?P<pk>d+)/$', views.profile, {}, name='item-profile'),
# url(r'^find_by_style/$', views.find_by_style, name='find_by_style'),
# url(r'^find_by_name/$', views.find_by_name, name='find_by_name'),
# url(r'^find_by_name/$', views.find_by_name, name='find_by_name'),
]