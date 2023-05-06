from django.urls import path
from reservation_system.views.index import home
from reservation_system.views.signup import signup
from reservation_system.views.signin import signin
from reservation_system.functions import signout, activate
from reservation_system.views.myAccount import myAccount
from reservation_system.views.makeReservation import makeReservation
from reservation_system.views.myReservations import myReservations
from reservation_system.views.addClasses import addClasses
from reservation_system.views.classesList import classesList
from reservation_system.views.beginNewSemester import beginNewSemester
from reservation_system.views.classesDetails import classesDetails
from reservation_system.views.editClasses import editClasses

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('makeReservation/', makeReservation, name='makeReservation'),
    path('myReservations/', myReservations, name='myReservations'),
    path('addClasses/', addClasses, name='addClasses'),
    path('classesList/', classesList, name='classesList'),
    path('beginNewSemester/', beginNewSemester, name='beginNewSemester'),
    path('classesDetails/<int:pk>/', classesDetails, name='classesDetails'),
    path('editClasses/<int:pk>/', editClasses, name='editClasses'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]