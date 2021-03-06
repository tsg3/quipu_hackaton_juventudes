CREATE TABLE IF NOT EXISTS quipu_db.Rol
(
    id INT NOT NULL AUTO_INCREMENT,
    rol VARCHAR(15),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Genero
(
    id INT NOT NULL AUTO_INCREMENT,
    genero VARCHAR(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Usuario
(
    id INT NOT NULL AUTO_INCREMENT,
    idRol INT NOT NULL,
    correo VARCHAR(50),
    nombre VARCHAR(15),
    apellido1 VARCHAR(15),
    apellido2 VARCHAR(15),
    nacimiento DATE,
    idGenero INT NOT NULL,
    nacionalidad VARCHAR(30),
    residencia VARCHAR(30),
    contrasena VARCHAR(20),
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idRol) REFERENCES quipu_db.Rol(id),
    FOREIGN KEY (idGenero) REFERENCES quipu_db.Genero(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Actividad
(
    id INT NOT NULL AUTO_INCREMENT,
    actividad VARCHAR(18),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.UsuarioActividad
(
    idUsuario INT NOT NULL,
    idActividad INT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id),
    FOREIGN KEY (idActividad) REFERENCES quipu_db.Actividad(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Prueba
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    tipo BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Post
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    idVerificador INT,
    datos TEXT(10000),
    publicacion DATETIME,
    titulo VARCHAR(100),
    verificado BOOLEAN,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id),
    FOREIGN KEY (idVerificador) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ComentarioPost
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    idPost INT,
    idComentarioPost INT,
    texto TEXT(10000),
    publicacion DATETIME,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id),
    FOREIGN KEY (idPost) REFERENCES quipu_db.Post(id),
    FOREIGN KEY (idComentarioPost) REFERENCES quipu_db.ComentarioPost(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Etiqueta
(
    id INT NOT NULL AUTO_INCREMENT,
    tipo VARCHAR(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.EtiquetaPost
(
    idEtiqueta INT NOT NULL,
    idPost INT NOT NULL,
    FOREIGN KEY (idEtiqueta) REFERENCES quipu_db.Etiqueta(id),
    FOREIGN KEY (idPost) REFERENCES quipu_db.Post(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Video
(
    id INT NOT NULL AUTO_INCREMENT,
    idPost INT NOT NULL,
    ruta VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Imagen
(
    id INT NOT NULL AUTO_INCREMENT,
    ruta VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ImagenPost
(
    idImagen INT NOT NULL,
    idPost INT NOT NULL,
    FOREIGN KEY (idImagen) REFERENCES quipu_db.Imagen(id),
    FOREIGN KEY (idPost) REFERENCES quipu_db.Post(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.MarketplaceItem
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    idVerificador INT NOT NULL,
    nombre VARCHAR(30),
    lugar VARCHAR(30),
    contacto VARCHAR(30),
    detalle VARCHAR(300),
    precio INT,
    verificado BOOLEAN,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id),
    FOREIGN KEY (idVerificador) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ImagenItem
(
    idImagen INT NOT NULL,
    idItem INT NOT NULL,
    FOREIGN KEY (idImagen) REFERENCES quipu_db.Imagen(id),
    FOREIGN KEY (idItem) REFERENCES quipu_db.MarketplaceItem(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ItemGuardar
(
    idItem INT NOT NULL,
    idUsuario INT NOT NULL,
    FOREIGN KEY (idItem) REFERENCES quipu_db.MarketplaceItem(id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Foro
(
    id BINARY(16) NOT NULL,
    idUsuario INT NOT NULL,
    titulo VARCHAR(100),
    datos TEXT(10000),
    publicacion DATETIME,
    cerrado BOOLEAN,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ComentarioForo
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    idForo BINARY(16),
    idComentarioForo INT,
    texto TEXT(10000),
    publicacion DATETIME,
    votos INT,
    promedio INT,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id),
    FOREIGN KEY (idForo) REFERENCES quipu_db.Foro(id),
    FOREIGN KEY (idComentarioForo) REFERENCES quipu_db.ComentarioForo(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.ForoGuardar
(
    idForo BINARY(16) NOT NULL,
    idUsuario INT NOT NULL,
    estado BOOLEAN,
    FOREIGN KEY (idForo) REFERENCES quipu_db.Foro(id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Evento
(
    id INT NOT NULL AUTO_INCREMENT,
    idUsuario INT NOT NULL,
    titulo VARCHAR(50),
    datos TEXT(1000),
    link VARCHAR(200),
    fecha DATETIME,
    estado BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (idUsuario) REFERENCES quipu_db.Usuario(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Grabacion
(
    id INT NOT NULL AUTO_INCREMENT,
    idEvento INT NOT NULL,
    ruta VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (idEvento) REFERENCES quipu_db.Evento(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.Likert
(
    id INT NOT NULL AUTO_INCREMENT,
    promedio DOUBLE(1, 1),
    votos int,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS quipu_db.LikertPost
(
    idLikert INT NOT NULL,
    idPost INT NOT NULL,
    FOREIGN KEY (idLikert) REFERENCES quipu_db.Likert(id),
    FOREIGN KEY (idPost) REFERENCES quipu_db.Post(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.LikertMarketplaceItem
(
    idLikert INT NOT NULL,
    idItem INT NOT NULL,
    FOREIGN KEY (idLikert) REFERENCES quipu_db.Likert(id),
    FOREIGN KEY (idItem) REFERENCES quipu_db.MarketplaceItem(id)
);

CREATE TABLE IF NOT EXISTS quipu_db.LikertEvento
(
    idLikert INT NOT NULL,
    idEvento INT NOT NULL,
    FOREIGN KEY (idLikert) REFERENCES quipu_db.Likert(id),
    FOREIGN KEY (idEvento) REFERENCES quipu_db.Evento(id)
);

INSERT INTO quipu_db.Rol (rol) VALUES 
    ("J??ven"),
    ("Administrador"),
    ("Autorizado"),
    ("Proveedor");

INSERT INTO quipu_db.Actividad (actividad) VALUES
    ("Pesca"),
    ("Maricultura"),
    ("Ganader??a de carne"),
    ("Ganader??a lechera"),
    ("Porcicultura"),
    ("Entomolfagia"),
    ("Agricultura"),
    ("Avicultura"),
    ("Apicultura");

INSERT INTO quipu_db.Genero (genero) VALUES
    ("Femenino"),
    ("Masculino"),
    ("No binario"),
    ("Otro");