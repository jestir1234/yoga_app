from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from .models.users import User
from .models import Workshop

from .serializers import UserSerializer
from .forms import WorkshopForm

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
    print('request', request)
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=workshop_id)
            workshop.delete()
            return redirect('workshops_list')
        except Workshop.DoesNotExist:
            return HttpResponse(status=404)
    else:
        print('NOT DELETE')
        return ''
