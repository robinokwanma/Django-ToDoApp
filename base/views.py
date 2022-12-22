from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.forms import TextInput
# Create your views here.
class TaskLogin(LoginView):
    fields= ['username', 'password']
    context_object_name= 'task'
    template_name= 'base/login.html'
    redirect_authenticated_user = True
    widgets = {
            'password' : TextInput(attrs={
                'class': "inputfield",
                'style': '',
                'placeholder': 'Password'
            })
        }
        
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class TaskRegister(FormView):
    template_name= 'base/register.html'
    form_class = UserCreationForm
    # redirect_authenticated_user = True
    success_url= reverse_lazy('tasks')
    
    def form_valid(self, form):
        user =  form.save()
        if user is not None:
            login(self.request, user)
        return super(TaskRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(TaskRegister, self).get(*args, **kwargs)
    
class TaskLogout(LogoutView):
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name= 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(name=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input']= search_input
        
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name= 'task'
    template_name= 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    context_object_name= 'taskform'
    template_name= 'base/form.html'
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')
    widgets = {
            'title' : TextInput(attrs={
                'class': "inputfield",
                'style': '',
                'placeholder': 'Your Task Title'
            })
        }
        
        
    
    def form_valid(self, form):
        form.instance.name = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields=  ['title', 'description', 'complete']
    template_name= 'base/task_edit.html'
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields= '__all__'
    context_object_name= 'task'
    template_name= 'base/confirm_delete.html'
    success_url= reverse_lazy('tasks')
    
