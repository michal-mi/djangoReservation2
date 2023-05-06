from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, Classes
from django.contrib.auth import get_user
from django.db import connection
from datetime import datetime, timedelta

def editClasses(request, pk):
    classes = Classes.objects.get(id=pk)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Reservation WHERE classes_id = (%s)', [pk])
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

    if request.method == "POST":
        if 'id' in request.POST :
            print("FFSDFSDF")
            id = request.POST['id']
            classesToDelete = Classes.objects.get(id=id)
            messages.success(request, "Zajęcia usunięto poprawnie!")
            classesToDelete.delete()

        else:
            beginningTime = request.POST['beginning_time']
            endingTime = request.POST['ending_time']
            slots = request.POST['slots']
            availableSlots = slots
            classroom = request.POST['classroom']
            building = request.POST['building']
            online = request.POST['online']
            note = request.POST['note']
            public = request.POST['public']

            error = False
            
            beginningTimeConv = datetime.strptime(beginningTime, '%Y-%m-%dT%H:%M')
            endingTimeConv = datetime.strptime(endingTime, '%Y-%m-%dT%H:%M')

            if beginningTimeConv >= endingTimeConv:
                error = True
                messages.error(request, "Data rozpoczęcia nie może być póżniejsza niż data zakończenia!")

            date = datetime.now()
            if beginningTimeConv < date:
                error = True
                messages.error(request, "Data rozpoczęcia nie może wcześniejsza niż bieżący czas!")

            if(public == 0):
                messages.warning(request, "Dopóki nie zmienisz statusu zajęć na publiczne nie będą one widoczne dla studentów!")

            if error:
                return render(request, 'reservation_system/editClasses.html', {'classes': classes, 'id': id, 'beginning_time': beginningTime, 'ending_time': endingTime, 'slots': slots, 'classroom': classroom, 'building': building, 'online': online, 'note': note, 'public': public})

            if not error:
                timeDiff = endingTimeConv - beginningTimeConv
                timeInMinutes = int(timeDiff.total_seconds() / 60)
                slotTime = timeInMinutes/int(availableSlots)

                slotsInfo = '{'
                availableSlotsConv = int(availableSlots)
                for i in range(availableSlotsConv):
                    intervalBegin = beginningTimeConv + i*timedelta(minutes=slotTime)
                    intervalEnd = beginningTimeConv + (i+1)*timedelta(minutes=slotTime)
                    slotsInfo += '"' + str(i) + '":{'
                    slotsInfo += '"available":1,'
                    slotsInfo += '"beginning_time":"' + str(intervalBegin) + '",'
                    slotsInfo += '"ending_time":"' + str(intervalEnd) + '"'
                    slotsInfo += '},'
                slotsInfo  = slotsInfo [:-1]
                slotsInfo += '}'

                classes.beginning_time = beginningTime
                classes.ending_time = endingTime
                classes.slots = slots
                classes.available_slots = availableSlots
                classes.classroom = classroom
                classes.building = building
                classes.online = online
                classes.note = note
                classes.public = public
                classes.slots_info = slotsInfo

                classes.save()
                messages.success(request, "Zmiany zostały pomyślnie zapisane")
                return redirect('home')
        
    return render(request, 'reservation_system/editClasses.html', {'classes': classes, 'reservations': reservations})