# -*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from users.views import UserLoginView

admin.site.site_header = 'Task manager'
admin.site.index_title = 'Task manager'
admin.site.site_title = 'Task manager'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('', include('tasks.urls')),
]
