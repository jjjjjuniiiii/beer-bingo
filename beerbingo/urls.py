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
]