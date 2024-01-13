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



