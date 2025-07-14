from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import os
from datetime import datetime, timedelta, timezone
import json
from controller import *
from routes import routes
from urllib.parse import parse_qs, urlparse, quote, unquote

#
ROUTES = routes
STATIC_DIR = './static'

# Our custom HTTP request handler
class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        """
        Initialise le gestionnaire HTTP personnalisé.

        Appelle le constructeur parent de BaseHTTPRequestHandler.
        """
        super().__init__(*args, **kwargs)
    
    def send_html_response(self, content, status_code=200):
        """
        Envoie une réponse HTTP avec un contenu HTML.

        Args:
            content (str): HTML à renvoyer.
            status_code (int): Code HTTP (200, 404, etc.).
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def redirect(self, location, permanent=False):
        """
        Redirige le client vers une autre URL.

        Args:
            location (str): URL de redirection.
            permanent (bool): Redirection permanente (301) ou temporaire (302).
        """
        status_code = 301 if permanent else 302
        self.send_response(status_code)
        self.send_header('Location', location)
        self.end_headers()

    def set_cookie(self, key, value, path='/', days=None, http_only=True):
        """
        Définit un cookie HTTP.

        Args:
            key (str): Nom du cookie.
            value (str): Valeur du cookie.
            path (str): Portée du cookie.
            days (int): Durée de vie du cookie en jours.
            http_only (bool): Empêche l'accès JavaScript (sécurité).
        """
        cookie = f"{quote(key)}={quote(value)}"
        if days is not None:
            expire_date = datetime.now(timezone.utc) + timedelta(days=days)
            expires_str = expire_date.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            cookie += f"; Expires={expires_str}"
        cookie += f"; Path={path}"
        if http_only:
            cookie += "; HttpOnly"
        self.send_header("Set-Cookie", cookie)

    def get_cookies(self):
        """
        Extrait et retourne les cookies du header HTTP.

        Returns:
            dict: Cookies présents sous forme de paires clé/valeur.
        """
        header = self.headers.get('Cookie')
        if not header:
            return {}
        cookies = {}
        for item in header.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies[unquote(key)] = unquote(value)
        return cookies

    def parse_url_path(self):
        """
        Analyse l'URL pour extraire le chemin et les paramètres.

        Returns:
            tuple: (chemin, dictionnaire des paramètres de requête)
        """
        parsed = urlparse(self.path)
        query_params = {
            key: (values[0] if len(values) == 1 else values)
            for key, values in parse_qs(parsed.query).items()
        }
        return parsed.path, query_params

    def get_request_body(self):
        """
        Lit et parse le corps de la requête HTTP.

        Gère JSON et formulaire encodé (x-www-form-urlencoded).

        Returns:
            dict | None: Données du body ou None si vide ou erreur.
        """
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length == 0:
                return None

            raw_data = self.rfile.read(length)
            content_type = self.headers.get('Content-Type', '').lower()

            if 'application/json' in content_type:
                return json.loads(raw_data.decode())

            elif 'application/x-www-form-urlencoded' in content_type:
                data = raw_data.decode()
                return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(data).items()}

            else:
                # Content-Type non géré
                return None

        except Exception as e:
            print("Erreur get_request_body:", e)
            return None

    def do_GET(self):
        """
        Gère les requêtes HTTP GET.

        Route vers un contrôleur ou sert un fichier statique si aucun contrôleur ne correspond.
        """
        path, query_params = self.parse_url_path()
        request_body = self.get_request_body()

        controller = ROUTES['GET'].get(path, None)

        if controller:
            controller(self, query_params=query_params, request_body=request_body)
        else:
            filepath = self.get_static_file_path(path)
            if filepath:
                self.serve_static_file(filepath)
            else:
                error_404(self)

    def do_POST(self):
        """
        Gère les requêtes HTTP POST.

        Analyse l'URL, extrait les paramètres et le body, 
        puis appelle le contrôleur correspondant.
        """
        path, query_params = self.parse_url_path()
        request_body = self.get_request_body()

        controller = ROUTES['POST'].get(path, None)

        if controller:
            controller(self, 
                    query_params=query_params, 
                    request_body=request_body)
        else:
            error_404(self)


    def get_static_file_path(self, path):
        """
        Détermine le chemin du fichier statique à servir.

        Args:
            path (str): URL demandée.

        Returns:
            str | None: Chemin absolu du fichier ou None si non valide.
        """
        clean_path = os.path.normpath(path).lstrip("/")
        filepath = os.path.join(STATIC_DIR, clean_path)

        if (
            os.path.commonprefix((os.path.abspath(filepath), os.path.abspath(STATIC_DIR))) != os.path.abspath(STATIC_DIR)
            or not os.path.exists(filepath)
            or not os.path.isfile(filepath)
        ):
            return None
        return filepath

    def serve_static_file(self, filepath):
        """
        Sert un fichier statique en réponse HTTP.

        Args:
            filepath (str): Chemin du fichier.
        """
        mime_type, _ = mimetypes.guess_type(filepath)
        if not mime_type:
            mime_type = "application/octet-stream; charset=utf-8"
        else:
            mime_type += '; charset=utf-8'

        with open(filepath, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    
    # Server address
    HOST = 'localhost'
    PORT = 8000
    
    server = HTTPServer((HOST, PORT), MyHandler)
    print(f"Server is running on http://{HOST}:{PORT}")
    server.serve_forever()