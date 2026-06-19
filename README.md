# Mysity - Django Web Application

A robust, full-featured web application built with Python and the Django web framework. This project implements a modular structure featuring user authentication, management, and a dynamic blogging system.

## 🚀 Features

- **User Management System:** Custom user registration, login, profile handling, and authentication workflows (`user_mangmant` app).
- **Blog Engine:** Dynamic content management, article publishing, and category structures (`blog` app).
- **SEO Optimized:** Built-in dynamic XML sitemaps configuration (`sitemaps.py`).
- **Clean Architecture:** Standard Django architecture with a clean separation of Models, Views, Forms, and Templates.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend Integration:** HTML5, CSS/SCSS Templates, Static files handling
- **Database:** PostgreSQL / SQLite (Configured via Django ORM)

## 📁 Project Structure

Key modules inside this project:
- `mysity/` - Core project settings and URL configurations.
- `blog/` - Managing articles, comments, and blog functionalities.
- `user_mangmant/` - Dedicated app for handling user accounts and management workflows.
- `templates/` - Global HTML layouts and interface components.

## 📦 Installation & Setup

Follow these steps to run the project locally:

1. **Clone the repository:**
```bash
   git clone [https://github.com/mohammadrezaxp/mysity.git](https://github.com/mohammadrezaxp/mysity.git)
## Navigate into the project directory:
   cd mysity
##​Install the dependencies:
   pip install -r requirements.txt
##​Apply database migrations:
   python manage.py migrate
##Run the development server:
   python manage.py runserver


