from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm

#For login system
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.Alot of coding

# Basic idea is to check if there is a POST request and perform some action based on the information

# sometimes we will want to save directly to the database, other times we set commit = false, so we can manipulate database


def index(request):
    return render(request,'basicapp/index.html')

#to check if user is login_required
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basicapp:index'))

@login_required
def special(request):
    return HttpResponse('youre logged in')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # FOR USER forms
            user = user_form.save()

            #hashing the password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)

            #Sets up one to one relationship
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basicapp/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #automatically authenticate user
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('basicapp:index'))


            else:
                return HttpResponse("Your account has been deactivated")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid Login details supplied!")

    else:
        return render(request,'basicapp/login.html')
