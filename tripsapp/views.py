from django.shortcuts import render, redirect
from django.contrib import messages
from tripsapp.models import *
import bcrypt

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    return render(request, 'index.html')

def register(request):
    error = User.objects.regValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user=User.objects.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['email'], password=pw_hash)
    request.session['user']=user.id
    return redirect('/dashboard')

def login(request):
    error = User.objects.loginValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user']=user.id
    return redirect('/dashboard')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    user =User.objects.get(id=request.session['user'])
    trips = Trip.objects.all()
    user_trips = Trip.objects.filter(attendees=user)
    context={
        'user':user,
        'user_trips':user_trips,
        'trips':trips
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    del request.session['user']
    return redirect('/')

def new(request):
    user = User.objects.get(id=request.session['user'])
    context={
        'user':user
    }
    return render(request, 'new.html', context)

def add_new(request):
    error = User.objects.infoValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='info')
        return redirect('/trips/new')
    creator = User.objects.get(id=request.session['user'])
    trip=Trip.objects.create(location=request.POST['location'], plan=request.POST['plan'], creator=creator, start=request.POST['start'], end= request.POST['end'])
    trip.attendees.add(creator)
    return redirect('/dashboard')

def trips(request, id):
    user=User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    attendees = trip.attendees.all()
    context ={
        'user':user,
        'trip':trip,
        'attendees':attendees
    }
    return render(request, 'trip_info.html', context)

def edit(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    start= str(trip.start)
    end = str(trip.end)
    context={
        'trip':trip,
        'user':user,
        'start':start,
        'end':end
    }
    return render(request, 'edit.html', context)

def edit_trip(request, id):
    error = User.objects.editValidator(request.POST)
    trip = Trip.objects.get(id=id)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='edit')
        return redirect('/trips/edit/'+str(id))
    trip.location= request.POST['location']
    print(request.POST['start'])
    trip.start = request.POST['start']
    trip.end=request.POST['end']
    trip.plan = request.POST['plan']
    trip.save()
    return redirect('/dashboard')

def join(request, id):
    user = User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    user.trips.add(trip)
    return redirect('/dashboard')

def remove(request,id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/dashboard')

def cancel(request,id):
    user=User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    trip.attendees.remove(user)
    return redirect('/dashboard')