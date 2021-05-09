# -*- coding:utf-8 -*-

from django.contrib import admin
from django.urls import include, path
from users.views import UserLoginView, UserLogoutView

from .views import IndexView

admin.site.site_header = 'Task manager'
admin.site.index_title = 'Task manager'
admin.site.site_title = 'Task manager'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('', IndexView.as_view(), name='index'),
]
