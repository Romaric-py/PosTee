import sqlite3
import bcrypt
from db_manager.db_manager import DBManager
from session_manager import create_session
from utils import read_file, TemplateDict, render

# --- Helpers ---

def render_auth_template(view_path: str, title: str, context: dict) -> str:
    variable_content = render(view_path, context)
    return render('html/auth_views/base.html', 
                  context= {
                    'title': title,
                    'variable_content': variable_content,
                    }, escape=True)


def redirect_with_cookie(handler, location: str, cookie: tuple = None):
    handler.send_response(302)
    handler.send_header('Location', location)
    if cookie:
        key, value, lifetime = cookie
        handler.set_cookie(key, value, seconds=lifetime)
    handler.end_headers()


def retrieve_user_by_email(email: str):
    return DBManager().fetch_one(
        "SELECT id, password FROM users WHERE email = ? AND active = 1", (email,)
    )


def create_user(firstname, lastname, email, password, gender):
    return DBManager().execute(
        """
        INSERT INTO users(firstname, lastname, email, password, gender)
        VALUES (?, ?, ?, ?, ?)
        """,
        (firstname, lastname, email, password, gender)
    )

# --- Views ---

def login_get(handler, form_values=None, error_messages=None, **kwargs):
    context = {
        'email_value': (form_values or {}).get('email', ''),
        'email_error': (error_messages or {}).get('email', ''),
        'password_error': (error_messages or {}).get('password', '')
    }
    html = render_auth_template('html/auth_views/login.html', 'Connexion', context)
    handler.send_html_response(html)


def register_get(handler, form_values=None, error_messages=None, **kwargs):
    context = {
        "firstname_value": form_values.get("firstname", ""),
        "lastname_value": form_values.get("lastname", ""),
        "email_value": form_values.get("email", ""),
        "gender_male_checked": 'checked' if form_values.get('gender') == 'male' else '',
        "gender_female_checked": 'checked' if form_values.get('gender') == 'female' else '',
        "gender_other_checked": 'checked' if form_values.get('gender') == 'other' else '',
        "firstname_error": error_messages.get("firstname", ""),
        "lastname_error": error_messages.get("lastname", ""),
        "email_error": error_messages.get("email", ""),
        "password_error": error_messages.get("password", ""),
        "confirm_password_error": error_messages.get("confirm-password", ""),
    }

    html = render_auth_template('html/auth_views/register.html', 'Inscription', context)
    handler.send_html_response(html)

# --- Controllers ---

def login_post(handler, **kwargs):
    data = kwargs.get('request_body', {})
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return login_get(handler, data, {'email': 'Email requis', 'password': 'Mot de passe requis'})

    row = retrieve_user_by_email(email)
    if not row or not bcrypt.checkpw(password.encode(), row['password'].encode()):
        return login_get(handler, data, {'password': 'Email ou mot de passe incorrect'})

    session_id, lifetime = create_session(row['id'])  # create_session doit retourner un tuple
    redirect_with_cookie(handler, '/feed', ('session_id', session_id, lifetime))


def register_post(handler, **kwargs):
    data = kwargs.get('request_body', {})
    required = {'firstname', 'lastname', 'email', 'password', 'confirm-password'}

    if not required.issubset(data):
        return register_get(handler, data, {'email': 'Tous les champs sont requis'})
    
    # TODO: étape de validation: utiliser une fonction qui prend firstname, lastname, email, password et retourne un dictionnaire des erreurs de validation
    # validate_register_data(...) -> status(bool), errors(dict)

    if data['password'] != data['confirm-password']:
        return register_get(handler, data, {'password': 'Les mots de passe ne correspondent pas'})

    pwd_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

    try:
        user_id = create_user(
            data['firstname'], data['lastname'],
            data['email'], pwd_hash,
            data.get('gender')
        )
    except sqlite3.IntegrityError:
        return register_get(handler, data, {'email': 'Email déjà utilisé'})
    except Exception as e:
        print("[ERREUR INSCRIPTION]", e)
        return handler.redirect('/register')

    session_id, lifetime = create_session(user_id)
    redirect_with_cookie(handler, '/feed', ('session_id', session_id, lifetime))
