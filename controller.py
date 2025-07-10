def read_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def base_html(title, body_content):
    return f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            {body_content}
        </body>
        </html>
    '''

def home(handler):
    response_content = read_file('html/home.html')
    handler.send_html_response(response_content)

def root(handler):
    handler.redirect('/home')

def about(handler):
    response_content = base_html('about', '<h1>Bienvenue dans la section « A propos »</h1>')
    handler.send_html_response(response_content)

def error_404(handler):
    response_content = base_html('404', '<h1>Erreur 404: Page non trouvée</h1>')
    handler.send_html_response(response_content)

def get_users(handler):
    users = ['Manfoya', 'Sephora', 'Ifèdé', 'Gemas', 'Herman', 'Lucie', 'Damien']
    response_content = '<h1>Liste des utilisateurs</h1>\n'
    response_content += '<ul>\n'
    for user in users:
        response_content += f'<li>{user}</li>'
    response_content += '</ul>\n'
    response_content = base_html('Utilisateurs', response_content)
    handler.send_html_response(response_content)
    
    