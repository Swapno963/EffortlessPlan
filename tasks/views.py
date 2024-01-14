from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Tasks
from .forms import Task_form
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
    
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class Show_all_task(ListView):
    template_name = 'show_task.html'
    model = Tasks
    form_class = Task_form

    # for filtering
    def get_queryset(self):
        priject_slug = self.kwargs.get('project')
        # print(priject_slug)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    
    def post(self, request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            print(form.cleaned_data)
            task = form.save(commit=False)
            return redirect('show_all_task')
        else:
            return self.get(request,*args, **kwargs)


# send user name 
def priority_filter(request, priority=None):
    form = Task_form()
    if priority is not None:
        data = Tasks.objects.filter(priority = priority)
        print( "slug",priority,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            print("from pri :", form.cleaned_data)

    data = Tasks.objects.all()
    print( "slug",priority,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data,'user':request.user})


def status_filter(request, current_status=None):
    form = Task_form()
    if current_status is not None:
        data = Tasks.objects.filter(current_status = current_status)
        print( "slug",current_status,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            print("from pri :", form.cleaned_data)

    data = Tasks.objects.all()
    print( "slug",current_status,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data})

def due_date_filter(request, due_date=None):
    form = Task_form()
    if due_date is not None:
        data = Tasks.objects.filter(due_date = due_date)
        print( "slug",due_date,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            print("from pri :", form.cleaned_data)

    data = Tasks.objects.all()
    print( "slug",due_date,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data})


def edit_task(request, id):
    post = Tasks.objects.get(pk=id) 
    data = Tasks.objects.all()

    task_form = Task_form(instance=post)
    if request.method == 'POST':
        task_form = Task_form(request.POST, instance=post)
        if task_form.is_valid(): 
            task_form.save()
    return render(request,'show_task.html',{'form':task_form,'object_list':data})


def delete_task(request, id):
    post = Tasks.objects.get(pk=id) 
    post.delete()
    # return redirect('homepage')


# register 
def task_maker_register(request):
    if request.method == 'POST':
        form =RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'authientication.html',{'form': form})

# login
def task_maker_login(request):
    if request.method =='POST':
        form =AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            name =form.cleaned_data['username']
            userpass =form.cleaned_data['password']
            user = authenticate(username=name, password=userpass)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'authientication.html', {'form': form})

# logout
def task_maker_logout(request):
    logout(request)
    return redirect('home')
