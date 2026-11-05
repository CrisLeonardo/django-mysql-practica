#!/bin/bash
# Despliegue en PythonAnywhere. Ejecutar en una consola Bash de la cuenta:
#   bash <(curl -s https://raw.githubusercontent.com/CrisLeonardo/django-mysql-practica/main/tools/pythonanywhere_setup.sh)
#
# Requisitos previos (en el sitio web):
#   - Databases: haber definido la contraseña de MySQL.
#   - Account > API Token: haber creado un token (la consola lo expone como $API_TOKEN).
set -e

REPO=https://github.com/CrisLeonardo/django-mysql-practica.git
ME=$(whoami)
DOMAIN="$(echo "$ME" | tr 'A-Z' 'a-z').pythonanywhere.com"
DBHOST="$ME.mysql.pythonanywhere-services.com"
DBNAME="$ME\$django_db"
APP=$HOME/django-mysql-practica
API="https://www.pythonanywhere.com/api/v0/user/$ME"

if [ -z "$API_TOKEN" ]; then
  echo "Falta API_TOKEN: crea el token en Account > API Token y abre una consola nueva."; exit 1
fi

PY=""
for v in 3.13 3.12; do command -v python$v >/dev/null && PY=python$v && break; done
[ -n "$PY" ] || { echo "No hay Python 3.12+ en esta cuenta (Django 6.1 lo necesita)."; exit 1; }
PYAPI=python$(echo "${PY#python}" | tr -d .)
echo "==> Usando $PY ($PYAPI) para $DOMAIN"

read -r -s -p "Contraseña de MySQL (la que pusiste en Databases): " MYSQL_PWD; echo
export MYSQL_PWD

echo "==> Creando la base $DBNAME"
mysql -h "$DBHOST" -u "$ME" -e "CREATE DATABASE IF NOT EXISTS \`$DBNAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "==> Código y entorno virtual"
if [ -d "$APP/.git" ]; then git -C "$APP" pull -q; else git clone -q "$REPO" "$APP"; fi
[ -d "$HOME/venv" ] || $PY -m venv "$HOME/venv"
"$HOME/venv/bin/pip" install -q --upgrade pip
"$HOME/venv/bin/pip" install -q -r "$APP/requirements.txt"

echo "==> Archivo .env"
SECRET=$("$HOME/venv/bin/python" -c "import secrets;print(secrets.token_urlsafe(50))")
cat > "$APP/.env" <<EOF
SECRET_KEY=$SECRET
DEBUG=False
ALLOWED_HOSTS=$DOMAIN
CSRF_TRUSTED_ORIGINS=https://$DOMAIN
ALLOW_OLD_MARIADB=1
DB_NAME=$DBNAME
DB_USER=$ME
DB_PASSWORD=$MYSQL_PWD
DB_HOST=$DBHOST
DB_PORT=3306
EOF
chmod 600 "$APP/.env"

echo "==> Migraciones y estáticos"
cd "$APP"
"$HOME/venv/bin/python" manage.py migrate --noinput
"$HOME/venv/bin/python" manage.py collectstatic --noinput

echo "==> Web app"
curl -s -X POST -H "Authorization: Token $API_TOKEN" \
  -d "domain_name=$DOMAIN" -d "python_version=$PYAPI" "$API/webapps/" >/dev/null || true
curl -s -X PATCH -H "Authorization: Token $API_TOKEN" \
  -d "source_directory=$APP" -d "virtualenv_path=$HOME/venv" "$API/webapps/$DOMAIN/" >/dev/null
curl -s -X POST -H "Authorization: Token $API_TOKEN" \
  -d "url=/static/" -d "path=$APP/staticfiles" "$API/webapps/$DOMAIN/static_files/" >/dev/null || true

WSGI="/var/www/$(echo "$DOMAIN" | tr . _)_wsgi.py"
cat > "$WSGI" <<EOF
import os
import sys

path = '$APP'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nameproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF

curl -s -X POST -H "Authorization: Token $API_TOKEN" "$API/webapps/$DOMAIN/reload/" >/dev/null
echo
echo "Listo: https://$DOMAIN/registro/"
