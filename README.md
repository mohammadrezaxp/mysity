# Mysity

**A Django blog and content-management application with a REST API.**

[![CI](https://github.com/mohammadrezaxp/mysity/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammadrezaxp/mysity/actions/workflows/ci.yml)

[API routes](api/urls.py) · [Models](blog/models.py) · [API tests](api/test_api.py) · [MIT license](LICENSE)

Mysity serves blog content through Django templates and Django REST Framework. Posts support publishing state, categories, tags, and view counts. API consumers can browse published content, authenticate with JWT, and work with post, category, and comment resources.

## Features

- Draft/published posts with slugs, categories, tags, and images.
- Server-rendered pages alongside a REST API.
- Post filtering by `category`, `auther`, and `status`; search by title/content; ordering by publication date or views.
- JWT token issue, refresh, and verification routes.
- Author/staff permission logic and user-dependent post visibility.
- OpenAPI schema, Swagger UI, and ReDoc.
- pytest tests, Docker configuration, and a GitHub Actions workflow.

## Technology

Python 3.11+ · Django 5.2 · Django REST Framework · SimpleJWT · drf-spectacular · SQLite/PostgreSQL · Docker · pytest

See [requirements.txt](requirements.txt) for the actual package versions. Redis and Celery dependencies are present; their presence alone does not establish an active background job or caching workflow.

## Quick start

```bash
git clone https://github.com/mohammadrezaxp/mysity.git
cd mysity
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\Activate.ps1` in PowerShell.

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, generate a unique `SECRET_KEY`, and configure `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL`.

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python manage.py migrate --settings=untitled2.settings
python manage.py createsuperuser --settings=untitled2.settings
python manage.py runserver --settings=untitled2.settings
```

These commands explicitly use `untitled2.settings`, which loads the environment configuration. Plain `manage.py` defaults to `untitled2.setting.dev`; that module shares the environment database and secret key and enables development tooling when DEBUG is true. Use a consistent settings module across migration, server, and test commands.

Open the [site](http://127.0.0.1:8000/), [admin](http://127.0.0.1:8000/admin/), or [API docs](http://127.0.0.1:8000/api/docs/). Create content in the admin, mark a post published, then retrieve it through the API.

## API guide

| Method | Route | Purpose |
| --- | --- | --- |
| GET/POST | `/api/posts/` | Browse visible posts or create a post |
| GET/PUT/PATCH/DELETE | `/api/posts/{id}/` | Retrieve or edit a post, subject to permissions |
| GET/POST | `/api/categories/` | Category resources |
| GET/POST | `/api/comments/` | Comment resources |
| POST | `/api/token/` | Obtain access/refresh tokens |
| POST | `/api/token/refresh/` | Refresh access token |
| POST | `/api/token/verify/` | Verify a token |
| GET | `/api/schema/`, `/api/docs/`, `/api/redoc/` | Schema and interactive documentation |

Examples use Bash/curl:

```bash
curl 'http://127.0.0.1:8000/api/posts/?search=django&ordering=-published_date'

curl -X POST http://127.0.0.1:8000/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"your-user","password":"your-password"}'

curl http://127.0.0.1:8000/api/posts/ \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Post lists use page-number pagination with a default page size of 10. Anonymous readers see published posts whose publication time has arrived and which do not require login. Signed-in readers can also see published members-only posts; authors can preview their own drafts and scheduled posts, and staff can see all posts. RSS, sitemaps, and public discovery widgets only include publicly readable posts. The model/API spelling `auther` is retained for compatibility. It is read-only and always assigned to the authenticated creator. Only the author or staff may edit a post; only staff may change categories. Comment edits belong to the comment author or staff. Comment email addresses are accepted as write-only fields and never returned in post or comment responses.

Create/update posts with `category_ids: [1, 2]` and `tag: ["django", "python"]`. Responses include nested categories and a list of tag names. Rich HTML is sanitized on input and output, including historical database content. Summernote uploads require staff authentication and are limited to 5 MB. Browser logout requires a CSRF-protected POST.

## Project map

```text
api/              Serializers, viewsets, permissions, routes, and API tests
blog/             Content models, template views, feeds, and sitemaps
mysity/           Site pages, contact forms, and supporting models
user_mangmant/    User-management app (existing package name)
untitled2/        Project settings and root URLs
templates/        Server-rendered presentation
```

## Test and container workflows

```bash
python manage.py check --settings=untitled2.settings
pytest -v
```

pytest already selects `untitled2.settings` through [pytest.ini](pytest.ini). Review the [CI history](https://github.com/mohammadrezaxp/mysity/actions) for the current workflow result.

The [Compose configuration](docker-compose.yml) uses PostgreSQL with persistent database and upload volumes. Set a generated `SECRET_KEY` and a strong, URL-safe `POSTGRES_PASSWORD` in `.env`, then run:

```bash
docker compose build web
docker compose up -d db
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
docker compose up -d web
```

Compose is configured for local HTTP on port 8000. For public hosting, configure your actual `ALLOWED_HOSTS`, enable secure cookies and HTTPS redirection, and place the application behind a trusted HTTPS proxy. Serve uploaded media separately; WhiteNoise serves collected static assets. Redis is available as an optional service but no background task workflow is configured.

## Validation and deployment

The regression suite covers post visibility, ownership, category/comment permissions, email privacy, HTML sanitization, login redirects, signup validation, editor uploads, contact identity, and public discovery. CI runs the tests against PostgreSQL, checks migrations and OpenAPI, and builds the Docker image.

```bash
python manage.py makemigrations --check --dry-run --settings=untitled2.settings
python manage.py spectacular --file schema.yml --validate --fail-on-warn --settings=untitled2.settings
```

Production WSGI/ASGI defaults to `untitled2.setting.prod`. It requires explicit `SECRET_KEY` and `ALLOWED_HOSTS`, shares `DATABASE_URL`, disables debug tooling, and defaults to secure cookies and HTTPS redirects. Configure `CSRF_TRUSTED_ORIGINS` for your HTTPS origin. Set the Django Site domain in admin for RSS/sitemap links. Back up the database and uploads before deploying and run `migrate`; existing comments are preserved without an inferred owner, so staff manage them until ownership is established. The prior committed secret must be replaced in any existing deployment.

No live deployment or screenshot gallery is included. Request throttling currently uses each process's local cache; configure a shared cache when scaling across workers. Uploaded media requires a separate web server or object storage in production.

## Contributing and license

Report a reproducible issue or submit a focused change with relevant tests. For private security reports, contact [the maintainer](mailto:m.mahmoudi.xp@gmail.com). Licensed under [MIT](LICENSE).
