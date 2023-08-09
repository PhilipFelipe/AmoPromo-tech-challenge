from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("airport/", include("airport.urls")),
    path("flight/", include("flight.urls")),
]
