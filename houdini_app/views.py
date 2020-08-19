from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import requests
from time import time
import jwt
import base64


def index(request):
    response = redirect("login")
    return response


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        form = CreateUserForm(
            username=username, email=email, password1=password1, password2=password2
        )
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            return redirect("account_email_verification_sent.html")

    context = {"form": form}
    return render(request, "account_signup", context)


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, "Username OR password is incorrect")
            return redirect("login")

    context = {}
    return render(request, "account/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("account_logout")


@login_required(login_url="account_login")
def zoom(request):
    return render(request, "index.html")


@login_required(login_url="account_login")
def meeting(request):
    return render(request, "meeting.html")


def speech(request):
    return render(request, "speech.html")


def testrequest(request):

    # OBTENER LOS TOKEN DE LA APP
    token = jwt.encode(
        {"iss": "xRNfGvDQT4KYNHx2BlYf-A", "exp": time() + 5000},
        "SJYmVPJc4nlp4FqIozn7hxy3QPiita2QWxVN",
        algorithm="HS256",
    ).decode("utf-8")
    # OBTENER LA INFORMACIÓN DEL USUARIO DE ZOOM
    context = {}

    # OBTENER LAS REUNIONES AGENDADAS DEL USUARIO
    """
    if request.method == "POST":
        userId = request.POST.get("userId")

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        params= {
            'type': 'live',
            'page_size': 30
        }

        r = requests.get('https://api.zoom.us/v2/users/'+str(userId)+'/meetings', headers=headers, params=params)

        rr = requests.get('https://api.zoom.us/v2/users/me', headers=headers)

        data = r.json()
        data2 = rr.json()
        context = {'respuesta':data}
        print(token)"""

    # OBTENER LAS GRABACIONES DE LA NUBE DEL USUARIO
    if request.method == "POST":
        userId = request.POST.get("userId")
        headers = {"Authorization": "Bearer " + str(token)}

        print(f"headers: {headers}")
        data = {"page_size": 30, "trash_type": "meeting_recordings"}
        r = requests.get(
            "https://api.zoom.us/v2/users/" + str(userId) + "/recordings",
            headers=headers,
            data=data,
        )
        print(token)
        data = r.json()
        context = {"respuesta": data}

    return render(request, "testrequest.html", context)


# @login_required(login_url='account_login')
"""
@login_required(login_url='account_login')
def upload(request):
    # customHeader = request.META['HTTP_MYCUSTOMHEADER']
    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    # filename = str(Chat.objects.count())
    # filename = filename + "name" + ".wav"

    with open(filename, 'wb') as uploadedFile:
        # the actual file is in request.body
        uploadedFile.write(text=request.body)

    # capture data from file
    r = sr.Recognizer()
    harvard = sr.AudioFile(filename_or_fileobject=filename)
    with harvard as source:
        r.adjust_for_ambient_noise(source=source)
        audio = r.record(source=source)

    # Handle Errors and update response with try Error
    response = {
        'success': True,
        'error': None,
        'transcription': None
    }

    try:
        msg = r.recognize_google(
            audio_data=audio, language='en-US', show_all=True)
        response['transcription'] = msg
    except sr.UnknownValueError:
        response['error'] = loggin.debug(
            'Speech recognition could not understand the audio')
    except sr.RequestError as e:
        response['success'] = False
        response['error'] = loggin.debug(
            'API is unreachable. Coult not request results from Speech Recognition service: {0}'.format(e))
    print(f'\n{response}')

    # os.remove(filename)
    # chat_message = Chat(user=request.user, message=msg)
    # if msg != '':
    #    chat_message.save()
    return redirect('/')

"""

