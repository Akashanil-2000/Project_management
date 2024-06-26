from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import View
import requests
from datetime import datetime
from .models import Project, Todo

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
    return render(request, 'todoApp/project_todos.html', {'project': project, 'todos': todos})

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
    if project.todo_set.exists():
        messages.error(
            request, "You cannot delete this project as it contains tasks.")
    else:
        project.delete()
        messages.success(request, "Project deleted successfully.")
    return redirect('project_list')


@login_required
@admin_required
def create_todo(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        project_id = request.POST.get('project')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        project = Project.objects.get(pk=project_id)
        todo = Todo.objects.create(
            name=name,
            project=project,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )

        # Redirect to the task list page
        return redirect('project_list')
    else:
        projects = Project.objects.all()
        users = User.objects.all()
        return render(request, 'todoApp/create_todo.html', {'projects': projects, 'users': users})

@login_required
@admin_required
def update_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if request.method == 'POST':
        # Update task fields based on form data
        todo.name = request.POST.get('name')
        todo.start_date = request.POST.get('start_date')
        todo.end_date = request.POST.get('end_date')
        todo.description = request.POST.get('description')
        todo.save()
        return redirect('project_list')
    else:
        # Render update task page with task data
        return render(request, 'todoApp/update_todo.html', {'todo': todo})
    

@login_required
@admin_required
def update_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if request.method == 'POST':
        # Update task fields based on form data
        todo.name = request.POST.get('name')
        todo.start_date = request.POST.get('start_date')
        todo.end_date = request.POST.get('end_date')
        todo.description = request.POST.get('description')
        todo.save()
        return redirect('project_list')
    else:
        # Render update task page with task data
        return render(request, 'todoApp/update_todo.html', {'todo': todo})
    
@login_required
@admin_required
def toggle_todo_completion(request, todo_id):
    if request.method == 'POST':
        todo = Todo.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
    return redirect('project_todos', project_id=todo.project.id)

    
import requests
from django.http import HttpResponse
from django.views import View


def generate_summary():
    summary = ''
    projects = Project.objects.all()

    for project in projects:
        summary += f'# {project.name}\n\n'
        todos = Todo.objects.filter(project=project)
        completed_todos = todos.filter(completed=True)
        pending_todos = todos.filter(completed=False)
        total_todos = todos.count()
        completed_count = completed_todos.count()

        summary += f'Summary: {completed_count} / {total_todos} completed.\n\n'

        summary += '## Pending Todos\n\n'
        for todo in pending_todos:
            summary += f'- [ ] **{todo.name}** - Description: {todo.description}, End date: {todo.end_date}\n\n'

        summary += '## Completed Todos\n\n'
        for todo in completed_todos:
            summary += f'- [x] **{todo.name}** - Description: {todo.description}, End date: {todo.end_date}\n\n'

    return summary


def create_gist(summary):
    # Replace with your GitHub token
    token = ''
    headers = {'Authorization': f'token {token}', 'accept': 'application/vnd.github+json'}
    data = {
        'description': 'Project Summary',
        'files': {
            'summary.md': {
                'content': summary
            }
        }
    }
    response = requests.post('https://api.github.com/gists', headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        return None

class GenerateSummaryView(View):
    def get(self, request, *args, **kwargs):
        # Generate summary
        summary = generate_summary()  # Call generate_summary without any arguments
        # Create gist
        gist_url = create_gist(summary)
        if gist_url:
            return HttpResponse(f'Successfully created gist: {gist_url}')
        else:
            return HttpResponse('Failed to create gist', status=500)



