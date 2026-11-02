# Despliegue en Railway (Django + MySQL)

1. Subir esta carpeta a un repositorio de GitHub (`venv/` y `evidencia/` ya están en `.gitignore`).
2. En https://railway.com: **New Project → Deploy from GitHub repo** y elegir el repositorio.
3. En el mismo proyecto: **+ New → Database → Add MySQL**.
4. En el servicio web → **Variables**:
   - `DEBUG` = `False`
   - `SECRET_KEY` = una cadena larga aleatoria
   - Referencias al MySQL (Add Reference): `MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`
5. Servicio web → **Settings → Networking → Generate Domain**. Railway define `RAILWAY_PUBLIC_DOMAIN`, que `settings.py` ya usa para `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`.
6. El `Procfile` ejecuta `migrate`, `collectstatic` y `gunicorn` en cada despliegue.
7. Abrir el dominio generado, registrar un usuario y guardar un cliente.

No se define `ALLOW_OLD_MARIADB`: ese ajuste es solo para el MariaDB 10.4 de XAMPP en local.
