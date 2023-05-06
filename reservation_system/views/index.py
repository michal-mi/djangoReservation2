from django.shortcuts import render
from django.contrib.auth.models import Classes

def home(request):
    classes = Classes.objects.all()
    # for c in classes:
    #     print(c.id, c.beginning_time, c.ending_time)
    return render(request, 'reservation_system/index.html')