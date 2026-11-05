"""Genera el PDF entregable. Uso:

  python tools/build_pdf.py --nombre "Tu Nombre" --carnet "0000-00-0000" \
      --url "https://tu-app.up.railway.app" --deploy-dir evidencia/deploy

--deploy-dir: carpeta con capturas (png/jpg) del proceso de despliegue.
Sin --url ni capturas, la sección de despliegue queda marcada como pendiente.
"""
import argparse
from datetime import date
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image as RLImage, PageBreak, Paragraph,
                                Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle)

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'septiembre', 'octubre', 'noviembre', 'diciembre']
ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / 'evidencia'

ap = argparse.ArgumentParser()
ap.add_argument('--nombre', default='[Nombre del estudiante]')
ap.add_argument('--carnet', default='[Carné]')
ap.add_argument('--url', default='')
ap.add_argument('--deploy-dir', default='')
ap.add_argument('--out', default=str(ROOT / 'Entregable-Django-MySQL.pdf'))
a = ap.parse_args()

ss = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=ss['Heading1'], fontSize=18, spaceAfter=10)
H2 = ParagraphStyle('H2', parent=ss['Heading2'], fontSize=13, spaceBefore=10, spaceAfter=6)
P = ParagraphStyle('P', parent=ss['BodyText'], fontSize=10.5, leading=14)
CAP = ParagraphStyle('CAP', parent=P, fontSize=9, textColor=colors.grey, spaceAfter=10)
CENTER = ParagraphStyle('C', parent=P, alignment=1, fontSize=13, leading=20)
TITLE = ParagraphStyle('T', parent=ss['Title'], fontSize=26, leading=32)
CODE = ParagraphStyle('CODE', fontName='Courier', fontSize=7.5, leading=9.2,
                      textColor=colors.HexColor('#e6e6e6'))

story = []


def img(path, width=15.5 * cm):
    w, h = Image.open(path).size
    return RLImage(str(path), width=width, height=width * h / w)


def term(text, limit=60):
    lines = text.strip().splitlines()
    if len(lines) > limit:
        lines = lines[:limit // 2] + ['  [...]'] + lines[-limit // 2:]
    box = Table([[Preformatted('\n'.join(l[:118] for l in lines), CODE)]], colWidths=[17 * cm])
    box.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e1e1e')),
                             ('LEFTPADDING', (0, 0), (-1, -1), 6),
                             ('TOPPADDING', (0, 0), (-1, -1), 6),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(box)
    story.append(Spacer(1, 8))


def read(name):
    p = EV / name
    if not p.exists():
        return ''
    raw = p.read_bytes()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return raw.decode('utf-16', errors='replace')
    return raw.decode('utf-8', errors='replace')


# ---- Carátula
story += [Spacer(1, 3 * cm),
          Paragraph('Universidad Mariano Gálvez de Guatemala', CENTER),
          Paragraph('Desarrollo Web — Décimo Semestre', CENTER),
          Spacer(1, 2 * cm),
          Paragraph('Práctica: Deployment de aplicación Python Django con MySQL', TITLE),
          Spacer(1, 1 * cm),
          Paragraph('Autenticación (registro, login, logout y recuperación de contraseña)<br/>'
                    'y módulo de clientes protegido por sesión', CENTER),
          Spacer(1, 3 * cm),
          Paragraph(f'<b>Estudiante:</b> {a.nombre}', CENTER),
          Paragraph(f'<b>Carné:</b> {a.carnet}', CENTER),
          Paragraph(f'<b>Fecha:</b> {date.today().day} de {MESES[date.today().month - 1]} de {date.today().year}', CENTER),
          PageBreak()]

# ---- Local
story += [Paragraph('1. Evidencia del proyecto en entorno local', H1),
          Paragraph('Stack: Python 3.14, Django 6.1.2, PyMySQL, MySQL/MariaDB (XAMPP), Bootstrap 5.', P),
          Paragraph('1.1 Creación del proyecto y migraciones (terminal)', H2),
          Paragraph('Comandos: <font face="Courier">django startproject nameproject .</font>, '
                    '<font face="Courier">startapp clientes</font>, '
                    '<font face="Courier">makemigrations</font> y <font face="Courier">migrate</font> '
                    'contra la base <font face="Courier">django_db</font> en MySQL.', P)]
term(read('migrate.txt'), 40)
story += [Paragraph('1.2 Tablas creadas en MySQL', H2)]
term(read('mysql_tablas.txt'), 40)
story += [Paragraph('1.3 Servidor en ejecución (runserver)', H2),
          Paragraph('Registro de peticiones: acceso sin sesión redirige a login (302), registro, '
                    'alta de clientes por POST y logout.', P)]
term(read('runserver_err.txt'), 40)
story.append(PageBreak())

story.append(Paragraph('1.4 Capturas de la aplicación', H2))
captions = [
    ('01_redirect_login', '/clientes/ sin sesión redirige a /login/ (protección con @login_required).'),
    ('02_registro', 'Pantalla de registro de usuario.'),
    ('03_inicio_con_sesion', 'Inicio tras registrarse: sesión iniciada.'),
    ('04_clientes_lista', 'Alta de clientes y listado leído desde MySQL.'),
    ('05_logout_redirect', 'Tras pulsar «Salir», /clientes/ vuelve a pedir login.'),
]
for n, c in captions:
    f = EV / 'local' / f'{n}.png'
    if f.exists():
        story += [img(f, 13 * cm), Paragraph(c, CAP)]
story.append(PageBreak())

# ---- Despliegue
story.append(Paragraph('2. Evidencia del proceso de despliegue', H1))
deploy_imgs = []
if a.deploy_dir:
    d = Path(a.deploy_dir)
    deploy_imgs = sorted(p for p in d.glob('*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg'))
if deploy_imgs:
    story.append(Paragraph('Plataforma: Render (servicio web Django) con base de datos MySQL en Aiven. '
                           'Configuración en el repositorio: <font face="Courier">render.yaml</font>, '
                           '<font face="Courier">requirements.txt</font>, variables de entorno y '
                           '<font face="Courier">DESPLIEGUE.md</font>.', P))
    for p in deploy_imgs:
        story += [img(p, 14 * cm), Paragraph(p.stem, CAP)]
else:
    story.append(Paragraph('<b>PENDIENTE:</b> insertar aquí las capturas del despliegue '
                           '(regenerar con <font face="Courier">--deploy-dir</font>).', P))

story += [Paragraph('3. Enlace público para validar', H1)]
if a.url:
    story.append(Paragraph(f'<link href="{a.url}" color="blue">{a.url}</link>', P))
    story.append(Paragraph('Probar: /registro/ para crear un usuario, luego /clientes/ para guardar clientes.', P))
else:
    story.append(Paragraph('<b>PENDIENTE:</b> enlace público de la aplicación desplegada.', P))

SimpleDocTemplate(a.out, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title='Práctica Django con MySQL').build(story)
print('PDF:', a.out)
