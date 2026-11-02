# Contexto del proyecto (para continuar en otro chat)

## Tarea (UMG, Desarrollo Web, 10º semestre)
1. Replicar la guía `README-DJANGO-PRACTICA-1.md` (Descargas): Django + MySQL, autenticación (registro/login/logout/recuperar) y módulo Clientes protegido por sesión.
2. Entregar un PDF con: carátula, evidencia de ejecución local (terminal), evidencia del despliegue (PythonAnywhere, DigitalOcean, Railway u otro) y enlace público para validar.

## Estado
- HECHO: proyecto completo en esta carpeta, probado en local contra MySQL (flujo completo OK).
- HECHO: archivos de despliegue (`requirements.txt`, `Procfile`, `.gitignore`, `DESPLIEGUE.md`) y `settings.py` leyendo variables de entorno (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DB_*` o `MYSQL*` de Railway, `RAILWAY_PUBLIC_DOMAIN`).
- HECHO: PDF generado `Entregable-Django-MySQL.pdf` (carátula + evidencia local). Secciones 2 y 3 (despliegue y URL) dicen PENDIENTE; carátula con marcadores `[Nombre del estudiante]` y `[Carné]`.
- PENDIENTE (lo hace el usuario; Claude no puede crear cuentas ni meter credenciales):
  1. Subir la carpeta a GitHub y desplegar en Railway con MySQL (pasos en `DESPLIEGUE.md`). Guardar capturas del proceso en `evidencia/deploy/`.
  2. Regenerar el PDF con nombre, carné, URL y capturas.
  3. Verificar la URL pública: `/registro/` y luego `/clientes/`.

## Entorno local
- Windows, Python 3.14, Django 6.1.2, PyMySQL. Entorno virtual del proyecto: `venv/`.
- MySQL: XAMPP (MariaDB 10.4.32). Si está apagado: `Start-Process C:\xampp\mysql\bin\mysqld.exe -ArgumentList '--defaults-file=C:\xampp\mysql\bin\my.ini','--standalone' -WindowStyle Hidden`. Base `django_db`, usuario `root` sin contraseña.
- Django 6.1 exige MariaDB 10.11+, por eso en local se usa `ALLOW_OLD_MARIADB=1` (parche en `nameproject/__init__.py`, desactiva `RETURNING`). NO definir en producción.
- Arrancar local (PowerShell):
  `$env:ALLOW_OLD_MARIADB='1'; .\venv\Scripts\python.exe manage.py runserver`
- Nota Django 6.1: el correo se configura con `MAILERS` (ya viene en consola por defecto); la guía menciona `EMAIL_BACKEND`, que no hizo falta.

## Herramientas de evidencia
- `C:\pwenv\` : venv aparte (ruta corta, la larga rompe `greenlet`) con playwright, pillow, reportlab, pymupdf. Si no existe: `py -m venv C:\pwenv; C:\pwenv\Scripts\python.exe -m pip install playwright pillow reportlab pymupdf`.
- `tools/shots.py <BASE_URL> <carpeta_salida>`: recorre el flujo en Chrome y guarda capturas (usuario de prueba `estudiante`; la contraseña está dentro del script). Sirve también contra la URL desplegada, p. ej. `C:\pwenv\Scripts\python.exe tools\shots.py https://TU-APP evidencia\deploy`.
- `tools/build_pdf.py --nombre ... --carnet ... --url ... --deploy-dir evidencia/deploy` regenera el PDF.
- `evidencia/`: `migrate.txt`, `mysql_tablas.txt`, `runserver_err.txt` (logs) y `local/*.png` (capturas locales).

## Estructura
`manage.py`, `nameproject/` (settings, urls, views, forms), `clientes/` (modelo Cliente, form, vista, urls), `templates/` (base, home, registration/*, clientes/create.html).
