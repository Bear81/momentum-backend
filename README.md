# Momentum Backend (Django REST Framework)

Live API: [https://momentum-backend-d83acc164707.herokuapp.com](https://momentum-backend-d83acc164707.herokuapp.com)

Frontend Repository: [https://github.com/Bear81/momentum-frontend](https://github.com/Bear81/momentum-frontend)

---

## Introduction

This is the **backend API** for **Momentum**, a full-stack habit tracking application built for Code Institute’s Portfolio Project 5 (resubmission).  
It is built using **Django REST Framework**, providing secure authentication, CRUD endpoints for habits, and user profile management.

The API supports the deployed React frontend hosted on Heroku.

---

## Database Schema

**Models include:**
- **User** (via Django AllAuth)
- **Profile** (OneToOne relationship with User)
- **Habit** (tracks title, frequency, completion, timestamps)

![Database ERD Placeholder](documentation/database-schema.webp)

---

## Key Features

| Feature | Description |
|----------|-------------|
| **CRUD API** | Endpoints for creating, reading, updating, and deleting habits. |
| **Authentication** | Secure user login, logout, and registration via dj-rest-auth. |
| **Permissions** | Users can only access and modify their own habits. |
| **Pagination & Filtering** | Paginated and filterable API responses. |
| **Deployment Ready** | Configured for Heroku with PostgreSQL database. |

---

## Technologies Used

### Languages & Frameworks
- Python 3.12
- Django 5 / Django REST Framework

### Libraries & Packages
- dj-rest-auth / django-allauth (authentication)
- django-cors-headers
- psycopg2 / dj-database-url (PostgreSQL integration)
- gunicorn (WSGI server)
- Cloudinary (optional image storage)
- PyJWT / SimpleJWT (token handling)

### Other Tools
- Git / GitHub for version control
- Heroku for deployment
- ElephantSQL for database hosting

---

## Testing

### Automated Testing

Automated tests implemented via Django’s built-in `TestCase` class.

| File | Description |
|------|--------------|
| `test_models.py` | Validates model creation and string representations. |
| `test_views.py` | Tests CRUD API endpoints for authenticated users. |

All automated tests ran successfully using `python manage.py test`.

---

### Manual Testing

| Feature | Expected Result | Actual Result | Pass |
|----------|----------------|----------------|------|
| **Register User** | Creates new user via `/dj-rest-auth/registration/`. | Works as expected. | ✅ |
| **Login User** | Returns token cookies. | Works as expected. | ✅ |
| **Logout User** | Clears authentication cookies. | Works as expected. | ✅ |
| **Create Habit** | POST creates new habit record. | Works as expected. | ✅ |
| **Edit Habit** | PATCH/PUT updates habit fields. | Works as expected. | ✅ |
| **Delete Habit** | DELETE removes record. | Works as expected. | ✅ |
| **Permission Check** | Other users cannot modify foreign habits. | Works as expected. | ✅ |
| **Pagination** | Returns 10 results per page. | Works as expected. | ✅ |
| **Validation** | Missing required field returns 400 error. | Works as expected. | ✅ |

---

## Deployment

Deployed on **Heroku** with a connected **PostgreSQL** database via **ElephantSQL**.

### Deployment Steps
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. Add allowed hosts and environment variables:  
   ```python
   ALLOWED_HOSTS = ['momentum-backend-d83acc164707.herokuapp.com', 'localhost']
   ```
3. Set up PostgreSQL in Heroku → Resources → Add-ons → “Heroku Postgres”.  
4. Add `DATABASE_URL` and `SECRET_KEY` to Heroku Config Vars.  
5. Set `DEBUG=False` for production.  
6. Push changes to GitHub and trigger Heroku auto-deploy.  

---

## Bugs & Fixes

| Bug | Fix |
|-----|-----|
| `dj-rest-auth` logout bug | Custom logout route added to clear cookies. |
| Email registration serializer error | Updated RegisterSerializer import and settings. |
| Token authentication conflict | SessionAuthentication enabled for browsable API. |

---

## Credits

- Built from the Code Institute DRF API walkthrough.  
- Deployment steps follow FoodSnap backend example by Art Cuddy.  

---

## Acknowledgements

Thanks to Code Institute mentors, Slack community, and my family for their support throughout the course.

---
