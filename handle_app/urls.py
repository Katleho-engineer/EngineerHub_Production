from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('proflie/<int:pk>', views.userProfilePage, name='profile'),
    path('update-user/', views.updateUserPage, name='update-user'),

    path('rooms/', views.roomsPage, name='rooms'),
    path('room/<int:pk>/', views.roomDetailPage, name='room-detail'),

    path('create-room/', views.createRoomPage, name='create-room'),
    path('update-room/<int:pk>', views.updateRoomPage, name='update-room'),
    path('delete-room/<int:pk>', views.deleteRoomPage, name='delete-room'),

    path('delete-message/<int:pk>', views.deleteMessagePage, name='delete-message'),

    path('test/<int:pk>/', views.TestPage)
]