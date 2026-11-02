import os

import pymysql

pymysql.install_as_MySQLdb()

# Solo para desarrollo local con XAMPP (MariaDB 10.4): Django 6.1 exige 10.11+.
# Se activa con la variable de entorno ALLOW_OLD_MARIADB=1; en producción no aplica.
if os.environ.get('ALLOW_OLD_MARIADB') == '1':
    from django.db.backends.mysql.features import DatabaseFeatures

    DatabaseFeatures.minimum_database_version = property(lambda self: (10, 4))
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
