from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Dashboard
from time import time
import jwt
import requests

import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.silence import split_on_silence
from django.shortcuts import render
from zoom.models import Zoom

# import pdb

# Create your views here.
@login_required(login_url="account_login")
def dashboard(request):
    if Zoom.objects.filter(user_id=request.user.id):
        context = {}
        userZoom = Zoom.objects.filter(user_id=request.user.id)[0]
        documents = Dashboard.objects.filter(user_id=request.user.id)
        token = jwt.encode(
            {"iss": "IMRIis5eQie4cCimN4-Q9Q", "exp": time() + 5000},
            "ufW7vOxxJhhy7hIEe3bSk73BE00kGUnF2MPS",
            algorithm="HS256",
        ).decode("utf-8")

        headers = {"Authorization": "Bearer " + str(token)}
        uuid = []
        detailsEndedMeetings = []

        params = {"type": "scheduled", "page_size": 30}
        # REQUEST GET USER MEETINGS
        r_get_meetings = requests.get(
            "https://api.zoom.us/v2/users/" + str(userZoom.email) + "/meetings",
            headers=headers,
            params=params,
        )
        meetingsInfo = r_get_meetings.json()
        # REQUEST GET USER ENDED MEETINGS
        r_ended_meetings = requests.get(
            f"https://api.zoom.us/v2/past_meetings/{userZoom.meetingId}/instances",
            headers=headers,
        )
        endedMeetings = r_ended_meetings.json()
        # EXTRACTING UUID
        for i in range(len(endedMeetings["meetings"])):
            uuid.append(endedMeetings["meetings"][i]["uuid"])
        # GET TOPIC ENDED MEETINGS
        if len(uuid) >= 4:
            rango = 4
        else:
            rango = len(uuid)
        for i in range(rango):
            r_get_details_ended_meetings = requests.get(
                f"https://api.zoom.us/v2/past_meetings/{uuid[i]}", headers=headers
            )
            detailsMeeting = r_get_details_ended_meetings.json()
            try:
                detailsMeeting.pop("dept")
                detailsMeeting.pop("duration")
                detailsMeeting.pop("host_id")
                detailsMeeting.pop("id")
                detailsMeeting.pop("total_minutes")
                detailsMeeting.pop("type")
                detailsMeeting.pop("user_email")
                detailsMeeting.pop("user_name")
                detailsMeeting.pop("user_name")
            except:
                print(f"error: {detailsEndedMeetings}")
                pass
            detailsEndedMeetings.append(detailsMeeting)
            print(detailsEndedMeetings)

        # CONTEXT DATA
        context["dataUser"] = userZoom.email
        context["meetingsInfo"] = meetingsInfo["meetings"]
        context["topicEndedMeetings"] = detailsEndedMeetings

        return render(request, "dashboard.html", context)
    else:
        return render(request, "dashboard.html")


@login_required(login_url="account_login")
def my_conversation(request):
    docid = int(request.GET.get("docid", 0))
    documents = Dashboard.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        docid = int(request.POST.get("docid", 0))
        title = request.POST.get("title")
        content = request.POST.get("content", "")
        if title == "":
            count = 1
            title = "default"
            while documents.filter(title=title):
                title = "default" + " (" + str(count) + ")"
                count += 1
        else:
            count = 0
            auxTitle = title
            while documents.filter(title=auxTitle):
                count += 1
                auxTitle = title
                auxTitle += " (" + str(count) + ")"

            if count > 0:
                title = title + " (" + str(count) + ")"
        if content == "":
            messages.info(request, "Error, note without content.")
            return redirect("/dashboard/my_conversation/")

        data = {"text": content}

        r = requests.post("http://bark.phon.ioc.ee/punctuator", data=data)

        content = r.text
        messages.info(request, "Note added success")
        if docid > 0:
            document = Dashboard.objects.get(pk=docid)
            document.title = title
            document.content = content
            document.save()

            return redirect("/dashboard/my_conversation/")
        else:
            document = Dashboard.objects.create(title=title, content=content)

            return redirect("/dashboard/my_conversation/")

    if docid > 0:
        document = Dashboard.objects.get(pk=docid)
    else:
        document = ""

    context = {"docid": docid, "documents": documents, "document": document}

    return render(request, "my_conversation.html", context)


