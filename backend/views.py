from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Project, Todo
from django.shortcuts import render, redirect
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required

# Create your views here.
def is_admin(user):
    return user.is_superuser


admin_required = user_passes_test(lambda user: user.is_superuser)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'todoApp/register.html', {'form': form})

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:  # If the user is an admin
                return redirect('project_list')
            else:  # If the user is a normal user
                return redirect('user_todo_list')
    else:
        form = LoginForm()
    return render(request, 'todoApp/login.html', {'form': form})

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

@login_required
@admin_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'todoApp/project_list.html', {'projects': projects})


@login_required
@admin_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        if start_date:  # Check if start_date is provided
            created_date = datetime.strptime(start_date, '%Y-%m-%d')  # Assuming date format is YYYY-MM-DD
        else:
            created_date = datetime.now()  # Set default created_date to current date
        Project.objects.create(name=name, created_date=created_date)
        return redirect('project_list')
    return render(request, 'todoApp/create_project.html')


def LogoutPage(request):
    logout(request)
    return redirect("login")

@login_required
@admin_required
def project_todos(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    todos = project.todo_set.all()
    return render(request, 'task_management_system_app/category_tasks.html', {'project': project, 'todos': todos})

@login_required
@admin_required
def delete_todo(request, todo_id):
    if request.method == 'POST':
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
    return redirect(reverse('project_list'))

@login_required
@admin_required
def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    if project.task_set.exists():
        messages.error(
            request, "You cannot delete this project as it contains tasks.")
    else:
        project.delete()
        messages.success(request, "Project deleted successfully.")
    return redirect('project_list')