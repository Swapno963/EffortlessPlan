from django.urls import path
from . import views
urlpatterns = [
    path('',views.priority_filter, name='priority_wise_filter') , 

    path('task/<int:priority>/',views.priority_filter, name='priority_wise_filter') , 


    path('/status/<slug:current_status>/',views.status_filter, name='status_wise_filter') , 

    path('/due_date/<slug:due_date>/',views.due_date_filter, name='due_date_filter') , 

    path('/edit/<int:id>/',views.edit_task, name='edit_task') , 
    path('/delete/<int:id>/',views.delete_task, name='delete_task') , 


   
]
