from utils import read_file, TemplateDict


# --- Helpers ---

def send_html(handler, path: str, status=200):
    content = read_file(path)
    handler.send_html_response(content, status_code=status)


# --- Routes ---

def home(handler, **kwargs):
    send_html(handler, 'html/index.html')


def about(handler, **kwargs):
    handler.send_html_response('<h1>Bienvenue dans la section « A propos »</h1>')

def error_404(handler, **kwargs):
    send_html(handler, 'html/404.html', status=404)

def feed(handler, **kwargs):
    session_id = handler.get_cookies().get('session_id')
    variable_content = f'<h1>Cette page atteste que vous êtes authentifié <br> SESSION_ID: {session_id}</h1>'
    context = TemplateDict(title='Feed', variable_content=variable_content, escape=False)
    base_content = read_file('html/auth_views/base.html')
    response_content = base_content.format_map(context)
    handler.send_html_response(response_content)
