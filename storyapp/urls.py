from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('index',views.index),
    path('engine',views.engine),

    path('login_view',views.login_view),
    path('register',views.register),
    path('logout_view',views.logout_view),
    path('profile',views.profile),

    path('history',views.history),
]
