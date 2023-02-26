from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
from django.contrib import auth
import json
# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request,'Templates/authentication/register.html')

    def post(self, request):
        #Get user data
        # Validtate
        #create a user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {'fieldVal': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Password must be at least 8 characters long')
                    return render(request,'Templates/authentication/register.html', context)

                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                if request.method == "POST": 
                    with get_connection(  
                        host=settings.EMAIL_HOST, 
                        port=settings.EMAIL_PORT,  
                        username=settings.EMAIL_HOST_USER, 
                        password=settings.EMAIL_HOST_PASSWORD, 
                        use_ssl=settings.EMAIL_USE_SSL  
                    ) as connection:  
                        # Path to the view
                        # getting the domain
                        # relative url to verification
                        # encode the UID
                        
                        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                        

                        domain = get_current_site(request).domain
                        link = reverse('activation', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                        activation_url = f'http://{domain}{link}'

                        email_subject = 'Activate your account'  
                        email_body = f"Hi {user.username},\n\nPlease click on the link to activate your account\n\n{activation_url}"  
                        email_from = 'noreply@signup.com'  
                        EmailMessage(email_subject, email_body, email_from, [email], connection=connection).send(fail_silently=False)  
                        messages.success(request, 'Account created successfully')
                        return render(request,'Templates/authentication/register.html',context)

        return render(request,'Templates/authentication/register.html', context)

class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + 'Message:'+ 'User already Activated')


            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated')
            return redirect('login')

        except:
            pass

        
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request,'Templates/authentication/login.html')


    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']


        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Logged in Successfully \n Welcome {user.username}")
                    return redirect('home')

                messages.error(request, f"Account not Active check your email")
                return render(request,'Templates/authentication/login.html')

            messages.error(request, f"Invalid credentials ")
            return render(request,'Templates/authentication/login.html')

        messages.error(request, f"Invalid credentials\n Please fill all fields")
        return render(request,'Templates/authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)

        messages.success(request, 'You have been logged out')
        return redirect('login')


class UserValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        # making the username Alphanumeric
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)

        #checking if user exists in the database
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_in_use': 'Username already exists'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        # Validating the email
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        #checking if user exists in the database
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_in_use': 'email already in use'}, status=409)

        return JsonResponse({'email_valid': True})