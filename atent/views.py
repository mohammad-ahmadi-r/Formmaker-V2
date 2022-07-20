from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect
from .models import Token
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


############################### User Registration ###########################################
def register(request):
    if request.method == "POST":
        username=request.POST['username']
        email = request.POST["email"]
        password = request.POST["password"]
        confpass = request.POST["conf-pass"]

        if password == confpass:
            if User.objects.filter(username=username).exists():
                messages.warning(request, "This username is already in use")
                return redirect('atent:register')

            User.objects.create_user(username= username, password= password, email= email)
            messages.success(request, "You successfully registerd:)")
            return redirect(reverse("form:index"))
        messages.warning(request, "password doesn't match")
        return redirect('atent:register')
    return render(request ,"atent/register.html")


################################# User Login ################################################
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            User.objects.get(username= username)
        except:
            messages.warning(request, "No such username!" )
            return HttpResponseRedirect(reverse("atent:login"))

        user = authenticate(request , username= username , password= password)
        if user is not None:
            if 'next' in request.POST:
                    login(request , user)
                    messages.success(request, "You successfully logged in!" )
                    return redirect(request.POST['next'])
            login(request, user)
            messages.success(request, "You successfully logged in!" )
            return HttpResponseRedirect(reverse("form:index"))

        messages.success(request, "Invalid Username or Password" )
        return HttpResponseRedirect(reverse("atent:login"))

    return render(request ,"atent/login.html")


################################# User Logout ############################################
def logout_view(request):
    logout(request)
    messages.success(request, "You successfully logged out!" )
    return HttpResponseRedirect(reverse("form:index"))


################################ Send email to reset password ###########################
def forgot_password(request):

    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
            t = Token(user_id=user, type=1)
            t.save()
        except:
            try:
                user = User.objects.get(email=request.POST["username"])
                t = Token(user_id=user, type=1)
                t.save()
            except:
                messages.warning(request, "No such User or Email!")
                return HttpResponseRedirect(reverse("form:index"))
        try:
            subject = 'change password'
            message = """From: From Person <"itsme@gmail.com">
            Subject: Reset Password

            http://localhost:8000/auth/reset-password/{num}/
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            
            send_mail( subject, message.format(num = t.id), email_from, recipient_list )
            messages.success(request, "Please check your email for next step." )
            return HttpResponseRedirect(reverse("form:index"))

        except Exception as ex:
            messages.warning(request, "Something went wrong. please try again later" )
            return HttpResponseRedirect(reverse("form:index"))
    else:
        return render(request, "atent/forgot-password.html")


############################# Reset user password #####################################
def reset_password(request, token):
    if request.method == "POST":
        t = Token.objects.get(id=token, type=1)
        user = User.objects.get(id=t.user_id)
        user.set_password(request.POST["password"])
        user.save()
        t.delete()
        messages.warning(request, "Password updated successfully" )
        return HttpResponseRedirect(reverse("atent:login"))
    else:
        try:
            t = Token.objects.get(id=token, type=1)
            return render(request, "atent/reset-password.html", {
                "username": User.objects.get(id=t.user.id).username
            })
        except:
            messages.warning(request, "Token not found! please try again later" )
            return HttpResponseRedirect(reverse("form:index"))
