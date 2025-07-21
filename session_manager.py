import uuid
import time
import threading
from db_manager.db_manager import DBManager

SESSION_DURATION = 3600  # 1h pour la durée d'une session
CLEANUP_INTERVAL   = 300  # 5 minutes entre deux nettoyages



# Création d’une session 
def create_session(user_id: int) -> tuple[str, int]:# c'est toi qui a dit que ce n'est pas erreur inh
    """
    Créer une noouvelle session pour l'utilisateur dont le 
    id est donné et on retourne le tuple
    (session_id, lifetime_in_seconds) : l'id de la session et la durée de vie de la session.
    """
    session_id = str(uuid.uuid4()) # génère un identifiant unique pour la session
    expires_at = int(time.time()) + SESSION_DURATION

    DBManager().execute(
        "INSERT INTO sessions(session_id, user_id, expires_at) VALUES (?, ?, ?)",
        (session_id, user_id, expires_at)
    )
    return session_id, SESSION_DURATION



#Renvoie l'user_id associé à la session si elle existe et n’est pas expirée.
def get_current_user(session_id: str) -> int | None:
    """
    Returns the user_id associated with a valid, non-expired session_id.
    Retourne None si la session est absent ou expiré
    """
    if not session_id:
        return None

    row = DBManager().fetch_one(
        "SELECT user_id FROM sessions WHERE session_id = ? AND expires_at > ?",
        (session_id, int(time.time()))
    )
    return row["user_id"] if row else None



# Déconnexion : suppression d’une session
def logout_session(session_id: str) -> None:
    """
    Supprime la session de la base de données 
    """
    DBManager().execute(
        "DELETE FROM sessions WHERE session_id = ?", (session_id,)
    )




# Tâche de fond : nettoyage automatique des sessions expirées
def cleanup_sessions(interval: int = CLEANUP_INTERVAL) -> None:
    """
    Lance un thread démon qui nettoie les sessions expirées toutes les 'interval' secondes.
    """
    def loop():
        while True:
            now = int(time.time())
            deleted = DBManager().execute(
                "DELETE FROM sessions WHERE expires_at <= ?", (now,)
            )
            print(f"[SessionCleaner] {deleted} session(s) expirée(s) supprimée(s).")
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()

