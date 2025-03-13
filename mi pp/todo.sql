-- Eliminar la base de datos si ya existe y crearla nuevamente
DROP DATABASE IF EXISTS curso_app;
CREATE DATABASE curso_app;
USE curso_app;

-- Eliminar tablas si ya existen
DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

-- Crear tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_image VARCHAR(255) DEFAULT 'default.png',
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de cursos
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de progreso del usuario en los cursos
CREATE TABLE progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    progress INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Insertar usuarios administradores con contraseñas encriptadas (se deben generar en Python)
DELETE FROM users WHERE username = 'yenyen';

INSERT INTO users (username, email, password_hash, role) 
VALUES ('yenyen', 'yensel01@gmail.com', ' scrypt:32768:8:1$WN4t3YpNDohERHh1$49007020f3f7b84f6efe72f312e5d8f3c9ddcb1c5eba3c2cf3c0c45703c7b3c02cce4538d33eabfed1f247809ea4ff31043f645519125eedd24ff07944dc51a6', 'admin');

INSERT INTO users (username, email, password_hash, role) 
VALUES ('admin', 'admin@example.com', 'HASHED_PASSWORD_ADMIN', 'admin');

-- Ver los usuarios creados
SELECT * FROM users;

INSERT INTO courses (title, description, image_url) VALUES
('Curso de Python', 'Aprende Python desde cero.', 'https://th.bing.com/th/id/OIP.cIs3AywwjmjLpenOhXgyZgHaHa?rs=1&pid=ImgDetMain'),
('Curso de JavaScript', 'Domina JavaScript y crea sitios web interactivos.', 'https://source.unsplash.com/400x300/?javascript'),
('Curso de HTML y CSS', 'Construye páginas web con HTML y CSS.', 'https://source.unsplash.com/400x300/?html,css'),
('Curso de React', 'Desarrolla aplicaciones frontend con React.', 'https://source.unsplash.com/400x300/?react'),
('Curso de Node.js', 'Crea servidores con Node.js y Express.', 'https://source.unsplash.com/400x300/?nodejs'),
('Curso de MySQL', 'Aprende a manejar bases de datos con MySQL.', 'https://source.unsplash.com/400x300/?mysql'),
('Curso de Django', 'Construye aplicaciones web con Django.', 'https://source.unsplash.com/400x300/?django'),
('Curso de Flask', 'Desarrolla APIs con Flask.', 'https://source.unsplash.com/400x300/?flask'),
('Curso de Java', 'Aprende programación con Java.', 'https://source.unsplash.com/400x300/?java'),
('Curso de C#', 'Desarrolla software con C#.', 'https://source.unsplash.com/400x300/?csharp');

select * from progress;