from django.urls import path, include
from airport.views import AirportListView

urlpatterns = [
    path("list", AirportListView.as_view()),
]
