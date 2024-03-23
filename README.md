After cloning the repo locally.
Run `python manage.py runserver`
If you run into any packages that is missing, install them with pip.
After the local development server is running, you might be prompted to do db migration.
Run `python manage.py migrate`
And then run `python manage.py createsuperuser` to create your admin user for testing
finally visit the local host to test out the web-app
