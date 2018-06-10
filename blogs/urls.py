# @Time    : 18-6-5 下午2:19
# @Author  : zbc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from .views import index, base, list, show, Search

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^base/$', base, name='base'),
    url(r'^list/$', list, name='list'),
    url(r'^show/$',show, name='show'),
    url(r'^search/$', Search.as_view, name='search')
]
