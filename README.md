# tailwebs

# tailwebs Project Setup Guide

## Overview
This guide will walk you through the steps to set up the Tailwebs project, which includes creating a Django project, setting up virtual environments, installing dependencies, and configuring the project with models, APIs, and the Django admin interface.


# Step 1: Create Project Directory
Create a directory for your project:
mkdir Tailwebs

# Step 2: Set Up a Virtual Environment
Create a virtual environment to isolate project dependencies:
python -m venv venv

Activate the virtual environment:
.\venv\Scripts\activate OR
source venv/bin/activate

# Step 3: Install Project Dependencies
Install the required dependencies by running the following command:
pip install -r requirements.txt

# Step 4: Create Django Project and Apps
Start a new Django project and create the necessary apps:
django-admin startproject tailwebs
cd tailwebs
python manage.py startapp account
python manage.py startapp master

# Step 5: Update settings.py
In the settings.py file, add your newly created apps (account, master) and rest_framework (for API functionality) to the INSTALLED_APPS list:

INSTALLED_APPS = [
...
'rest_framework',
'account',
'master',

]

# Step 6: Create urls.py in Each App
Inside both the account and master apps, create a urls.py file to define app-specific routes:

account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Add account-related API endpoints here
    
]

master/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Add routes for subject management here
    
]

Then, in the main urls.py file (in the tailwebs folder), include the app-specific routes:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('master/', include('master.urls')), 
    
]
# Step 7: Create .env File for Secrets
Create a .env file in the root directory to store sensitive information such as secret keys and API credentials. Example:

SECRET_KEY=your_secret_key_here
DATABASE_URL=your_database_url_here
DEBUG=True

Make sure to add .env to your .gitignore to prevent it from being committed to version control.

# Step 8: Add .gitignore File
Create a .gitignore file in the root directory and add files to exclude from version control:

*.pyc
*.pyo
*.pyd
__pycache__
venv/
*.env
db.sqlite3

# Step 9: Create Models
Create models for teacher data, student data, and any other necessary models in the models.py files of the respective apps (account, master). For example:

TeacherData: Stores teacher-specific data like username and password.
StudentData: Stores student-specific data and their associated subjects.
Run the following commands to create and apply database migrations:

python manage.py makemigrations
python manage.py migrate

# Step 10: Create Superuser
To access the Django admin panel, create a superuser:

python manage.py createsuperuser
Follow the prompts to create the superuser.

# Step 11: Run the Development Server
Start the Django development server:

python manage.py runserver
You can access the server at http://localhost:8000/. The admin panel is accessible at http://localhost:8000/django-admin/.

# Step 12: Add Subjects via Django Admin
Login to the Django admin panel and add subjects manually. These subjects will be dynamically linked to student data.

# Step 13: Create serializers.py and APIs
In the account app, create a serializers.py file to handle serialization of your models. Here's an example of how you can define serializers for TeacherData and StudentData:

from rest_framework import serializers
from .models import TeacherData, StudentData

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherData
        fields = ['username', 'password']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ['name', 'subject', 'marks']
Create the necessary API views in views.py and define routes for them in the urls.py file of the account app. This will expose endpoints for creating, updating, and retrieving teacher and student data.

