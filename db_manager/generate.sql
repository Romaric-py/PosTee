-- 1️ Utilisateurs
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname   TEXT    NOT NULL,
    lastname    TEXT    NOT NULL,
    email       TEXT    UNIQUE,
    avatar_url  TEXT,
    bio         TEXT,
    password    TEXT    NOT NULL,                 -- mot de passe haché (bcrypt/argon2)
    gender      TEXT    CHECK (gender IN ('male','female','other')),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    active      BOOLEAN DEFAULT 1                 -- 1 = actif, 0 = désactivé
);

-- 2️ Publications (posts)
CREATE TABLE posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content     TEXT    NOT NULL,
    visibility  TEXT    CHECK (visibility IN ('public','friends','private')) DEFAULT 'public',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    active      BOOLEAN DEFAULT 1
);

-- 3️ Commentaires
CREATE TABLE comments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id     INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content     TEXT    NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    active      BOOLEAN DEFAULT 1
);

-- 4️ Likes
CREATE TABLE likes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id     INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)                      -- un seul like par utilisateur et par post
);

-- 5️ Relations d'amitié
CREATE TABLE friendships (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id_1     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_id_2     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    initiator_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status        TEXT CHECK (status IN ('pending','accepted','blocked')) DEFAULT 'pending',
    active        BOOLEAN DEFAULT 1,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id_1, user_id_2),
    CHECK (user_id_1 < user_id_2),
    CHECK (initiator_id IN (user_id_1, user_id_2))
);

-- 6️ Notifications
CREATE TABLE notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type        TEXT    CHECK (type IN ('like','comment','friend_request','message')) NOT NULL,
    content     TEXT    NOT NULL,
    is_read     BOOLEAN DEFAULT 0,                 -- 0 = non lue, 1 = lue
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7️ Conversations
CREATE TABLE conversations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8️ Participants à une conversation
CREATE TABLE conversation_participants (
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (conversation_id, user_id)
);

-- 9️ Messages dans une conversation
CREATE TABLE messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body            TEXT    NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    edited_at       DATETIME,
    deleted         BOOLEAN DEFAULT 0,             -- suppression douce
    active          BOOLEAN DEFAULT 1
);

-- 🔟 Pièces jointes / médias
CREATE TABLE media (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id     INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    message_id  INTEGER REFERENCES messages(id) ON DELETE CASCADE,
    file_url    TEXT NOT NULL,
    mime_type   TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 11 Sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expires_at INTEGER NOT NULL
);


-- Index pour performances
CREATE INDEX idx_posts_visibility    ON posts(active, visibility, created_at);
CREATE INDEX idx_friendships_status  ON friendships(status);
CREATE INDEX idx_notifications_read  ON notifications(user_id, is_read, created_at);
CREATE INDEX idx_messages_conv_time  ON messages(conversation_id, created_at);
CREATE INDEX idx_media_post          ON media(post_id);
CREATE INDEX idx_media_message       ON media(message_id);


-- Triggers de mise à jour automatique (anti-récursifs)

-- Trigger pour users
CREATE TRIGGER trg_users_updated
AFTER UPDATE ON users
FOR EACH ROW
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger pour posts
CREATE TRIGGER trg_posts_updated
AFTER UPDATE ON posts
FOR EACH ROW
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE posts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger pour comments
CREATE TRIGGER trg_comments_updated
AFTER UPDATE ON comments
FOR EACH ROW
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE comments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger pour friendships
CREATE TRIGGER trg_friendships_updated
AFTER UPDATE ON friendships
FOR EACH ROW
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE friendships SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
