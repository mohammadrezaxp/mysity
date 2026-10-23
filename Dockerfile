FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home appuser && mkdir -p /app/media /app/staticfiles && chown -R appuser:appuser /app
USER appuser
RUN DJANGO_SETTINGS_MODULE=untitled2.setting.prod SECRET_KEY=build-placeholder-only ALLOWED_HOSTS=localhost python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn","untitled2.wsgi:application","--bind","0.0.0.0:8000","--workers","3"]
