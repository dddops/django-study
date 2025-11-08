"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import login
from totododo import views as totododoviews
from login import views


urlpatterns = [
    path('todo/create', totododoviews.todo_create, name='todo_create'),
    path('todo/update/<int:pk>', totododoviews.todo_update, name='todo_update'),
    path('todo/delete/<int:pk>', totododoviews.todo_delete, name='todo_delete'),
    path('todo/<int:pk>', totododoviews.todo_info, name='todo_info'),
    path('admin/', admin.site.urls),
    path('', totododoviews.todo_list, name='todo_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', login.views.sign_up, name='signup'),
    path('login/', login.views.login, name='login'),
]
