release: python manage.py showmigrations && python manage.py makemigrations attendance && python manage.py migrate && python manage.py shell < create_superuser.py
web: gunicorn app.wsgi --log-file -