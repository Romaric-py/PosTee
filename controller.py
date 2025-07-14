# UTILS
class TemplateDict(dict):
    def __missing__(self, key):
        return f'{{{key}}}'

def read_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content



# CONTROLLERS 
def home(handler, query_params=None, body_request=None):
    response_content = read_file('html/index.html')
    handler.send_html_response(response_content)

def about(handler, **kwargs):
    response_content = '<h1>Bienvenue dans la section « A propos »</h1>'
    handler.send_html_response(response_content)

def error_404(handler, **kwargs):
    response_content = read_file('html/404.html')
    handler.send_html_response(response_content, 404)

def login_get(handler, **kwargs):
    base_content = read_file('html/auth_views/base.html')
    variable_content = read_file('html/auth_views/login.html')
    context = TemplateDict(title='Connexion', variable_content=variable_content)
    response_content = base_content.format_map(context)
    handler.send_html_response(response_content)

def register_get(handler, **kwargs):
    pass

def login_post(handler, **kwargs):
    pass

def register_post(handler, **kwargs):
    pass

    