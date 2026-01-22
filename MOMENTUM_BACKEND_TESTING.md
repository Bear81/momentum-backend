<a id="top"></a>

# Momentum Backend Testing

This document outlines backend testing carried out for the **Momentum** Django REST Framework API. Testing was performed throughout development using:

- Django’s built-in test runner (limited automated tests where appropriate)
- The **DRF Browsable API** for authenticated/unauthenticated endpoint verification
- Manual endpoint testing (e.g. browser devtools / REST client) against both local and deployed environments

The primary focus for PP5 is demonstrating correct authentication, CRUD behaviour, ownership enforcement, and secure deployment configuration.

---

## Test Environments

### Local Development

- Backend: Django + DRF (local server)
- Database: PostgreSQL (local / dev configuration)

### Production (Deployed)

- Backend (Heroku): `https://momentum-backend-d83acc164707.herokuapp.com/`
- Admin: `https://momentum-backend-d83acc164707.herokuapp.com/admin/`

> Note: The backend root URL returns **404** by design. The application is **API-only**, and all functionality is exposed via `/api/v1/` endpoints.

---

## Automated Testing (Limited)

Automated testing was implemented to validate basic model and permission behaviours during development. The main purpose for assessment evidence is **manual endpoint testing** and **frontend integration testing** (see frontend testing document).

### Running Tests

```bash
python manage.py test
```

---

<a href="#top">Back to the top</a>

# Manual API Testing

Manual testing focused on validating:

- Authentication endpoints
- Habit CRUD operations
- Ownership enforcement (users can only access and modify their own habits)
- Expected error responses for invalid data and unauthorised requests

All endpoints below assume the API prefix:

- `/api/v1/`

---

## Authentication Endpoints

| Test Case | Endpoint                      | Method | Steps                                | Expected Result                        | Actual Result | Status  |
| --------- | ----------------------------- | ------ | ------------------------------------ | -------------------------------------- | ------------- | ------- |
| AT01      | `/api/v1/auth/register/`      | POST   | Submit valid username + password     | 201 Created, user created              | As expected   | ✅ Pass |
| AT02      | `/api/v1/auth/register/`      | POST   | Submit missing required field(s)     | 400 Bad Request with validation errors | As expected   | ✅ Pass |
| AT03      | `/api/v1/auth/token/`         | POST   | Submit valid credentials             | 200 OK with access + refresh tokens    | As expected   | ✅ Pass |
| AT04      | `/api/v1/auth/token/`         | POST   | Submit invalid credentials           | 401 Unauthorized                       | As expected   | ✅ Pass |
| AT05      | `/api/v1/auth/token/refresh/` | POST   | Submit valid refresh token           | 200 OK with new access token           | As expected   | ✅ Pass |
| AT06      | `/api/v1/auth/token/refresh/` | POST   | Submit invalid/expired refresh token | 401 Unauthorized                       | As expected   | ✅ Pass |

> Logout behaviour: **client-side** only (frontend clears stored tokens). No server-side token blacklisting/invalidation is implemented.

---

## Habits CRUD

| Test Case | Endpoint               | Method    | Steps                                       | Expected Result                        | Actual Result | Status  |
| --------- | ---------------------- | --------- | ------------------------------------------- | -------------------------------------- | ------------- | ------- |
| HC01      | `/api/v1/habits/`      | GET       | Request without auth                        | 401 Unauthorized                       | As expected   | ✅ Pass |
| HC02      | `/api/v1/habits/`      | GET       | Request with valid JWT                      | 200 OK, list of user-owned habits      | As expected   | ✅ Pass |
| HC03      | `/api/v1/habits/`      | POST      | Create habit with valid payload (auth)      | 201 Created, habit returned            | As expected   | ✅ Pass |
| HC04      | `/api/v1/habits/`      | POST      | Create habit with missing required field(s) | 400 Bad Request with validation errors | As expected   | ✅ Pass |
| HC05      | `/api/v1/habits/<id>/` | PUT/PATCH | Update owned habit (auth)                   | 200 OK, habit updated                  | As expected   | ✅ Pass |
| HC06      | `/api/v1/habits/<id>/` | PUT/PATCH | Update without auth                         | 401 Unauthorized                       | As expected   | ✅ Pass |
| HC07      | `/api/v1/habits/<id>/` | DELETE    | Delete owned habit (auth)                   | 204 No Content                         | As expected   | ✅ Pass |
| HC08      | `/api/v1/habits/<id>/` | DELETE    | Delete without auth                         | 401 Unauthorized                       | As expected   | ✅ Pass |

---

## Ownership & Permissions

Ownership enforcement is validated both manually and through behaviour observed in frontend integration.

| Test Case | Scenario                                              | Steps                                                              | Expected Result                                              | Actual Result | Status  |
| --------- | ----------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ | ------------- | ------- |
| OP01      | User A cannot view User B’s habit via detail endpoint | Login as User A, request `/habits/<id>/` for habit owned by User B | 404 Not Found (or 403 Forbidden depending on implementation) | As expected   | ✅ Pass |
| OP02      | User A cannot update User B’s habit                   | Login as User A, attempt PUT/PATCH on User B’s habit               | 404 Not Found (or 403 Forbidden)                             | As expected   | ✅ Pass |
| OP03      | User A cannot delete User B’s habit                   | Login as User A, attempt DELETE on User B’s habit                  | 404 Not Found (or 403 Forbidden)                             | As expected   | ✅ Pass |
| OP04      | Admin can view all habits via Django admin            | Log into `/admin/` as admin                                        | Admin can view/manage all records                            | As expected   | ✅ Pass |

> Implementation note (CBV pattern): ownership is enforced server-side by scoping querysets to the authenticated user (e.g. filtering by `owner=request.user`) and/or applying object-level permission checks.

---

## Validation & Error Handling (Backend)

| Test Case | Scenario               | Steps                                        | Expected Result | Actual Result | Status  |
| --------- | ---------------------- | -------------------------------------------- | --------------- | ------------- | ------- |
| VE01      | Invalid `period` value | POST habit with period not in allowed values | 400 Bad Request | As expected   | ✅ Pass |
| VE02      | Invalid numeric target | POST habit with target <= 0                  | 400 Bad Request | As expected   | ✅ Pass |
| VE03      | Missing required field | POST habit missing name                      | 400 Bad Request | As expected   | ✅ Pass |
| VE04      | Malformed JSON         | POST invalid JSON body                       | 400 Bad Request | As expected   | ✅ Pass |

---

## Production Configuration Verification

| Check                 | Expected                               | Result   |
| --------------------- | -------------------------------------- | -------- |
| DEBUG disabled        | `DEBUG=False` in production            | Verified |
| Secrets not committed | No API keys / DB creds in repo         | Verified |
| Env vars used         | Config supplied via Heroku config vars | Verified |
| CORS restricted       | Frontend origin allowed; not wildcard  | Verified |
| Permissions enforced  | Ownership enforced server-side         | Verified |

---

## Bugs Fixed (Backend)

The following backend-related issues were identified and resolved during development:

1. **Ownership enforcement**
   - Fixed by ensuring habit queries are scoped to the authenticated user (users cannot access or modify other users’ data).

2. **Deployment configuration alignment**
   - Confirmed environment variables and security settings (`DEBUG=False`, allowed origins, and host configuration) were correctly applied in production.

---

## Notes on Database / Migrations

During development, database changes were managed using Django migrations. When schema updates required resetting development data, migrations were handled carefully to avoid inconsistent states.

Production migrations were applied cautiously to avoid data loss or downtime.

---

<a href="#top">Back to the top</a>
