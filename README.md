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
👨‍💻 Funcionalidades por rol
🛠️ Administrador

- Registrar nuevos libros
- Registrar usuarios y administradores
- Listar libros, usuarios y préstamos
- Visualizar el estado de los préstamos
- Cerrar sesión

📘 Usuario
- Listar libros disponibles
- Registrar un préstamo
- Ver sus préstamos activos
- Devolver libros
- Cerrar sesión

🔒 Seguridad implementada

Contraseñas cifradas con hashlib.sha256

Evita inyecciones SQL mediante consultas parametrizadas (%s)

Validaciones de tipo y limpieza de entradas de usuario

Control de roles: evita acceso no autorizado a funciones administrativas
