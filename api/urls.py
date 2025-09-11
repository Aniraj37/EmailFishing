from django.urls import path  # <-- import path
from .views import FileReader , FileReaderView, FileByIDView      # <-- your view

urlpatterns = [
    path('file-reader/', FileReader.as_view(), name="file-reader"),
    path('failure/', FileReaderView.as_view(), name="failure-email" ),
    path('failure/<uuid:id>/', FileByIDView.as_view(), name="failure-email" )
]