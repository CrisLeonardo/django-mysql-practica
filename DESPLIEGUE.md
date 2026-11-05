# Despliegue: Render (app) + Aiven (MySQL)

## 1. Base de datos en Aiven (gratis, sin tarjeta)
1. Crear cuenta en https://console.aiven.io/signup y un servicio **MySQL** con el plan **Free**.
2. Cuando esté en *Running*, en la pestaña **Overview** copiar: Host, Port, User, Password y Database name.
3. Descargar el **CA certificate** (`ca.pem`) de esa misma página.

## 2. App en Render (plan gratis)
1. Crear cuenta en https://render.com (con GitHub).
2. Abrir https://dashboard.render.com/blueprint/new?repo=https://github.com/CrisLeonardo/django-mysql-practica
   (lee `render.yaml`).
3. Rellenar `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` con los datos de Aiven.
4. En el servicio → **Environment → Secret Files** → agregar `ca.pem` con el contenido del certificado.
5. Desplegar (*Manual Deploy → Deploy latest commit*). Render asigna `https://<nombre>.onrender.com`;
   `settings.py` lo toma de `RENDER_EXTERNAL_HOSTNAME`.
6. Abrir `/registro/`, crear un usuario y guardar un cliente en `/clientes/`.

Notas: el plan gratis de Render duerme tras 15 min sin tráfico (la primera visita tarda ~1 min).
`ALLOW_OLD_MARIADB=1` solo es necesario porque Aiven usa MySQL 8.0 y Django 6.1 pide 8.4+.

## Alternativa: Railway
Ver `railway.json` y `Procfile`; requiere plan de pago (la prueba gratuita expiró).
