# Mysity - Full-Stack Blog Platform 🌐

![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> A production-ready blog platform built with Django 5.x featuring a modern UI, user authentication, rich content management, and SEO optimization.

---

## 🔥 What I Built

- **User Authentication System** — Complete login, logout, registration with session management
- **Blog Engine** — Full CRUD operations with categories, tags, and author management
- **Comments System** — Authenticated users can leave comments on posts
- **WYSIWYG Editor** — Rich text editor powered by Django Summernote
- **SEO Optimized** — Dynamic XML sitemaps for search engines
- **RSS Feed** — Built-in RSS feed for blog subscribers
- **Responsive Design** — Modern UI with smooth animations
- **CAPTCHA Protection** — Bot protection on forms

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Django 5.x | Backend Framework |
| PostgreSQL / SQLite | Database |
| HTML5 / CSS3 | Frontend |
| django-summernote | WYSIWYG Editor |
| django-taggit | Tagging System |
| django-captcha | Bot Protection |
| django-debug-toolbar | Development Tools |

## 📁 Project Structure

```
mysity/
├── mysity/              # Core Django settings
├── blog/                # Blog app (models, views, templates)
├── user_manage/         # Authentication app
├── templates/           # Global templates
├── requirements.txt     # Dependencies
└── manage.py
```

## 🚀 Key Features Demo

| Feature | Screenshot |
|---------|------------|
| Home Page | ![Home](docs/screenshots/home.png) |
| Blog Post | ![Post](docs/screenshots/post.png) |
| Login | ![Login](docs/screenshots/login.png) |
| Admin Panel | ![Admin](docs/screenshots/admin.png) |

## 📦 Installation

```bash
# Clone the project
git clone https://github.com/mohammadrezaxp/mysity.git
cd mysity

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 🔗 Important URLs

| Page | URL |
|------|-----|
| Home | `/ref/home/` |
| Blog | `/blog/` |
| Login | `/ref/user_manage/login/` |
| Register | `/ref/user_manage/sing_up/` |
| Contact | `/ref/contact/` |
| Admin | `/admin/` |

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ by [mohammadrezaxp](https://github.com/mohammadrezaxp)**