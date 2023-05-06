from django.db import models
from django.contrib.auth.models import User

class Classes(models.Model):
    beginning_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    slots = models.IntegerField()
    available_slots = models.IntegerField()
    classroom = models.CharField(max_length=30, null=True, blank=True)
    building = models.CharField(max_length=60, null=True, blank=True)
    online = models.BooleanField()
    note = models.CharField(max_length=255, null=True, blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Classes'


# W pliku models.py w aplikacji reservation
from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, null=True, blank=True)
    friendly_number = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'Reservation'