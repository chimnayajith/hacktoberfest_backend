import csv
import os
from django.core.management.base import BaseCommand
from attendance.models import Attendee
from django.core.files import File
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Import attendees from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"File {csv_file_path} does not exist."))
            return

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    attendee = Attendee(
                        name=row['Name'],
                        email=row['Email'],
                        roll_no=row['Roll Number'],
                        gender=row['Gender']
                    )
                    attendee.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported attendee: {attendee.name}"))
                except ValidationError as e:
                    self.stderr.write(self.style.ERROR(f"Error importing attendee {row['Name']}: {e}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Unexpected error for {row['Name']}: {e}"))
