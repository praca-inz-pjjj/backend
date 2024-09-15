# Custom startup script for Django app on Azure App Service

echo "Running startup.sh:"

echo "[1] Run migrations"
python manage.py migrate

echo "[2] Collect static files"
python manage.py collectstatic

echo "[3] Run server"
gunicorn --bind=0.0.0.0 --timeout 600 backend.wsgi
