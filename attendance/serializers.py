from rest_framework import serializers
from .models import Attendee, Attendance

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['uuid', 'name', 'roll_no', 'gender', 'email']

class AttendanceSerializer(serializers.ModelSerializer):
    attendee = AttendeeSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['attendee', 'intime']
