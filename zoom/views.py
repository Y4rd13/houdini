from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Zoom
#from punctuator import Punctuator
from time import time
import jwt
import requests
# Create your views here.

@login_required(login_url='account_login')
def requestInfo(request):
        context = {}
        # OBTENER LOS TOKEN DE LA APP
        token = jwt.encode(
        {"iss": 'IMRIis5eQie4cCimN4-Q9Q', "exp": time() + 5000},
        'ufW7vOxxJhhy7hIEe3bSk73BE00kGUnF2MPS',
        # Specify the hashing alg
        algorithm='HS256'
        ).decode('utf-8')
        # Convert token to utf-8
        headers = {
            "Authorization": "Bearer " + str(token)
        }
        # REQUEST GET USER INFORMATION
        r_info_user = requests.get('https://api.zoom.us/v2/users/me', headers=headers)
        dataUser = r_info_user.json()

        #----SAVE USER INFO------|
        if (Zoom.objects.filter( user_id=request.user.id)):
            messages.info(request,"Error, you already have an associated zoom account.")
            return render(request, 'requestZoomInfo.html')
        elif(Zoom.objects.filter( email =  dataUser['email'])):
            messages.info(request,"Error, the Zoom account is already being used in another account.")
            return render(request, 'requestZoomInfo.html')
        else:
            user = Zoom.objects.create(idAccount = dataUser['id'], firstName = dataUser['first_name'], lastName = dataUser['last_name'], email =  dataUser['email'], meetingId = dataUser['pmi'], personalMeetingUrl = dataUser['personal_meeting_url'])
            user.save()
            messages.info(request, "Zoom account added")
            return render(request, 'requestZoomInfo.html')
        #-----------------------|
