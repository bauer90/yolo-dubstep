__author__ = 'erhanhu'

from django.conf.urls import patterns, url
from yelp import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^search_zipcode/', views.search_zipcode, name='search_zipcode'),
                       url(r'^search_zipcode_reuslt/(?P<zipcode>[\w\-]+)/$', views.search_zipcode_result, name='search_zipcode_result'),

                       )