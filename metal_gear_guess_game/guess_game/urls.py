from django.urls import path

from . import views


app_name = "guess_game"
urlpatterns = [
    path('start_of_guess', views.start_of_guess, name='start_of_guess'),
    path('start_of_guess/lose_in_guess', views.lose_in_guess, name='lose_in_guess'),
    path('start_of_guess/win_in_guess', views.win_in_guess, name='win_in_guess'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.login_page, name='logout'),

]