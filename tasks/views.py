from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Tasks
from .forms import Task_form
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import AuthenticationForm


# eamil varification
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User



from rest_framework.permissions import IsAuthenticated, AllowAny  # NOQA
from rest_framework.decorators import api_view



from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from django_filters.rest_framework  import DjangoFilterBackend

class TasksViewset(viewsets.ModelViewSet):
    queryset = models.Tasks.objects.all()
    serializer_class = serializers.TasksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority','due_date','current_status']

# new


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode() 
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("http://127.0.0.1:5500/login.html")
        # return HttpResponse("Your account activated Now You can use ourwebsite!")
    else:
        return redirect("http://127.0.0.1:5500/register.html")
    
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    def get(self, request):
        # request.user.auth_token.delete()
        logout(request)
        return HttpResponse('logout')
    # new ended


# # register 
# def task_maker_register(request):
#     if request.method == 'POST':
#         form =RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.is_active = False
#             user.save()

#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
            
#             print("uid :", uid)
#             print("token :", token)
#             confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
#             email_subject = "Confirm Your Email"
#             email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
#             email = EmailMultiAlternatives(email_subject , '', to=[user.email])
#             email.attach_alternative(email_body, "text/html")
#             email.send()
#             return HttpResponse("Check your mail for confirmation")
#     else:
#         form = RegisterForm()
#     return render(request, 'authientication.html',{'form': form})

# # activate
# def activate(request, uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode() 
#         user =User._default_manager.get(pk=uid)
#     except(User.DoesNotExist):
#         user = None 
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active =True
#         user.save()
#         return redirect('task_maker_login')
#     else:
#         return redirect('task_maker_register')
    
# # login
# def task_maker_login(request):
#     if request.method =='POST':
#         form =AuthenticationForm(request=request,data=request.POST)
#         if form.is_valid():
#             name =form.cleaned_data['username']
#             userpass =form.cleaned_data['password']
#             user = authenticate(username=name, password=userpass)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  
#     else:
#         form = AuthenticationForm()
#     return render(request, 'authientication.html', {'form': form})

# # logout
# def task_maker_logout(request):
#     logout(request)
#     return redirect('home')
