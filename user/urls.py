from rest_framework.authtoken import views
from django.urls import path

from user.views import UserRegistrationView

urlpatterns = [
    path("register", UserRegistrationView.as_view()),
    path("obtain-token", views.obtain_auth_token),
]
