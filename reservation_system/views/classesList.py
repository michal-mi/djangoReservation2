from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, Classes
from django.contrib.auth import get_user

def classesList(request):
    classes = Classes.objects.all().order_by('beginning_time')
    return render(request, 'reservation_system/classesList.html', {'classes': classes})