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

# Je suppose que register_get sert à envoyer le formulaire
def register_get(handler, **kwargs):
    # Cette fonction sert à afficher la page d'inscription.
    # Elle lit le template HTML de base et le contenu spécifique à l'inscription,
    # puis insère ce contenu dans le template avant de l'envoyer comme réponse HTML.

    base_content = read_file('html/auth_views/base.html')
    variable_content = read_file('html/auth_views/register.html')
    context = TemplateDict(title='Inscription', variable_content=variable_content)
    response_content = base_content.format_map(context)
    handler.send_html_response(response_content)

# login_post : ici c’est pour l’authentification, et il crée une session dans la table
def login_post(handler, **kwargs):
    # Cette fonction traite une tentative de connexion d’un utilisateur.
    # Étapes :
    # 1. Lire le corps de la requête HTTP (formulaire soumis)
    # 2. Vérifier que l’email et le mot de passe sont présents
    # 3. Chercher l’utilisateur actif dans la base de données
    # 4. Vérifier le mot de passe avec bcrypt
    # 5. Si ok, créer une session et renvoyer un cookie au navigateur

    body = handler.rfile.read(int(handler.headers['Content-Length'])).decode()
    data = {k: v[0] for k, v in parse_qs(body).items()}

    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        handler.send_json_response({'error': 'Champs manquants'}, 400)
        return

    row = DBManager().fetch_one(
        "SELECT id, password FROM users WHERE email = ? AND active = 1", (email,)
    )
    if not row or not bcrypt.checkpw(password.encode(), row['password'].encode()):
        handler.send_json_response({'error': 'Identifiants invalides'}, 401)
        return

    session_id = secrets.token_urlsafe(32)
    expires = int(time.time()) + 60 * 60 * 24 * 7
    DBManager().execute("INSERT INTO sessions(session_id, user_id, expires_at) VALUES (?,?,?)",
                        (session_id, row['id'], expires))

    handler.send_response(302)
    handler.send_header('Location', '/feed')
    handler.send_header('Set-Cookie', f'session={session_id}; HttpOnly; Path=/')
    handler.end_headers()

# Ah, ici c’est pour créer un compte
def register_post(handler, **kwargs):
    # Cette fonction gère l’inscription d’un utilisateur.
    # Étapes :
    # 1. Lire et parser les données du formulaire soumis
    # 2. Vérifier que tous les champs requis sont présents et valides
    # 3. Hasher le mot de passe de manière sécurisée avec bcrypt
    # 4. Enregistrer l’utilisateur dans la base de données
    # 5. Créer une session automatiquement (connexion immédiate)
    # 6. Envoyer un cookie au navigateur avec l'ID de session

    # Lecture du corps de la requête
    body = handler.rfile.read(int(handler.headers['Content-Length'])).decode()
    data = {k: v[0] for k, v in parse_qs(body).items()}

    # Vérification des champs obligatoires
    required = {'firstname', 'lastname', 'email', 'password', 'confirm-password'}
    if not required.issubset(data):
        handler.send_json_response({'error': 'Champs manquants'}, 400)
        return
    if data['password'] != data['confirm-password']:
        handler.send_json_response({'error': 'Mots de passe différents'}, 400)
        return

    # Hachage du mot de passe
    pwd_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

    # Insertion de l’utilisateur en base
    try:
        db = DBManager()
        user_id = db.execute(
            """INSERT INTO users(firstname, lastname, email, password, gender)
               VALUES (?,?,?,?,?)""",
            (data['firstname'], data['lastname'], data['email'], pwd_hash,
             data.get('gender'))
        )
    except sqlite3.IntegrityError:
        handler.send_json_response({'error': 'Cet e-mail existe déjà'}, 409)
        return

    # Création d’une session (connexion automatique après inscription)
    session_id = secrets.token_urlsafe(32)
    expires = int(time.time()) + 60 * 60 * 24 * 7  # 7 jours
    db.execute("INSERT INTO sessions(session_id, user_id, expires_at) VALUES (?,?,?)",
               (session_id, user_id, expires))

    handler.send_response(302)
    handler.send_header('Location', '/feed')  # Redirection après inscription
    handler.send_header('Set-Cookie', f'session={session_id}; HttpOnly; Path=/')
    handler.end_headers()