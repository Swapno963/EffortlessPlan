from django.urls import path
from . import views
urlpatterns = [
    path('',views.Show_all_task.as_view(), name='show_all_task')    
]
