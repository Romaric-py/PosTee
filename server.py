from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import os
from controller import *
from routes import routes

#
ROUTES = routes
STATIC_DIR = './static'

# Our custom HTTP request handler
class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        """Initialise le constructeur de la classe parente puis définit les attributs d'instance
        
        Args:
            self (MyHandler): instance de classe
        """
        super().__init__(*args, **kwargs)
    
    def send_html_response(self, content, status_code=200):
        """Fournit une réponse html au client

        Args:
            status_code (int): code status
            content (str): contenu
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def redirect(self, location, permanent=False):
        status_code = (301 if permanent else 302)
        self.send_response(status_code)
        self.send_header('Location', location)
        self.end_headers()
    
    def do_GET(self):
        """Gère toutes les requêtes dont la méthode est GET
        
        Args:
            self (MyHandler): instance de classe
        """
        print('Path:', self.path, '; Method:', self.command)
        controller = ROUTES['GET'].get(self.path, None)
        if controller:
            controller(self)
        else:
            filepath = self.get_static_file_path(self.path)
            if filepath:
                self.serve_static_file(filepath)
            else:
                error_404(self)
            
              
    def do_POST(self):
        """Gère toutes les requêtes dont la méthode est POST
        
        Args:
            self (MyHandler): instance de classe
        """
        print('Path:', self.path, '; Method:', self.command)
    
    def get_static_file_path(self, path):
        clean_path = os.path.normpath(path).lstrip("/")
        filepath = os.path.join(STATIC_DIR, clean_path)

        # Sécurité basique : empêcher de sortir du dossier
        if os.path.commonprefix((os.path.abspath(filepath), os.path.abspath(STATIC_DIR))) != os.path.abspath(STATIC_DIR) or not os.path.exists(filepath):
            return None
        return filepath
    
    def serve_static_file(self, filepath):
        """Sert un fichier statique spécifié

        Args:
            filepath (str): nom du chemin relatif vers le fichier
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