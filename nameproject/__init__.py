import os
from pathlib import Path

import pymysql

# Variables desde un archivo .env (usado en PythonAnywhere); no pisa las ya definidas.
# Se carga aquí, antes que settings.py, porque el ajuste de más abajo se lee al importar.
_env_file = Path(__file__).resolve().parent.parent / '.env'
if _env_file.exists():
    for _line in _env_file.read_text(encoding='utf-8').splitlines():
        _key, _sep, _value = _line.partition('=')
        if _sep and not _line.lstrip().startswith('#'):
            os.environ.setdefault(_key.strip(), _value.strip())

pymysql.install_as_MySQLdb()

# Django 6.1 exige MariaDB 10.11+ / MySQL 8.4+. XAMPP trae MariaDB 10.4 y PythonAnywhere
# MySQL 8.0, así que en esos entornos se activa con la variable ALLOW_OLD_MARIADB=1.
if os.environ.get('ALLOW_OLD_MARIADB') == '1':
    from django.db.backends.mysql.features import DatabaseFeatures

    DatabaseFeatures.minimum_database_version = property(
        lambda self: (10, 4) if self.connection.mysql_is_mariadb else (8, 0)
    )
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
