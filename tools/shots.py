import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/')
OUT = sys.argv[2]
USER, EMAIL, PWD = 'estudiante', 'estudiante@example.com', 'Umg-Practica-2026!'

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    pg = b.new_page(viewport={'width': 1100, 'height': 700})

    def shot(name):
        pg.screenshot(path=f'{OUT}/{name}.png')

    pg.goto(f'{BASE}/clientes/')          # sin sesión -> redirige a login
    shot('01_redirect_login')

    pg.goto(f'{BASE}/registro/')
    pg.fill('#id_username', USER)
    pg.fill('#id_email', EMAIL)
    pg.fill('#id_password1', PWD)
    pg.fill('#id_password2', PWD)
    shot('02_registro')
    pg.click('button[type=submit]')
    pg.wait_for_load_state()
    shot('03_inicio_con_sesion')

    pg.goto(f'{BASE}/clientes/')
    for nombre, correo in [('Ana Lopez', 'ana@example.com'), ('Carlos Perez', 'carlos@example.com')]:
        pg.fill('#id_nombre', nombre)
        pg.fill('#id_correo', correo)
        pg.click('button:has-text("Guardar cliente")')
        pg.wait_for_load_state()
    shot('04_clientes_lista')

    pg.click('button:has-text("Salir")')
    pg.wait_for_load_state()
    pg.goto(f'{BASE}/clientes/')
    shot('05_logout_redirect')
    b.close()
print('done')
