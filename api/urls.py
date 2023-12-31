from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('rooms-list/', views.RoomsPage.as_view(), name='rooms-api'),
    path('room/<int:pk>/', views.RoomDetailPage.as_view(), name='room-api'),
    path('room-create/', views.CreateRoomsPage.as_view(), name='room-api'),

    path('messages', views.MessagesPage.as_view(), name='message-api'),
    path('room-messages/<int:pk>', views.RoomMessages.as_view(), name='room-messages-api'),
    path('user-messages/<int:pk>', views.UserMessages.as_view(), name='user-messages-api'),

    path('topics/', views.Topics.as_view(), name='topics-api'),
    path('topic/<int:pk>/', views.Topic.as_view(), name='topic-api'),

    path('account/login', obtain_auth_token, name='login-api'),
    path('account/register', views.Registration, name='register-api'),
    path('account/logout', views.Logout, name='logout-api'),
]