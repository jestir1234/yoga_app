from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Workshop, Booking, User
from django.contrib import messages

from .serializers import UserSerializer
from .forms import WorkshopForm, PersonalInfoForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = "Invalid login credentials"
    else:
        message = ""
    return render(request, 'login.html', {'message': message})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def home_view(request):
  return render(request, 'home.html', {'message': 'Not found'})


def register_view(request):
    return render(request, 'user_create.html', {'message': 'Not found'})

def users_list_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users_list.html', context)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(View):
    def get(self, request):
        users = User.objects.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'type': user.type,
                'email': user.email,
            })
        return JsonResponse({'users': user_list})


class UserDetail(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': user.type,
            'email': user.email,
        }
        return JsonResponse(user_data)


class UserUpdateView(View):
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        data = request.POST

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)

        user.save()

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': user.type,
            'email': user.email,
        })


@login_required
def my_view(request):
    # Only authenticated users can access this view
    ...

@login_required
@user_passes_test(lambda user: user.type == 'teacher', login_url='home')
def workshop_create_view(request):
    """
    View for creating workshops.
    """
    teachers = User.objects.filter(type="teacher")
    context = {'teachers': teachers}
    if request.method == 'POST':
        print('inside workshop_create_view post')
        form = WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            print('FORM IS VALID')
            workshop = form.save(commit=False)
            workshop.teacher = request.user
            workshop.save()
            form.save_m2m()
            return redirect('workshops_list')
        else:
            print('FORM IS INVALID')

    else:
        form = WorkshopForm()

    context['form'] = form
    return render(request, 'workshop_create.html', context)


@login_required
@user_passes_test(lambda user: user.type == 'teacher', login_url='home')
def workshop_list_view(request):
    workshops = Workshop.objects.all()
    context = {'workshops': workshops}
    return render(request, 'workshops_list.html', context)


def workshop_delete(request, workshop_id):
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=workshop_id)
            workshop.delete()
            return redirect('workshops_list')
        except Workshop.DoesNotExist:
            return HttpResponse(status=404)


@login_required
def book_workshops(request):
    workshops = Workshop.objects.all()
    booked_workshops = Booking.objects.filter(
        user=request.user).values_list('workshop_id', flat=True)
    bookings = [
        workshop for workshop in workshops if workshop.id in booked_workshops]
    context = {'workshops': workshops, 'bookings': bookings}
    return render(request, 'workshop_booking.html', context)


@login_required
def book_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    if request.method == 'POST':
        if workshop != None:
            # Create a new booking object and save it
            booking = Booking.objects.create(
                user=request.user,
                workshop=workshop,
            )
            booking.user = request.user
            booking.workshop = workshop
            booking.save()
            return redirect('book_workshops')
        else:
            print('WORKSHOP NOT FOUND')
            return HttpResponse(status=404)
        

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    workshop = booking.workshop
    booking.delete()
    return redirect('book_workshops')


@login_required
def list_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings_list.html', {'bookings': bookings})


@login_required
@user_passes_test(lambda user: user.type == 'teacher', login_url='home')
def my_workshops(request):
    workshops = Workshop.objects.filter(teacher=request.user)
    return render(request, 'my_workshops.html', {'workshops': workshops})


@login_required
@user_passes_test(lambda user: user.type == 'teacher', login_url='home')
def edit_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)

    if request.method == 'POST':
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid():
            form.save()
            return redirect('my_workshops')
    else:
        form = WorkshopForm(instance=workshop)

    context = {'form': form}
    return render(request, 'edit_workshop.html', context)


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Personal information updated successfully.')
            return redirect('home')
    else:
        form = PersonalInfoForm(instance=request.user)

    context = {'user': request.user}
    return render(request, 'user_edit.html', context)
