from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import UserProfile
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        is_employee = request.POST.get('is_employee') == 'on'
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone)
        login(request, user)
        messages.success(request, 'You are now logged in')
        return redirect('job_list')
    return render(request, 'accounts/signup.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('job_list')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request, 'accounts/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')