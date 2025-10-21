import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime, timedelta
import hashlib


class SistemaLibreria:
    def __init__(self):
        self.connection = None
        self.usuario_actual = None
        self.tipo_usuario = None
        self.nombre_usuario = None
        
    def conectar_bd(self):
        """Conectar a la base de datos MySQL de forma segura"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='sistema_libreria',
                user='root',  # Cambiar por tu usuario de MySQL
                password='toor'   # Cambiar por tu contraseña de MySQL
            )
            if self.connection.is_connected():
                print("✓ Conexión exitosa a la base de datos")
                return True
        except Error as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            print("Por favor verifica:")
            print("1. Que MySQL esté ejecutándose")
            print("2. Que la base de datos 'sistema_libreria' exista")
            print("3. Que el usuario y contraseña sean correctos")
            return False

    def verificar_tablas(self):
        """Verificar que las tablas necesarias existan"""
        tablas_requeridas = ['administradores', 'usuarios', 'libros', 'prestamos']
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
            
            for tabla in tablas_requeridas:
                if tabla not in tablas_existentes:
                    print(f"✗ Tabla '{tabla}' no encontrada en la base de datos")
                    return False
            
            print("✓ Todas las tablas necesarias existen")
            return True
        except Error as e:
            print(f"✗ Error al verificar tablas: {e}")
            return False

    def hash_password(self, password):
        """Hashear la contraseña para mayor seguridad usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_password(self, password, password_hash):
        """Verificar si la contraseña coincide con el hash"""
        return self.hash_password(password) == password_hash

    def validar_input(self, texto):
        """Validar y limpiar input básico"""
        return texto.strip()

    def validar_numero(self, texto):
        """Validar que el input sea un número"""
        try:
            return int(texto.strip())
        except ValueError:
            return None

    def login(self):
        """Sistema de login unificado"""
        print("\n" + "="*50)
        print("           SISTEMA DE LOGIN")
        print("="*50)
        
        username = self.validar_input(input("Username/Email: "))
        password = getpass.getpass("Password: ")
        
        if not username or not password:
            print("✗ Username/Email y password son requeridos")
            return False
        
        # Primero intentamos buscar como administrador
        if self.verificar_credenciales_administrador(username, password):
            self.tipo_usuario = "administrador"
            return True
        
        # Si no es administrador, buscamos como usuario regular
        if self.verificar_credenciales_usuario(username, password):
            self.tipo_usuario = "usuario"
            return True
        
        print("✗ Credenciales incorrectas o usuario no encontrado")
        return False
    
    def verificar_credenciales_administrador(self, username, password):
        """Verificar credenciales de administrador con contraseña encriptada"""
        try:
            cursor = self.connection.cursor()
            query = "SELECT id, nombre, password FROM administradores WHERE username = %s"
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Verificar contraseña hasheada
                if self.verificar_password(password, resultado[2]):
                    self.usuario_actual = resultado[0]
                    self.nombre_usuario = resultado[1]
                    print(f"\n✓ Bienvenido administrador: {resultado[1]}")
                    return True
                else:
                    print("✗ Contraseña incorrecta")
            return False
        except Error as e:
            print(f"Error en login administrador: {e}")
            return False
    
    def verificar_credenciales_usuario(self, username, password):
        """Verificar credenciales de usuario regular con contraseña encriptada"""
        try:
            cursor = self.connection.cursor()
            query = "SELECT id, nombre, password FROM usuarios WHERE email = %s"
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Verificar contraseña hasheada
                if self.verificar_password(password, resultado[2]):
                    self.usuario_actual = resultado[0]
                    self.nombre_usuario = resultado[1]
                    print(f"\n✓ Bienvenido usuario: {resultado[1]}")
                    return True
                else:
                    print("✗ Contraseña incorrecta")
            return False
        except Error as e:
            print(f"Error en login usuario: {e}")
            return False

    # === FUNCIONES PARA ADMINISTRADORES ===
    
    def registrar_libro(self):
        """Registrar nuevo libro de forma segura"""
        print("\n" + "="*50)
        print("        REGISTRAR NUEVO LIBRO")
        print("="*50)
        
        # Validar todos los inputs
        titulo = self.validar_input(input("Título: "))
        autor = self.validar_input(input("Autor: "))
        isbn = self.validar_input(input("ISBN: "))
        editorial = self.validar_input(input("Editorial: "))
        
        año_input = input("Año de publicación: ")
        año = self.validar_numero(año_input)
        if año is None:
            print("✗ Año debe ser un número válido")
            return
        
        categoria = self.validar_input(input("Categoría: "))
        
        cantidad_input = input("Cantidad disponible: ")
        cantidad = self.validar_numero(cantidad_input)
        if cantidad is None or cantidad < 0:
            print("✗ Cantidad debe ser un número positivo")
            return
        
        # Validar campos requeridos
        if not titulo or not autor:
            print("✗ Título y autor son campos requeridos")
            return
        
        try:
            cursor = self.connection.cursor()
            # Uso de parámetros para prevenir inyecciones SQL
            query = """INSERT INTO libros (titulo, autor, isbn, editorial, año_publicacion, categoria, cantidad_disponible) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (titulo, autor, isbn, editorial, año, categoria, cantidad))
            self.connection.commit()
            print("✓ Libro registrado exitosamente!")
        except Error as e:
            print(f"✗ Error al registrar libro: {e}")
    
    def registrar_usuario(self):
        """Registrar nuevo usuario de forma segura con contraseña encriptada"""
        print("\n" + "="*50)
        print("       REGISTRAR NUEVO USUARIO")
        print("="*50)
        
        nombre = self.validar_input(input("Nombre: "))
        email = self.validar_input(input("Email: "))
        password = getpass.getpass("Password (mínimo 4 caracteres): ")
        confirm_password = getpass.getpass("Confirmar password: ")
        telefono = self.validar_input(input("Teléfono: "))
        direccion = self.validar_input(input("Dirección: "))
        
        # Validaciones
        if not nombre or not email or not password:
            print("✗ Nombre, email y password son campos requeridos")
            return
        
        if password != confirm_password:
            print("✗ Las contraseñas no coinciden")
            return
        
        if len(password) < 4:
            print("✗ La contraseña debe tener al menos 4 caracteres")
            return
        
        try:
            cursor = self.connection.cursor()
            # Verificar si el email ya existe
            check_query = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(check_query, (email,))
            if cursor.fetchone():
                print("✗ El email ya está registrado")
                return
            
            # Hashear la contraseña antes de guardarla
            password_hash = self.hash_password(password)
            
            # Insertar nuevo usuario con parámetros
            query = "INSERT INTO usuarios (nombre, email, password, telefono, direccion) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, email, password_hash, telefono, direccion))
            self.connection.commit()
            print("✓ Usuario registrado exitosamente!")
            print("🔒 Contraseña encriptada y guardada de forma segura")
        except Error as e:
            print(f"✗ Error al registrar usuario: {e}")
    
    def registrar_administrador(self):
        """Registrar nuevo administrador de forma segura con contraseña encriptada"""
        print("\n" + "="*50)
        print("     REGISTRAR NUEVO ADMINISTRADOR")
        print("="*50)
        
        username = self.validar_input(input("Username: "))
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirmar password: ")
        nombre = self.validar_input(input("Nombre completo: "))
        email = self.validar_input(input("Email: "))
        
        # Validaciones
        if not username or not password or not nombre or not email:
            print("✗ Todos los campos son requeridos")
            return
        
        if password != confirm_password:
            print("✗ Las contraseñas no coinciden")
            return
        
        if len(password) < 4:
            print("✗ La contraseña debe tener al menos 4 caracteres")
            return
        
        try:
            cursor = self.connection.cursor()
            # Verificar si el username ya existe
            check_query = "SELECT id FROM administradores WHERE username = %s"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                print("✗ El username ya está registrado")
                return
            
            # Hashear la contraseña antes de guardarla
            password_hash = self.hash_password(password)
            
            # Insertar nuevo administrador con parámetros
            query = "INSERT INTO administradores (username, password, nombre, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password_hash, nombre, email))
            self.connection.commit()
            print("✓ Administrador registrado exitosamente!")
            print("🔒 Contraseña encriptada y guardada de forma segura")
        except Error as e:
            print(f"✗ Error al registrar administrador: {e}")
    
    def listar_libros(self):
        """Listar todos los libros de forma segura"""
        print("\n" + "="*50)
        print("           LISTA DE LIBROS")
        print("="*50)
        try:
            cursor = self.connection.cursor()
            # Consulta segura sin parámetros de usuario
            query = "SELECT id, titulo, autor, editorial, año_publicacion, categoria, cantidad_disponible FROM libros ORDER BY titulo"
            cursor.execute(query)
            libros = cursor.fetchall()
            
            if libros:
                print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Editorial':<15} {'Año':<6} {'Categoría':<15} {'Disp.'}")
                print("-" * 95)
                for libro in libros:
                    print(f"{libro[0]:<5} {libro[1]:<25} {libro[2]:<20} {libro[3]:<15} {libro[4]:<6} {libro[5]:<15} {libro[6]:<5}")
            else:
                print("No hay libros registrados")
        except Error as e:
            print(f"✗ Error al listar libros: {e}")
    
    def listar_usuarios(self):
        """Listar todos los usuarios de forma segura"""
        print("\n" + "="*50)
        print("          LISTA DE USUARIOS")
        print("="*50)
        try:
            cursor = self.connection.cursor()
            # Consulta segura
            query = "SELECT id, nombre, email, telefono FROM usuarios ORDER BY nombre"
            cursor.execute(query)
            usuarios = cursor.fetchall()
            
            if usuarios:
                print(f"{'ID':<5} {'Nombre':<20} {'Email':<25} {'Teléfono':<15}")
                print("-" * 70)
                for usuario in usuarios:
                    print(f"{usuario[0]:<5} {usuario[1]:<20} {usuario[2]:<25} {usuario[3]:<15}")
            else:
                print("No hay usuarios registrados")
        except Error as e:
            print(f"✗ Error al listar usuarios: {e}")
    
    def listar_prestamos(self):
        """Listar todos los préstamos con INNER JOIN de forma segura"""
        print("\n" + "="*50)
        print("          LISTA DE PRÉSTAMOS")
        print("="*50)
        try:
            cursor = self.connection.cursor()
            # Consulta segura con INNER JOIN
            query = """
            SELECT p.id, l.titulo, u.nombre, p.fecha_prestamo, p.fecha_devolucion, p.estado
            FROM prestamos p
            INNER JOIN libros l ON p.libro_id = l.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY p.fecha_prestamo DESC
            """
            cursor.execute(query)
            prestamos = cursor.fetchall()
            
            if prestamos:
                print(f"{'ID':<5} {'Libro':<20} {'Usuario':<15} {'Préstamo':<12} {'Devolución':<12} {'Estado':<10}")
                print("-" * 80)
                for prestamo in prestamos:
                    devolucion = prestamo[4] if prestamo[4] else "Pendiente"
                    estado = "✅ Activo" if prestamo[5] == 'activo' else "✅ Devuelto"
                    print(f"{prestamo[0]:<5} {prestamo[1]:<20} {prestamo[2]:<15} {str(prestamo[3]):<12} {str(devolucion):<12} {estado:<10}")
            else:
                print("No hay préstamos registrados")
        except Error as e:
            print(f"✗ Error al listar préstamos: {e}")

    # === FUNCIONES PARA USUARIOS ===
    
    def registrar_prestamo(self):
        """Registrar nuevo préstamo de forma segura"""
        print("\n" + "="*50)
        print("          REGISTRAR PRÉSTAMO")
        print("="*50)
        self.listar_libros_disponibles()
        
        libro_input = input("\nID del libro a prestar: ")
        libro_id = self.validar_numero(libro_input)
        
        if libro_id is None:
            print("✗ ID debe ser un número válido")
            return
        
        try:
            cursor = self.connection.cursor()
            # Verificar disponibilidad con parámetros
            query = "SELECT id, titulo, cantidad_disponible FROM libros WHERE id = %s AND cantidad_disponible > 0"
            cursor.execute(query, (libro_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                fecha_prestamo = datetime.now().date()
                fecha_devolucion_estimada = fecha_prestamo + timedelta(days=15)
                
                # Registrar préstamo con parámetros
                query = "INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, estado) VALUES (%s, %s, %s, 'activo')"
                cursor.execute(query, (libro_id, self.usuario_actual, fecha_prestamo))
                
                # Actualizar cantidad disponible con parámetros
                query = "UPDATE libros SET cantidad_disponible = cantidad_disponible - 1 WHERE id = %s"
                cursor.execute(query, (libro_id,))
                
                self.connection.commit()
                print(f"\n✓ Préstamo registrado exitosamente!")
                print(f"📖 Libro: {resultado[1]}")
                print(f"📅 Fecha de préstamo: {fecha_prestamo}")
                print(f"⏰ Devolver antes de: {fecha_devolucion_estimada}")
            else:
                print("✗ Libro no disponible o no encontrado")
                
        except Error as e:
            print(f"✗ Error al registrar préstamo: {e}")
    
    def listar_libros_disponibles(self):
        """Listar solo libros disponibles de forma segura"""
        print("\n" + "="*50)
        print("        LIBROS DISPONIBLES")
        print("="*50)
        try:
            cursor = self.connection.cursor()
            # Consulta segura
            query = "SELECT id, titulo, autor, editorial, categoria, cantidad_disponible FROM libros WHERE cantidad_disponible > 0 ORDER BY titulo"
            cursor.execute(query)
            libros = cursor.fetchall()
            
            if libros:
                print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Editorial':<15} {'Categoría':<15} {'Disp.'}")
                print("-" * 85)
                for libro in libros:
                    print(f"{libro[0]:<5} {libro[1]:<25} {libro[2]:<20} {libro[3]:<15} {libro[4]:<15} {libro[5]:<5}")
            else:
                print("No hay libros disponibles")
        except Error as e:
            print(f"✗ Error al listar libros: {e}")
    
    def devolver_libro(self):
        """Devolver libro prestado de forma segura"""
        print("\n" + "="*50)
        print("           DEVOLVER LIBRO")
        print("="*50)
        self.mis_prestamos_activos()
        
        prestamo_input = input("\nID del préstamo a devolver: ")
        prestamo_id = self.validar_numero(prestamo_input)
        
        if prestamo_id is None:
            print("✗ ID debe ser un número válido")
            return
        
        try:
            cursor = self.connection.cursor()
            
            # Verificar que el préstamo pertenece al usuario actual con parámetros
            query = """SELECT p.libro_id, l.titulo 
                      FROM prestamos p 
                      INNER JOIN libros l ON p.libro_id = l.id 
                      WHERE p.id = %s AND p.usuario_id = %s AND p.estado = 'activo'"""
            cursor.execute(query, (prestamo_id, self.usuario_actual))
            resultado = cursor.fetchone()
            
            if resultado:
                libro_id = resultado[0]
                libro_titulo = resultado[1]
                fecha_devolucion = datetime.now().date()
                
                # Actualizar préstamo con parámetros
                query = "UPDATE prestamos SET estado = 'devuelto', fecha_devolucion = %s WHERE id = %s"
                cursor.execute(query, (fecha_devolucion, prestamo_id))
                
                # Actualizar cantidad disponible del libro con parámetros
                query = "UPDATE libros SET cantidad_disponible = cantidad_disponible + 1 WHERE id = %s"
                cursor.execute(query, (libro_id,))
                
                self.connection.commit()
                print(f"✓ Libro '{libro_titulo}' devuelto exitosamente!")
                print(f"📅 Fecha de devolución: {fecha_devolucion}")
            else:
                print("✗ Préstamo no encontrado, ya devuelto o no te pertenece")
                
        except Error as e:
            print(f"✗ Error al devolver libro: {e}")
    
    def mis_prestamos_activos(self):
        """Mostrar préstamos activos del usuario actual de forma segura"""
        print("\n" + "="*50)
        print("        MIS PRÉSTAMOS ACTIVOS")
        print("="*50)
        try:
            cursor = self.connection.cursor()
            # Consulta segura con parámetros
            query = """
            SELECT p.id, l.titulo, p.fecha_prestamo, l.autor
            FROM prestamos p
            INNER JOIN libros l ON p.libro_id = l.id
            WHERE p.usuario_id = %s AND p.estado = 'activo'
            ORDER BY p.fecha_prestamo DESC
            """
            cursor.execute(query, (self.usuario_actual,))
            prestamos = cursor.fetchall()
            
            if prestamos:
                print(f"{'ID':<5} {'Libro':<25} {'Autor':<20} {'Préstamo':<12}")
                print("-" * 65)
                for prestamo in prestamos:
                    fecha_devolucion_estimada = prestamo[2] + timedelta(days=15)
                    print(f"{prestamo[0]:<5} {prestamo[1]:<25} {prestamo[3]:<20} {str(prestamo[2]):<12}")
                    print(f"     📅 Devolver antes: {fecha_devolucion_estimada}")
                    print()
            else:
                print("No tienes préstamos activos")
        except Error as e:
            print(f"✗ Error al listar préstamos: {e}")

    # === MENÚ PRINCIPAL ===
    
    def menu_administrador(self):
        """Menú para administradores"""
        while True:
            print("\n" + "="*50)
            print(f"    MENÚ ADMINISTRADOR - {self.nombre_usuario}")
            print("="*50)
            print("1. 📚 Registrar libro")
            print("2. 👥 Registrar usuario")
            print("3. 🔧 Registrar administrador")
            print("4. 📖 Listar libros")
            print("5. 👨‍💼 Listar usuarios")
            print("6. 📋 Listar préstamos")
            print("7. 🚪 Cerrar sesión")
            print("-"*50)
            
            opcion = input("Seleccione una opción (1-7): ")
            
            if opcion == "1":
                self.registrar_libro()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "3":
                self.registrar_administrador()
            elif opcion == "4":
                self.listar_libros()
            elif opcion == "5":
                self.listar_usuarios()
            elif opcion == "6":
                self.listar_prestamos()
            elif opcion == "7":
                print("¡Sesión cerrada! 👋")
                break
            else:
                print("✗ Opción inválida")
    
    def menu_usuario(self):
        """Menú para usuarios"""
        while True:
            print("\n" + "="*50)
            print(f"      MENÚ USUARIO - {self.nombre_usuario}")
            print("="*50)
            print("1. 📚 Listar libros disponibles")
            print("2. 📖 Registrar préstamo")
            print("3. 📋 Mis préstamos activos")
            print("4. ↩️  Devolver libro")
            print("5. 🚪 Cerrar sesión")
            print("-"*50)
            
            opcion = input("Seleccione una opción (1-5): ")
            
            if opcion == "1":
                self.listar_libros_disponibles()
            elif opcion == "2":
                self.registrar_prestamo()
            elif opcion == "3":
                self.mis_prestamos_activos()
            elif opcion == "4":
                self.devolver_libro()
            elif opcion == "5":
                print("¡Sesión cerrada! 👋")
                break
            else:
                print("✗ Opción inválida")
    
    def ejecutar(self):
        """Función principal del sistema"""
        print("🚀 Iniciando Sistema de Biblioteca...")
        
        if not self.conectar_bd():
            print("No se pudo conectar a la base de datos. Saliendo...")
            input("Presiona Enter para continuar...")
            return
        
        if not self.verificar_tablas():
            print("Faltan tablas en la base de datos. Saliendo...")
            input("Presiona Enter para continuar...")
            return
        
        # Inicia directamente con el login
        if self.login():
            if self.tipo_usuario == "administrador":
                self.menu_administrador()
            else:
                self.menu_usuario()
        
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    try:
        # Ejecutar el sistema principal directamente
        sistema = SistemaLibreria()
        sistema.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n❌ Sistema interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        input("Presiona Enter para salir...")
        self.connection = mysql.connector.connect(
    
    host='localhost',
    database='sistema_libreria',
    user='root',
    password='toor'  # Cambia esto por tu contraseña
)
