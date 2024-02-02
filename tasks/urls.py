from django.urls import path
from . import views
    # rest start
from rest_framework.routers import DefaultRouter
from django.urls import path, include
router = DefaultRouter() # amader router

router.register('', views.TasksViewset) 
# router.register('delete-post/<int:id>/', views.delete_task)  # NOQA
urlpatterns = [
    path('api/', include(router.urls)),
    # new
    path('register/', views.UserRegistrationApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view(), name='loginPage'),
    path('logout/', views.UserLogoutView.as_view()),
    path('active/<uid64>/<token>/', views.activate),
    # rest end
    # path('delete/<int:id>/',views.delete_task, name='delete_task') , 
    # path('',views.priority_filter, name='home') , 

    # path('task/<int:priority>/',views.priority_filter, name='priority_wise_filter') , 


    # path('status/<slug:current_status>/',views.status_filter, name='status_wise_filter') , 

    # path('due_date/<slug:due_date>/',views.due_date_filter, name='due_date_filter') , 

    # path('edit/<int:id>/',views.edit_task, name='edit_task') , 
    # # authientication
    # path('login',views.task_maker_login, name='task_maker_login') , 
    # path('register',views.task_maker_register, name='task_maker_register') , 

    # path('active/<uid64>/<token>/',views.activate, name='active') , 

    # path('logout',views.task_maker_logout, name='task_maker_logout') , 


   
]
