from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from ..tokens import generate_token
from web_app import settings
import re

def signup(request):
    if request.method == "POST":
        # username = request.POST['userName']
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        emailAddress = request.POST.get('email')
        password = request.POST.get('password')
        passwordConfirmation = request.POST.get('passwordConfirmation')

        error = False

        if User.objects.filter(username=username):
            error = True
            messages.error(request, "Taka nazwa użytkownika jest już w użyciu")

        if User.objects.filter(email=emailAddress):
            error = True
            messages.error(request, "Istnieje już konto o tym adresie email")
        
        if password != passwordConfirmation:
            error = True
            messages.error(request, "Podane hasła różnią się")

        if not any([
            re.search(r"[A-Z]", password),
            re.search(r"[a-z]", password),
            re.search(r"[0-9]", password),
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password),
            len(password) >= 8
        ]):
            error = True
            messages.error(request, "Hasło nie spełnia wymagań")
        
        if error == False:
            myuser = User.objects.create_user(username, emailAddress, password)
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.is_superuser = 0
            myuser.is_active = False
            myuser.save()

            messages.success(request, "Twoje konto zostało pomyślnie. Został Ci wysłany mail aktywacyjny")

            current_site = get_current_site(request)
            subject = "System rezerwacji - utworzenie konta"
            link = render_to_string('account_confirmation.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                subject,
                link,
                settings.EMAIL_HOST_USER,
                [myuser.email]
            )
            email.fail_silently = True
            email.send()

            return redirect('signin')
        
        if error:
            return render(request, 'reservation_system/signup.html', {'username': username, 'firstName': firstName, 'lastName': lastName, 'email': emailAddress, 'password': password, 'passwordConfirmation': passwordConfirmation})
    
    return render(request, 'reservation_system/signup.html')