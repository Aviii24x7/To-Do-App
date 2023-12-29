from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Create your views here.
class CustomLoginView(LoginView):
    template_name = "ToDoApp/user_login.html"
    fields = "__all__"
    
    def get_success_url(self):
        return reverse_lazy("tasks-page")
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks-page')
        return super(CustomLoginView, self).get(*args, **kwargs)

class UserRegister(FormView):
    template_name =  "ToDoApp/user_register.html"
    form_class= UserCreationForm
    redirect_authenticate_user = True
    success_url = reverse_lazy('tasks-page')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks-page')
        return super(UserRegister, self).get(*args, **kwargs)
    
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "ToDoApp/task_list.html"
    context_object_name = "tasks"
    ordering = ['complete', '-created']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user= self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        
        searched = self.request.GET.get('searched') or ""
        if searched:
            context["tasks"] = context["tasks"].filter(title__icontains=searched)
        
        context['searched']= searched
       
        return context
    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model=Task
    context_object_name= "task"
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy("tasks-page")
    
    def form_valid(self, form):
        form.instance.user =  self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields = ['title','description','complete']
    success_url = reverse_lazy("tasks-page")
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model =  Task
    context_object_name= "task"
    success_url = reverse_lazy("tasks-page")
    # template_name= "task_deletion_confirm.html"
    
def complete_task(request, pk):
    task=Task.objects.get(id=pk)
    task.complete= not task.complete
    task.save()
    return redirect("tasks-page")
    
    