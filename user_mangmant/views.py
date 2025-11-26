from django.contrib.auth import authenticate, login, logout
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



def regster_page (request):
    return render(request ,'User_mage/regster_user.html')