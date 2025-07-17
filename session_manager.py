import uuid
import time
import threading

SESSION_DURATION = 3600  # 1h

# Use DBManager


def create_session(user_id):
    # Note: utiliser uuid pour générer session_id
    # Retourne la session et sa durée de vie
    return "ey-session-id-not-implemented", SESSION_DURATION

def get_current_user(session_id):
    # consulte la base de données
    # pour connaître l'utilisateur associé, puis retourne son user_id, sinon None
    pass

def logout_session(session_id):
    # Supprime la session de la base de données
    pass

def cleanup_sessions(interval=300):
    def loop():
        while True:
            now = int(time.time())
            ... # requête SQL pour nettoyer les sessions expirées
            print("Sessions expirées nettoyées.")
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
