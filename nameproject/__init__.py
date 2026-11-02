import os

import pymysql

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
