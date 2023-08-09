from django.urls import path

from flight.views import FlightsListAPIView

urlpatterns = [
    path(
        "consult/<str:origin>/<str:destination>/<str:departure_date>/<str:return_date>",
        FlightsListAPIView.as_view(),
    ),
]
