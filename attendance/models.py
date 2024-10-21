from django.db import models
import uuid
from django.utils import timezone
from django.db.models import Max
from datetime import timedelta
from .utils.qr_generator import generate_qr_code
from .utils.sendMail import send_attendee_welcome_email

class Attendee(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_code_file = generate_qr_code(str(self.uuid))
            self.qr_code.save(f'{self.uuid}.png', qr_code_file, save=False)
        super().save(*args, **kwargs)

        send_attendee_welcome_email(self)


class Session(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField(unique=True, default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DurationField(blank=True, null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            start_datetime = timezone.datetime.combine(timezone.now().date(), self.start_time)
            end_datetime = timezone.datetime.combine(timezone.now().date(), self.end_time)
            self.duration = end_datetime - start_datetime

        if not self.pk:
            max_number = Session.objects.aggregate(Max('number'))['number__max']
            self.number = max_number + 1 if max_number is not None else 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    intime = models.DateTimeField(null=True, blank=True)
    outtime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.attendee.name} - {self.session.name} - {self.intime or 'No check-in'}"

    def check_out(self):
        self.outtime = timezone.now()
        self.save()
