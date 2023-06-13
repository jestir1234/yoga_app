from django.urls import path, include
from workshop.views import (
    UserCreateView, 
    UserDetail, 
    UserUpdateView, 
    login_view, 
    home_view, 
    logout_view, 
    register_view, 
    users_list_view, 
    workshop_create_view, 
    workshop_list_view,
    workshop_delete,
    book_workshop,
    book_workshops,
    cancel_booking,
    list_bookings,
    my_workshops,
    edit_workshop,
    edit_user
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/create', UserCreateView.as_view(), name='user_create'),
    path('users/register', register_view, name='register_view'),
    path('users/', users_list_view, name='user-list'),
    path('users/<int:user_id>', UserDetail.as_view(), name='user-detail'),
    path('users/login', login_view, name='login_view'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='log_out'),
    path('workshop/create/', workshop_create_view, name='workshop_create_view'),
    path('workshops/', workshop_list_view, name='workshops_list'),
    path('workshops/<int:workshop_id>/delete/', workshop_delete, name='workshop_delete'),
    path('workshops/book/', book_workshops, name='book_workshops'),
    path('workshops/<int:workshop_id>/book/', book_workshop, name='book_workshop'),
    path('workshops/bookings/', list_bookings, name='list_bookings'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('my-workshops/', my_workshops, name='my_workshops'),
    path('my-workshops/edit/<int:workshop_id>/', edit_workshop, name='edit_workshop'),
    path('edit-user/', edit_user, name='edit_user'),
]
