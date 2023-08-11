from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("airport/", include("airport.urls")),
    path("flight/", include("flight.urls")),
]
