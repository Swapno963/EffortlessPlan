from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Tasks
from .forms import Task_form
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
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
    return render(request,'show_task.html',{'form':form,'object_list':data})


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