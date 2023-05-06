from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.contrib.auth.models import User, Classes, Reservation
from django.contrib.auth import get_user
from datetime import datetime,  time
from web_app import settings
import json


def makeReservation(request):
    # pobieramy z bazy danych wszystkie zajęcia
    classes = Classes.objects.filter(beginning_time__gte=datetime.now())
    # tworzymy pusty słownik na daty zajęć
    dates = {}
    now = datetime.now()
    # iterujemy po zajęciach i wypełniamy słownik dat
    for single_class in classes:
        date = single_class.beginning_time.date()
        time_start = single_class.beginning_time.time()
        time_end = single_class.ending_time.time()
        slots_info = json.dumps(single_class.slots_info)
        if date not in dates and single_class.public == 1:
            dates[date] = []
        if (date > now.date() or (date == now.date() and time_start > now.time())) and single_class.public == 1 :
            dates[date].append({
                'class_id': single_class.id,
                'slots': single_class.slots,
                'available_slots': single_class.available_slots,
                'start_time': time_start.strftime('%H:%M'),
                'end_time': time_end.strftime('%H:%M'),
                'classroom': single_class.classroom,
                'building': single_class.building,
                'online': single_class.online,
                'slots_info': slots_info
            })

    if request.method == "POST":
        slots_info = request.POST['slots_info']
        available_slots =  request.POST['available_slots']
        note = request.POST['note']
        friendly_number = request.POST['friendly_number']
        class_id = request.POST['class_id']
        user = get_user(request)
        beginning_time = request.POST['beggining_time']
        ending_time = request.POST['ending_time']

        print(beginning_time)

        micro = 000000
        hourBeg = beginning_time[11:13]
        minutesBeg = beginning_time[14:16]
        secondsBeg = beginning_time[17:19]
        hourEnd = ending_time[11:13]
        minutesEnd = ending_time[14:16]
        secondsEnd = ending_time[17:19]
        beginningTimeConv = time(hour=int(hourBeg), minute=int(minutesBeg), second=int(secondsBeg), microsecond=int(micro))
        endingTimeConv = time(hour=int(hourEnd), minute=int(minutesEnd), second=int(secondsEnd), microsecond=int(micro))

        newReservation = Reservation.objects.create(note=note, friendly_number=friendly_number, classes_id=class_id, student_id=user.id, beggining_time=beginningTimeConv, ending_time = endingTimeConv)
        newReservation.save()

        chosenClass = Classes.objects.get(id=class_id)
        chosenClass.slots_info = slots_info
        chosenClass.available_slots = available_slots 
        chosenClass.save()

        subject = "System rezerwacji - utworzenie rezerwacji " + friendly_number
        link = render_to_string('reservation_confirmation.html',{
            'fname': user.first_name,
            'friendly_number': friendly_number,
            'classes_beg': chosenClass.beginning_time,
            'classes_end': chosenClass.ending_time,
            'online': chosenClass.online,
            'building': chosenClass.building,
            'classroom': chosenClass.classroom,
            'slot_beg': beginningTimeConv,
            'slot_end': endingTimeConv,
            'note': note
        })
        email = EmailMessage(
            subject,
            link,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = True
        email.send()

        messages.success(request, "Rezerwacja została utworzona. Możesz ją zobaczyć w widoku Moje Rezerwacje. Zostało ci również wysłane potwierdzenie")
        

    
    return render(request, 'reservation_system/makeReservation.html', {'dates': dates})