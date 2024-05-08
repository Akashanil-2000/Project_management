"""
URL configuration for TodoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from backend import views
from backend.views import GenerateSummaryView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.project_list, name='project_list'),
    path('project/create/', views.create_project, name='create_project'),
    path("logout/", views.LogoutPage, name="logout"),
    path('projects/<int:project_id>/', views.project_todos, name='project_todos'),
    path('project/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('todos/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('todos/create/', views.create_todo, name='create_todo'),
    path('todos/update/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('generate-summary/', GenerateSummaryView.as_view(), name='generate_summary'),
]
