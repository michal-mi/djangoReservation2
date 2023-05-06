from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nieprawidłowe dane logowania!")
            return render(request, 'reservation_system/signin.html', {'username': username, 'password': password})

    return render(request, 'reservation_system/signin.html')