@login_required(login_url="account_login")
def settings(request):
    error = True
    if request.method == "POST":
        username = request.POST.get("username")
        newusername = request.POST.get("newusername")
        email = request.POST.get("email")
        newemail = request.POST.get("newemail")
        oldpassword = request.POST.get("oldpassword")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        user = authenticate(request, username=username, password=oldpassword)

        if user != None:

            usuario = User.objects.get(username=username)

            if user is not None:
                if (
                    password1 == password2
                    and password1 != ""
                    and password2 != ""
                    and password1 != usuario.password
                ):
                    usuario.password = password1
                    messages.success(request, "Password changed succesfully")
                    error = False
                if newemail != user.get_email_field_name and newemail != "":
                    if User.objects.filter(email=newemail).exists():
                        pass
                    else:
                        usuario.email = newemail
                        messages.success(request, "Email changed succesfully")
                        error = False
                if (
                    user.get_username != newusername
                    and newusername != ""
                    and len(newusername) > 5
                ):
                    if User.objects.filter(username=newusername).exists():
                        pass
                    else:
                        usuario.username = newusername
                        messages.success(request, "Username changed succesfully")
                        error = False
                if error is True:
                    messages.error(
                        request,
                        "Error changing info. Please make sure the data fields are correctly.",
                    )
                else:
                    usuario.save()

        else:
            messages.error(
                request, "Wrong password! Please write your password correctly"
            )

    context = {}
    return render(request, "settings.html", context)


def delete_document(request, docid):
    document = Dashboard.objects.get(pk=docid)
    document.delete()

    return redirect("/dashboard/my_conversation/")


def chunks_speech_recognition(request):
    # CONSTANTS
    documents = Dashboard.objects.filter(user_id=request.user.id)
    docid = int(request.GET.get("docid", 0))
    context = {}
    filename = os.getcwd() + "\\" + "audio.wav"
    FORMAT = "wav"
    min_silence_len = 1000
    silence_tresh = -60
    duration = 10
    adjust_ambient_noise = False
    message = ""
    msg = ""
    # Handle audio format
    myaudio = AudioSegment.from_wav(filename)
    start_making_chunks = time()

    print("Making chunks...")
    # Make chunks of one sec
    # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length=4000)
    # chunks = split_on_silence(
    #    audio_segment=myaudio,
    # must be silent for at least 0.5 seconds
    # or 500 ms. adjust this value based on user
    # requirement. if the speaker stays silent for
    # longer, increase this value. else, decrease
    #    min_silence_len=min_silence_len,
    # consider it silent if quieter than -16 dBFS
    # adjust this per requirement
    #    silence_thresh=silence_tresh,
    # )
    elapsed_making_chunks = time() - start_making_chunks
    print("Elapsed time making chunks: {0}".format(elapsed_making_chunks))
    print(f"chunks: {chunks}")
    # Handle Errors and update response with try Error
    response = {"success": True, "error": None, "transcription": None}

    limit, MULT = 1, 5
    for i, chunk in enumerate(chunks):
        # Silence chunk: duration specified in milliseconds
        chunk_silent = AudioSegment.silent(duration=duration)

        # add silence beginning & end of audio chunk
        # it doesn't seem abruptly sliced
        # less chunck_silent could improve the speed, but decrease the accuracy
        audio_chunk = chunk_silent + chunk + chunk_silent
        chunk_name = "chunk{0}.wav".format(i)
        print("exporting", chunk_name)
        audio_chunk.export(out_f=chunk_name, bitrate="192k", format=FORMAT)
        filename = "chunk" + str(i) + ".wav"

        print("Processing chunk: " + str(i))

        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            # could increase accuracy, but decrease speed and accuracy in some parts
            if adjust_ambient_noise:
                r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            if i == limit * MULT:
                with open("result.txt", "a") as f:
                    f.write("\n")
                limit += 1
            else:
                msg = r.recognize_google(
                    audio_data=audio, language="en-US", show_all=False
                )
                message += " " + msg

                response["transcription"] = msg
        except sr.UnknownValueError:
            response["error"] = logging.debug(
                "Speech recognition could not understand the audio"
            )
        except sr.RequestError as e:
            response["success"] = False
            response["error"] = logging.debug(
                "API is unreachable. Coult not request results from Speech Recognition service: {0}".format(
                    e
                )
            )
        os.remove(path=chunk_name)
        print(response)
    context = {
        "docid": docid,
        "documents": documents,
        "message": message,
    }
    # os.remove(filename)
    return render(
        request=request, template_name="my_conversation.html", context=context
    )
