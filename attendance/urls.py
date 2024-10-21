from django.urls import path
from .views import TrackAttendanceView

urlpatterns = [
    path('track-attendance/', TrackAttendanceView.as_view(), name='track-attendance'),
]
