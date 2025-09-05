from django.urls import path  # <-- import path
from .views import FileReader       # <-- your view

urlpatterns = [
    path('file-reader/', FileReader.as_view(), name="file-reader")
]