# Mysity — Django Content Management & REST API Platform

[![CI](https://github.com/mohammadrezaxp/mysity/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammadrezaxp/mysity/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-orange.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Project Overview

**Mysity** is a robust, production-ready Django-based content management and blog platform enhanced with a full-featured Django REST Framework (DRF) API. Designed as a strong junior-to-mid level backend portfolio project, it demonstrates clean architecture, secure authentication, robust database querying, automated testing, and containerized deployment readiness.

---

## Key Features

- **Advanced Blog CMS**: Draft/published post states, unique slugs, view counters, categorization, and tag management.
- **RESTful API (DRF)**: Fully documented endpoints supporting pagination, filtering (`django-filter`), search, and ordering.
- **JWT & Session Authentication**: Secure dual-authentication support using `SimpleJWT` alongside standard session auth.
- **Role-Based Permissions**: Granular object-level permissions ensuring authors manage only their own posts/comments, while staff moderate content.
- **Automated Testing**: Comprehensive test suite built with `pytest` and `pytest-django`.
- **Database Flexibility**: Native support for SQLite (local development) and PostgreSQL (production via environment config).
- **Containerization**: Fully configured `Dockerfile` and `docker-compose.yml` for multi-service orchestration (Web, PostgreSQL, Redis).
- **API Documentation**: Interactive API docs powered by `drf-spectacular` (Swagger UI & ReDoc).

---

## Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.11+ |
| **Framework** | Django 5.2 |
| **API** | Django REST Framework, SimpleJWT, DRF Spectacular |
| **Database** | PostgreSQL / SQLite |
| **Caching / Broker** | Redis |
| **Testing** | Pytest, Pytest-Django |
| **Deployment** | Docker, Gunicorn |

---

## Architecture

The project follows standard Django app modularization:
```
mysity/
├── api/              # DRF serializers, viewsets, permissions, and API tests
├── blog/             # Core blog models, views, feeds, and sitemaps
├── mysity/           # Static pages, contact forms, and utilities
├── user_mangmant/    # Custom user management and authentication
├── untitled2/        # Project settings, WSGI, ASGI, and root URL conf
└── templates/        # HTML templates for server-rendered views
```

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/posts/` | List published posts (filterable/searchable) | No |
| `GET` | `/api/posts/{id}/` | Retrieve post detail | No |
| `POST` | `/api/posts/` | Create a new post | Yes (Author/Staff) |
| `GET` | `/api/categories/` | List categories | No |
| `GET` | `/api/comments/` | List comments | No |
| `POST` | `/api/comments/` | Add a comment | Yes |
| `POST` | `/api/token/` | Obtain JWT pair (Login) | No |
| `POST` | `/api/token/refresh/` | Refresh JWT access token | No |
| `GET` | `/api/docs/` | Swagger UI documentation | No |
| `GET` | `/api/redoc/` | ReDoc documentation | No |

---

## Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammadrezaxp/mysity.git
   cd mysity
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your local configurations:
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Testing

Run the automated test suite using `pytest`:
```bash
pytest -v
```

---

## Author

**Mohammadreza**
- GitHub: [mohammadrezaxp](https://github.com/mohammadrezaxp)
