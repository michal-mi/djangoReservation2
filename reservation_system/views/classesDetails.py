from django.shortcuts import render
from django.contrib.auth.models import User, Classes
from django.contrib.auth import get_user
from django.db import connection


def classesDetails(request, pk):
    with connection.cursor() as cursor:
        classes = Classes.objects.get(id=pk)
        cursor.execute('SELECT friendly_number, first_name, last_name, beggining_time, ending_time, note FROM Reservation INNER JOIN auth_user ON Reservation.student_id = auth_user.id WHERE classes_id = (%s)', [pk])
        rows = cursor.fetchall()
        reservations = []
        for row in rows:
            reservation = {
                'friendly_number': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'beginning_time': row[3],
                'ending_time': row[4],
                'note': row[5]
            }
            reservations.append(reservation)
    return render(request, 'reservation_system/classesDetails.html', {'reservations': reservations, 'classes': classes})