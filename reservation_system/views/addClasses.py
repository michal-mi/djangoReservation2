from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, Classes
from django.contrib.auth import get_user
from datetime import datetime, timedelta

def addClasses(request):
    if request.method == "POST":
        beginningTime = request.POST['beginning_time']
        endingTime = request.POST['ending_time']
        slots = request.POST['slots']
        availableSlots = slots
        classroom = request.POST['classroom']
        building = request.POST['building']
        online = request.POST['online']
        note = request.POST['note']
        public = request.POST['public']
        user = get_user(request)

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
            return render(request, 'reservation_system/addClasses.html', {'beginning_time': beginningTimeConv, 'ending_time': endingTimeConv, 'slots': slots, 'classroom': classroom, 'building': building, 'online': online, 'note': note, 'public': public})

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

            newClasses = Classes.objects.create(beginning_time=beginningTime, ending_time = endingTime, slots = slots, available_slots = availableSlots, classroom = classroom, building = building, online = online, note = note, public = public, lecturer_id = user.id, slots_info = slotsInfo)
            newClasses.save()
            messages.success(request, "Zajęcia zostały utworzone")
            return redirect('home')
    
    return render(request, 'reservation_system/addClasses.html')