from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import re

def myAccount(request):
    if request.method == "POST":
        password = request.POST.get('password')
        newPassword = request.POST.get('newPassword')
        user = get_user(request)
        newPasswordConfirm = request.POST.get('newPasswordConfirm')

        error = False

        if not any([
            re.search(r"[A-Z]", newPassword),
            re.search(r"[a-z]", newPassword),
            re.search(r"[0-9]", newPassword),
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", newPassword ),
            len(newPassword) >= 8
        ]):
            error = True
            messages.error(request, "Hasło nie spełnia wymagań")

        if newPassword != newPasswordConfirm:
            error = True
            messages.error(request, "Hasła są różne!")

        if not check_password(password, user.password):
            error = True
            messages.error(request, "Nieprawidłowe stare hasło!")
        
        if not error:
            userObject = User.objects.get(username = user)
            userObject.set_password(newPassword)
            userObject.save()
            messages.success(request, "Hasło zmieniono poprawnie! Zaloguj się ponownie")
            return redirect('home')
        
        if error:
            return render(request, 'reservation_system/myAccount.html', {'password': password, 'newPassword': newPassword, 'newPasswordConfirm': newPasswordConfirm})

    return render(request, 'reservation_system/myAccount.html')

