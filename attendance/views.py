from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendee, Attendance, Session
from django.utils import timezone

class TrackAttendanceView(APIView):
    def post(self, request, *args, **kwargs):
        uuid = request.data.get('uuid')
        session_id = request.data.get('session_id')

        if not uuid or not session_id:
            return Response({"error": "UUID and Session ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendee = Attendee.objects.get(uuid=uuid)
        except Attendee.DoesNotExist:
            return Response({"error": "Attendee not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = Session.objects.get(number=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        attendance = Attendance.objects.filter(attendee=attendee, session=session, outtime__isnull=True).first()

        if attendance:
            attendance.check_out()
            return Response({
                "message": "Checked out successfully.",
                "outtime": attendance.outtime,
                "attendee": {
                    "name": attendee.name,
                    "roll_no": attendee.roll_no,
                    "gender": attendee.gender,
                    "email": attendee.email,
                    "uuid": attendee.uuid,
                },
                "session": {
                    "name": session.name,
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "duration": session.duration,
                }
            }, status=status.HTTP_200_OK)
        else:
            Attendance.objects.create(attendee=attendee, session=session, intime=timezone.now())
            return Response({
                "message": "Checked in successfully.",
                "intime": timezone.now(),
                "attendee": {
                    "name": attendee.name,
                    "roll_no": attendee.roll_no,
                    "gender": attendee.gender,
                    "email": attendee.email,
                    "uuid": attendee.uuid,
                },
                "session": {
                    "name": session.name,
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "duration": session.duration,
                }
            }, status=status.HTTP_200_OK)
