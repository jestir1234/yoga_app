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
    workshop_delete
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/create', UserCreateView.as_view(), name='user_create'),
    path('users/register', register_view, name='register_view'),
    path('users/', users_list_view, name='user-list'),
    path('users/<int:user_id>', UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/login', login_view, name='login_view'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='log_out'),
    path('workshop/create/', workshop_create_view, name='workshop_create_view'),
    path('workshops/', workshop_list_view, name='workshops_list'),
    path('workshops/<int:workshop_id>/delete/', workshop_delete, name='workshop_delete'),
]
