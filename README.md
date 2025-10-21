# 📚 Sistema de Biblioteca en Python y MySQL

Este proyecto es un **Sistema de Gestión de Biblioteca** desarrollado en **Python 3** con conexión a una base de datos **MySQL**.  
Permite la administración completa de libros, usuarios, préstamos y devoluciones, con roles diferenciados para **administradores** y **usuarios regulares**.

---

## 🚀 Características principales

- 🔐 **Login seguro** con contraseñas encriptadas (SHA-256)
- 👨‍💼 **Roles de usuario**: Administrador y Usuario
- 📚 **Gestión de libros**: alta, listado y control de disponibilidad
- 👥 **Gestión de usuarios** y administradores
- 📖 **Registro y control de préstamos**
- ↩️ **Devolución de libros** con actualización automática del stock
- 🧠 **Validaciones de entrada** para evitar errores y SQL injection
- 🛡️ **Uso de consultas parametrizadas** para máxima seguridad

---


CREATE TABLE administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255)
);

CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(30),
    editorial VARCHAR(100),
    año_publicacion INT,
    categoria VARCHAR(50),
    cantidad_disponible INT DEFAULT 0
);

CREATE TABLE prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE,
    estado ENUM('activo', 'devuelto') DEFAULT 'activo',
    FOREIGN KEY (libro_id) REFERENCES libros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
