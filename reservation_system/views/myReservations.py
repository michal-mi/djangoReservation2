from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Classes, Reservation
from django.db import connection
from datetime import datetime
from web_app import settings
import json

def myReservations(request):
    user = get_user(request)
    with connection.cursor() as cursor:
        cursor.execute('SELECT friendly_number, classes.beginning_time, reservation.beggining_time, reservation.ending_time, reservation.note, classes.online, classroom, building, reservation.id, classes.id, classes.beginning_time FROM reservation INNER JOIN classes ON reservation.classes_id = classes.id WHERE reservation.student_id = (%s)', [user.id])
        rows = cursor.fetchall()
        reservations = []
        for row in rows:
            reservation = {
                'friendly_number': row[0],
                'date': row[1],
                'beggining_time': row[2],
                'ending_time': row[3],
                'note': row[4],
                'online': row[5],
                'classroom': row[6],
                'building': row[7],
                'id': row[8],
                'classes_id': row[9],
                'classes_beg': row[10]
            }
            reservations.append(reservation)

    if request.method == "POST":
        print("FFSDFSDF")
        id = request.POST['id']
        beg_time = request.POST['begTime']
        classes_id = request.POST['classesId']

        thisReservation = Reservation.objects.get(id=id)
        connectedClasses = Classes.objects.get(id=classes_id)

        connectedClasses.available_slots = connectedClasses.available_slots + 1
        slots_info = connectedClasses.slots_info
        slots_info = json.loads(slots_info)
        beg_timedate = connectedClasses.beginning_time

        year = beg_timedate.year
        month = beg_timedate.month
        day = beg_timedate.day
        hour = int(beg_time[:2])
        minutes = int(beg_time[-2:])
        seconds = 0

        searchDatetime = datetime(year, month, day, hour, minutes, seconds)

        for key, value in slots_info.items():
            if str(value["beginning_time"]) == str(searchDatetime):
                value["available"] = 1
                print(f"Zmieniono status dostępności dla obiektu {key}")

        slots_updated = json.dumps(slots_info)

        connectedClasses.slots_info = slots_updated
        connectedClasses.save()

        subject = "System rezerwacji - anulowanie rezerwacji " + thisReservation.friendly_number
        link = render_to_string('reservation_cancelation.html',{
            'fname': user.first_name,
            'friendly_number': thisReservation.friendly_number,
            'classes_beg': connectedClasses.beginning_time,
            'classes_end': connectedClasses.ending_time,
            'slot_beg': thisReservation.beggining_time,
            'slot_end': thisReservation.ending_time,
            'note': thisReservation.note
        })
        email = EmailMessage(
            subject,
            link,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = True
        email.send()

        thisReservation.delete()

        messages.success(request, "Rezerwację anulowano poprawnie!")
    
    return render(request, 'reservation_system/myReservations.html', {'reservations': reservations})