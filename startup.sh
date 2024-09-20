# Custom startup script for Django app on Azure App Service

echo "Running startup.sh:"

echo "[1] Run migrations"
python manage.py migrate

echo "[2] Collect static files"
python manage.py collectstatic

echo "[3] Make 'log' directory"
mkdir log

echo "[4] Run server"
gunicorn backend.wsgi -c ./gunicorn/config.py
