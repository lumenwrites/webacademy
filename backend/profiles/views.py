from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from .models import User, Subscriber
from .forms import RegistrationForm, UserForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
 
    nextpage = request.GET.get('next', '/')

    # Initialize the form either fresh or with the appropriate POST data as the instance
    auth_form = AuthenticationForm(None, request.POST or None)
    
    if auth_form.is_valid():
        auth_login(request, auth_form.get_user())
        return HttpResponseRedirect(nextpage)
    
    else:
        # for errors
        return render(request, 'profiles/login.html', {
            'loginform': auth_form,
        })
    
# Only sign up
def join(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
 
    nextpage = request.GET.get('next', '/')

    auth_form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            None,
                                            form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.save()

            # log user in after signig up
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect("/")
        else:
            # for errors
            return render(request, 'profiles/login.html', {
                'joinform': form,
            })

    else:
        return render(request, 'profiles/login.html', {
            'joinform': auth_form,
        })



# Email subscribe
def email_subscribe(request):
    if request.method == 'POST':    
        email = request.POST.get('email')
        ref = request.GET.get('ref')
        email_subscriber, created = Subscriber.objects.get_or_create(email=email,
                                                                     ref=ref)
        email_subscriber.save()
        
        return HttpResponseRedirect("/?notification=subscribed")


    
