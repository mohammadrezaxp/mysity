from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def loge_page(request) :
    if request.user.is_authenticated :
        return redirect('/ref/home/')
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)
        if user is not  None :
            login(request,user)
            if not remember :
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {user.username}!')
            print(f'✅ Login successful - User:{user.username}')
            next_url = request.GET.get('next', '/ref/home/')
            return redirect(next_url)
        else:
            print(f"❌ Login failed - Invalid credentials for username: {username}")
            messages.error(request,'Invalid username or password')

    return render(request ,'User_mage/login_user.html')

def logout_page (request):
    logout(request)
    messages.info(request,'you are logout as website')
    return redirect('/ref/user_mange/login')



def sing_up_page(request):
    if request.user.is_authenticated:
        return redirect('/ref/home/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        print(f"🔍 Register attempt - Username: {username}, Email: {email}")

        # بررسی فیلدهای ضروری
        if not username or not email or not password or not password_confirm:
            messages.error(request,'All fields are required.')
            return render(request,'User_mage/index.html')

        if password != password_confirm:
            messages.error(request,'Passwords do not match')
            return render(request,'User_mage/index.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'User_mage/index.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'User_mage/index.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'User_mage/index.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print(f"✅ User created: {username}")

            login(request, user)
            messages.success(request,f'Welcome {username}! Your account has been created successfully.')
            return redirect('/ref/home/')
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'User_mage/index.html')

    return render(request ,'User_mage/index.html')