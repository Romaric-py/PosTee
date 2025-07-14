-- USERS
INSERT INTO users (firstname, lastname, email, avatar_url, bio, password, gender) VALUES
('Alice', 'Durand', 'alice@mail.com', '/avatars/alice.jpg', 'Fan de CSS', 'hash1', 'female'),
('Bob', 'Martin', 'bob@mail.com', '/avatars/bob.jpg', 'Dev Python', 'hash2', 'male'),
('Claire', 'Dupont', 'claire@mail.com', '/avatars/claire.jpg', 'Voyageuse', 'hash3', 'female'),
('David', 'Nguyen', 'david@mail.com', NULL, 'Geek en tout', 'hash4', 'male'),
('Eva', 'Bernard', 'eva@mail.com', NULL, 'Design addict', 'hash5', 'female'),
('Farid', 'Kamal', 'farid@mail.com', NULL, 'Hackeur éthique', 'hash6', 'male'),
('Gwen', 'Morel', 'gwen@mail.com', '/avatars/gwen.jpg', 'Fullstack', 'hash7', 'other'),
('Hugo', 'Lopez', 'hugo@mail.com', '/avatars/hugo.jpg', 'Photographe', 'hash8', 'male'),
('Iris', 'Dumont', 'iris@mail.com', NULL, 'Musicienne', 'hash9', 'female'),
('Jean', 'Fabre', 'jean@mail.com', NULL, 'DevOps dans l’âme', 'hash10', 'male');

-- POSTS
INSERT INTO posts (author_id, content, visibility) VALUES
(1, 'Bonjour le monde !', 'public'),
(2, 'Je suis fatigué.', 'private'),
(3, 'Nouveau projet en ligne 💡', 'friends'),
(4, 'Je refais mon portfolio.', 'public'),
(5, 'Des idées de lecture ?', 'public'),
(6, 'Quel framework JS choisir ?', 'friends'),
(7, 'Regardez ce paysage 😍', 'public'),
(8, 'Je quitte Twitter.', 'private'),
(9, 'Refonte de mon blog.', 'public'),
(10, 'Faut-il tout coder from scratch ?', 'friends');

-- COMMENTS
INSERT INTO comments (post_id, author_id, content) VALUES
(1, 2, 'Bienvenue !'),
(1, 3, 'Salut Alice !'),
(2, 4, 'Courage mec'),
(3, 5, 'C’est trop stylé !'),
(4, 6, 'Tu vas utiliser quel stack ?'),
(5, 7, 'Essaye Dune !'),
(6, 8, 'Vue 3 est pas mal.'),
(7, 9, 'Super photo !'),
(8, 10, 'Bonne décision'),
(9, 1, 'Fait avec quel CMS ?');

-- LIKES
INSERT INTO likes (user_id, post_id) VALUES
(2, 1),
(3, 1),
(4, 3),
(5, 3),
(6, 4),
(7, 4),
(8, 5),
(9, 6),
(10, 7),
(1, 9);

-- FRIENDSHIPS
INSERT INTO friendships (user_id_1, user_id_2, initiator_id, status) VALUES
(1, 2, 1, 'accepted'),
(1, 3, 3, 'accepted'),
(2, 4, 2, 'pending'),
(3, 5, 3, 'blocked'),
(4, 6, 6, 'accepted'),
(5, 7, 5, 'accepted'),
(6, 8, 6, 'pending'),
(7, 9, 9, 'accepted'),
(8, 10, 8, 'blocked'),
(1, 10, 1, 'accepted');

-- NOTIFICATIONS
INSERT INTO notifications (user_id, type, content) VALUES
(1, 'like', 'Bob a aimé votre post.'),
(2, 'comment', 'Claire a commenté votre post.'),
(3, 'friend_request', 'David vous a envoyé une demande d’amis.'),
(4, 'like', 'Eva a aimé votre post.'),
(5, 'comment', 'Farid a commenté votre post.'),
(6, 'friend_request', 'Gwen veut être votre ami.e.'),
(7, 'message', 'Nouveau message de Hugo'),
(8, 'comment', 'Iris a réagi.'),
(9, 'like', 'Jean a liké votre photo.'),
(10, 'message', 'Alice vous a écrit.');

-- CONVERSATIONS
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;
INSERT INTO conversations DEFAULT VALUES;

-- PARTICIPANTS
INSERT INTO conversation_participants (conversation_id, user_id) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5), (3, 6),
(4, 7), (4, 8),
(5, 9), (5, 10),
(6, 1), (6, 3),
(7, 2), (7, 5),
(8, 4), (8, 6),
(9, 7), (9, 9),
(10, 8), (10, 10);

-- MESSAGES
INSERT INTO messages (conversation_id, sender_id, body) VALUES
(1, 1, 'Salut Bob !'),
(1, 2, 'Yo Alice.'),
(2, 3, 'T’as fini ton site ?'),
(2, 4, 'Presque'),
(3, 5, 'Faut qu’on parle de JS'),
(3, 6, 'Encore toi !'),
(4, 7, 'Photo à retoucher'),
(4, 8, 'Je gère ça.'),
(5, 9, 'On se voit ce weekend ?'),
(5, 10, 'Carrément.'),
(6, 1, 'Je vais tester Svelte.'),
(6, 3, 'Bon choix !'),
(7, 2, 'T’as lu mon post ?'),
(7, 5, 'Yep, pas mal.'),
(8, 4, 'CSS, t’aime bien ?'),
(8, 6, 'Je préfère SCSS.'),
(9, 7, 'C’est moi ou le serveur lag ?'),
(9, 9, 'Lag oui.'),
(10, 8, 'Bonne nuit'),
(10, 10, 'Toi aussi !');

-- MEDIA
INSERT INTO media (post_id, file_url, mime_type) VALUES
(1, '/uploads/image1.jpg', 'image/jpeg'),
(2, '/uploads/image2.png', 'image/png'),
(3, '/uploads/doc1.pdf', 'application/pdf'),
(4, '/uploads/img4.gif', 'image/gif'),
(5, '/uploads/photo5.jpg', 'image/jpeg'),
(6, '/uploads/pic6.png', 'image/png'),
(7, '/uploads/fichier7.pdf', 'application/pdf'),
(8, '/uploads/media8.mp4', 'video/mp4'),
(9, '/uploads/audio9.mp3', 'audio/mpeg'),
(10, '/uploads/photo10.jpg', 'image/jpeg');

-- SESSIONS
-- ...