# Mysity - Django Web Application

A robust, full-featured web application built with Python and the Django web framework. This project implements a modular structure featuring user authentication, management, and a dynamic blogging system.

## 🚀 Features

- **User Management System:** Custom user registration, login, profile handling, and authentication workflows.
- **Blog Engine:** Dynamic content management, article publishing, categories, tags, and comments.
- **SEO Optimized:** Built-in dynamic XML sitemaps for search engine visibility.
- **Contact System:** Ticket-based contact form for user inquiries.
- **RSS Feed:** Built-in RSS feed for blog posts.
- **Clean Architecture:** Standard Django structure with Models, Views, Forms, and Templates.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django 5.x |
| Database | PostgreSQL / SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Tools | django-summernote, django-captcha, django-taggit |

## 📁 Project Structure

```
untitled2/
├── mysity/              # Core project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── forms.py
├── blog/                # Blog app
│   ├── models.py        # Post, Category, Tag, Comment
│   ├── views.py         # Blog views
│   ├── urls.py
│   └── templates/
├── user_manage/         # User authentication app
│   ├── views.py         # Login, Logout, Signup
│   └── urls.py
├── templates/            # Global templates
│   ├── base.html
│   ├── blog/
│   └── mysity/
└── manage.py
```

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/mohammadrezaxp/mysity.git
cd mysity
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 🔑 Key URLs

| URL | Description |
|-----|-------------|
| `/ref/home/` | Home page |
| `/ref/contact/` | Contact form |
| `/ref/about/` | About page |
| `/ref/user_manage/login/` | User login |
| `/ref/user_manage/sing_up/` | User registration |
| `/blog/` | Blog home |
| `/blog/<id>/` | Single post |
| `/admin/` | Admin panel |
| `/summernote/` | WYSIWYG editor |

## 📝 License

This project is open-source and available for personal and commercial use.