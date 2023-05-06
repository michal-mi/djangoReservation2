from django.shortcuts import redirect, render
from django.contrib.auth import get_user
from django.contrib.auth.models import User, Reservation, Classes
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from web_app import settings
import re


def beginNewSemester(request):
    if request.method == "POST":
        password = request.POST.get('password')

        user = get_user(request)

        if check_password(password, user.password):
            superuser = User.objects.get(is_superuser=1)

            for user in User.objects.exclude(id=superuser.id):
                subject = "System rezerwacji - usunięcie konta"
                link = render_to_string('account_deleted.html',{
                    'name': user.first_name,
                    'lecturer': superuser.first_name + " " + superuser.last_name
                })
                email = EmailMessage(
                    subject,
                    link,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                email.fail_silently = True
                email.send()

            User.objects.exclude(id=superuser.id).delete()
            Reservation.objects.all().delete
            Classes.objects.all().delete()
            messages.success(request, "Nowy semestr został rozpoczęty!")
            return redirect('home')
        else:
            messages.error(request, "Nieprawidłowe hasło!")
            return render(request, 'reservation_system/beginNewSemester.html', {'password': password})
    
    return render(request, 'reservation_system/beginNewSemester.html')