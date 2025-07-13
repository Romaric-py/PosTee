-- Utilisateurs
INSERT INTO users (firstname, lastname, email, avatar_url, bio, password, gender)
VALUES 
('Alice', 'Dupont', 'alice@example.com', '/avatars/alice.jpg', 'J’aime les chats.', 'hashed_password_1', 'female'),
('Bob', 'Martin', 'bob@example.com', '/avatars/bob.jpg', 'Développeur JS.', 'hashed_password_2', 'male'),
('Charlie', 'Durand', 'charlie@example.com', '/avatars/charlie.jpg', 'Lecteur compulsif.', 'hashed_password_3', 'other');

-- Publications (posts)
INSERT INTO posts (author_id, content, visibility)
VALUES
(1, 'Bonjour tout le monde ! ☀️', 'public'),
(2, 'Quelqu’un connaît un bon resto à Lyon ?', 'friends'),
(3, 'Ceci est un post privé pour mes yeux uniquement.', 'private');

-- Commentaires
INSERT INTO comments (post_id, author_id, content)
VALUES
(1, 2, 'Salut Alice !'),
(1, 3, 'Bienvenue ici 😄'),
(2, 1, 'Essaie le Bouchon des Cordeliers !');

-- Likes
INSERT INTO likes (user_id, post_id)
VALUES
(2, 1),
(3, 1),
(1, 2);

-- Relations d’amitié
INSERT INTO friendships (user_id_1, user_id_2, status)
VALUES
(1, 2, 'accepted'),
(1, 3, 'pending'),
(2, 3, 'accepted');

-- Notifications
INSERT INTO notifications (user_id, type, content)
VALUES
(1, 'like', 'Bob a aimé votre post.'),
(1, 'comment', 'Charlie a commenté votre post.'),
(2, 'friend_request', 'Alice vous a envoyé une demande d’ami.');

-- Conversations
INSERT INTO conversations DEFAULT VALUES;

-- Participants à la conversation
INSERT INTO conversation_participants (conversation_id, user_id)
VALUES
(1, 1),
(1, 2);

-- Messages
INSERT INTO messages (conversation_id, sender_id, body)
VALUES
(1, 1, 'Salut Bob, ça va ?'),
(1, 2, 'Hey Alice, ça roule et toi ?');

-- Médias
INSERT INTO media (post_id, file_url, mime_type)
VALUES
(1, '/media/post1_photo.jpg', 'image/jpeg'),
(2, '/media/post2_file.pdf', 'application/pdf');

-- Fin du script
