from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Tasks
# Create your views here.
class Show_all_task(ListView):
    template_name = 'show_task.html'
    model = Tasks
