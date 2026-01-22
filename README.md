<a id="top" href="https://momentum-backend-d83acc164707.herokuapp.com/admin/" target="_blank">
<img src="documentation/readme_images/logo-white.webp"></a><br />

<h2>Momentum Backend API</h2>

<h1 id="contents">Contents</h1>

- [Introduction](#introduction)
- [Database Schema](#database-schema)
- [User Stories](#user-stories)
- [Agile Methodology](#agile-methodology)
- [Technologies Used](#technologies-used)
  - [Languages](#languages)
  - [Frameworks, libraries, and Programs](#frameworks-libraries-and-programs)
- [Testing Automated and Manual](TESTING.md)
- [Bugs](#bugs)
- [Project Setup](#project-setup)
- [Deployment](#deployment)
  - [Setting up JSON web tokens](#setting-up-json-web-tokens)
  - [Prepare API for deployment to Heroku](#prepare-api-for-deployment-to-heroku)
  - [Deployment to Heroku](#deployment-to-heroku)
  - [Database Creation](#database-creation)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

## Introduction

This repository contains the backend API for the Momentum habit tracking application, built using Django and Django REST Framework as part of Code Institute’s Portfolio Project 5.

The backend is responsible for user authentication, habit data management, and enforcing ownership and permission rules. It exposes a RESTful API consumed by the deployed React frontend.

The backend does not serve a frontend user interface. The root URL intentionally returns a 404 response, as all functionality is accessed via API endpoints. The Django admin interface is available for administrative access only.

The React frontend repository can be found here:  
https://github.com/Bear81/momentum-frontend

The live backend admin interface can be accessed here:  
https://momentum-backend-d83acc164707.herokuapp.com/admin/

## Database Schema

The database schema contains the following models with full CRUD capabilities:

### Users (Django built-in)

- Default Django User model for authentication
- Fields: username, password, email, etc.

### Habits

- Core model for habit tracking
- Fields:
  - `owner` (ForeignKey to User)
  - `name` (CharField, max_length=100)
  - `period` (CharField, choices: daily/weekly/monthly)
  - `target` (PositiveIntegerField, default=1)
  - `description` (TextField, optional)
  - `tags` (CharField, optional)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)

### Relationships:

- One User can have many Habits (One-to-Many)
- Habits are owned by a single User

[PLACEHOLDER: If you have additional models like HabitLogs, Comments, etc., document them here]

<h2 id="user-stories">User Stories</h2>

API User Stories for the backend:

1. As an authenticated API user I can create a new habit with required and optional fields
2. As an authenticated API user I can retrieve a list of all my habits
3. As an authenticated API user I can retrieve details of a specific habit
4. As an authenticated API user I can update any of my existing habits
5. As an authenticated API user I can delete any of my habits
6. As an authenticated API user I can filter habits by period
7. As an authenticated API user I can search habits by name, description, or tags
8. As an API user I can register a new account with username and password
9. As an API user I can log in to receive authentication tokens
10. As an authenticated API user I can refresh my access token
11. As an authenticated API user I can log out by clearing stored authentication tokens on the client
12. As an API user I receive appropriate error messages for invalid requests
13. As an API user I can only access my own habits (owner filtering)
14. As a developer I can see clear API documentation through Django REST Framework's browsable API

<h2 id="agile-methodology">Agile Methodology</h2>

<a href="#top">Back to the top.</a>

The Agile Methodology was used to plan this project. This was implemented through Github and the Project Board which can be seen here - <a href="The project board can be viewed here - https://github.com/users/Bear81/projects/8
" target="_blank"> Momentum Backend User Stories</a>

Through the use of the Kanban board in the projects view in Github, the project was divided into sections:

- Todo
- In Progress
- Done

![Kanban board github](documentation/screenshots/github-kanban-board.webp)

Github issues were used to create User Stories and any other fixes or updates for the project. Each User Story had:

- Clear title
- Acceptance criteria
- Labels for priority and categorization
- Assignment to appropriate sprint/milestone

Milestones were used to organise development phases. Core API functionality was prioritised to meet assessment requirements, with additional ideas recorded as future enhancements.

[PLACEHOLDER: Number] enhancement features were not completed and left for further development.

## Testing

<a href="#top">Back to the top.</a>

- Automated Unit testing, Manual testing and validation results can be viewed [HERE](/TESTING.md)

## Bugs

<a href="#top">Back to the top.</a>

- Bugs encountered during development and solutions can be viewed [HERE](/TESTING.md#bugs)

## Technologies Used

<a href="#top">Back to the top.</a>

### Languages

- Python 3.x - Django REST API

### Frameworks, libraries, and Programs

- **Django 4.x**
  - High-level Python web framework
- **Django REST Framework (DRF)**
  - Toolkit for building Web APIs
- **Django REST Framework SimpleJWT**
  - JSON Web Token authentication for DRF
- **django-filter**
  - Reusable Django application for filtering querysets
- **psycopg2**
  - PostgreSQL database adapter for Python
- **dj-database-url**
  - Django utility to utilize DATABASE_URL environment variable
- **python-dotenv**
  - Reads key-value pairs from .env file
- **whitenoise**
  - Simplified static file serving for Python web apps
- **gunicorn**
  - Python WSGI HTTP Server for UNIX
- **django-cors-headers**
  - Django app for handling Cross-Origin Resource Sharing (CORS)
- **Git**
  - Version control system
- **GitHub**
  - Repository hosting service
- **GitPod / VS Code**
  - IDE for development
- **Heroku**
  - Cloud platform for deployment
- **Neon PostgreSQL**
  - PostgreSQL database hosting provided via Code Institute infrastructure

## Project Setup

<a href="#top">Back to the top.</a>

### Initial Setup

1. Use the Code Institute GitPod Full Template to create a new repository, and open it in GitPod.

2. Install Django by using the terminal command:

```bash
pip3 install 'django<5'
```

3. Start the project using the terminal command:

```bash
django-admin startproject momentum .
```

- The dot at the end initializes the project in the current directory.

4. Create a new app called 'habits':

```bash
python manage.py startapp habits
```

5. Install Django REST Framework:

```bash
pip install djangorestframework
```

6. Go to settings.py file and add the newly installed apps:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'habits',
]
```

7. Create an env.py file in the top directory and add to .gitignore

8. In the env.py file add the following:

```python
import os
os.environ["SECRET_KEY"] = "your-secret-key-here"
os.environ["DEV"] = "1"
```

9. In settings.py import the environment variables:

```python
import os
if os.path.exists('env.py'):
    import env

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = 'DEV' in os.environ
```

10. Migrate the database:

```bash
python manage.py migrate
```

11. Create a superuser:

```bash
python manage.py createsuperuser
```

12. Run the development server:

```bash
python manage.py runserver
```

## Deployment

<a href="#top">Back to the top.</a>

### Setting up JSON Web Tokens

1. Install JSON Web Token authentication:

```bash
pip install djangorestframework-simplejwt
```

2. In settings.py, add the JWT authentication to REST_FRAMEWORK settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

3. Configure Simple JWT settings in settings.py:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

4. In the main urls.py file add the JWT token endpoints:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('habits.urls')),
]
```

5. Update requirements.txt:

```bash
pip freeze > requirements.txt
```

### Prepare API for Deployment to Heroku

1. Install required packages for deployment:

```bash
pip install gunicorn
pip install dj-database-url psycopg2
pip install django-cors-headers
pip install whitenoise
```

2. Update requirements.txt:

```bash
pip freeze > requirements.txt
```

3. Create a Procfile in the root directory:

```
release: python manage.py migrate
web: gunicorn momentum.wsgi
```

4. In settings.py, set up allowed hosts:

```python
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST'),
    'localhost',
    '127.0.0.1',
]
```

5. Add CORS headers middleware in settings.py:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

6. Configure CORS allowed origins in settings.py:

```python
if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN'),
    ]
else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://.*\.gitpod\.io$",
        r"^http://localhost:5173$",
        r"^http://localhost:3000$",
    ]

CORS_ALLOW_CREDENTIALS = True
```

7. Configure database settings in settings.py:

```python
import dj_database_url

if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```

8. Configure static files in settings.py:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

9. Update requirements.txt one final time:

```bash
pip freeze > requirements.txt
```

### Deployment to Heroku

1. Log in to Heroku account

2. Click "New" and select "Create new app"

3. Give the app a unique name and choose your region

4. Click "Create app"

5. Navigate to the "Settings" tab

6. Click "Reveal Config Vars" and add the following:
   - `SECRET_KEY`: Your Django secret key
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `ALLOWED_HOSTS`: Backend deployment host
   - `CORS_ALLOWED_ORIGINS`: Frontend deployment URL
   - `CSRF_TRUSTED_ORIGINS`: Frontend and backend deployment URLs
   - `DISABLE_COLLECTSTATIC`: 1 (temporary, remove after first successful deploy)

7. Navigate to the "Deploy" tab

8. In "Deployment method" section, select "GitHub"

9. Search for your repository and click "Connect"

10. In the "Manual deploy" section, select the main branch and click "Deploy Branch"

11. The build log will run. When complete, you will see "Build succeeded"

12. Click "Open App" to view your deployed API

13. Optional: Enable automatic deploys in the "Automatic deploys" section

#### Database Configuration

The project uses a PostgreSQL database hosted via Neon, provided through Code Institute infrastructure.

The database connection is configured using the `DATABASE_URL` environment variable, which is supplied via Heroku config vars. No database credentials are stored in the repository.

## API Endpoints

<a href="#top">Back to the top.</a>

### Authentication Endpoints

| Method | Endpoint                      | Description          | Auth Required |
| ------ | ----------------------------- | -------------------- | ------------- |
| POST   | `/api/v1/auth/register/`      | Register new user    | No            |
| POST   | `/api/v1/auth/token/`         | Obtain JWT tokens    | No            |
| POST   | `/api/v1/auth/token/refresh/` | Refresh access token | No            |

### Habits Endpoints

| Method | Endpoint               | Description            | Auth Required    |
| ------ | ---------------------- | ---------------------- | ---------------- |
| GET    | `/api/v1/habits/`      | List all user's habits | Yes              |
| POST   | `/api/v1/habits/`      | Create new habit       | Yes              |
| GET    | `/api/v1/habits/{id}/` | Retrieve habit details | Yes              |
| PUT    | `/api/v1/habits/{id}/` | Update habit           | Yes (Owner only) |
| PATCH  | `/api/v1/habits/{id}/` | Partial update habit   | Yes (Owner only) |
| DELETE | `/api/v1/habits/{id}/` | Delete habit           | Yes (Owner only) |

### Query Parameters

**Habits List Endpoint** (`/api/v1/habits/`):

- `search`: Search by name, description, or tags
- `period`: Filter by period (daily, weekly, monthly)
- `ordering`: Order results (e.g., `-created_at`)

Example:

```
GET /api/v1/habits/?search=exercise&period=daily&ordering=-created_at
```

## Credits

<a href="#top">Back to the top.</a>

The Code Institute walkthrough DRF_API project was used for the initial setup of this project, with modifications made to suit the Momentum habit tracking requirements.

Additional resources:

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Simple JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django Filter Documentation](https://django-filter.readthedocs.io/)

## Acknowledgements

This project was made possible with the support of:

- Code Institute mentor for guidance and feedback
- Code Institute tutors for technical support
- Code Institute Slack community
- Stack Overflow community for problem-solving

<a href="#top">Back to the top.</a>
