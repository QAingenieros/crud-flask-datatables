# Sistema de Gestión con Flask y DataTables

Sistema de gestión que implementa un CRUD completo con Flask como backend y DataTables para la interfaz de usuario.

## Características

- CRUD completo (Create, Read, Update, Delete)
- Soft Delete implementado
- Interfaz responsiva con Bootstrap
- Tablas dinámicas con DataTables
- API RESTful
- Soporte para múltiples tipos de datos
- Documentación automática de endpoints

## Tecnologías Utilizadas

### Backend
- Flask 3.0.2
- SQLAlchemy 2.0.28
- Flask-SQLAlchemy 3.1.1
- Python 3.x

### Frontend
- jQuery 3.7.1
- DataTables 1.13.7
- Bootstrap 5.3.0
- Font Awesome 6.2.0

## Estructura del Proyecto

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# .flaskenv
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
```

5. Inicializar la base de datos:
```bash
flask init-db
```

## Uso

1. Iniciar el servidor:
```bash
flask run
```

2. Acceder a la aplicación:
```
http://localhost:5000
```

## Modelos de Datos

### Usuario
- id: Integer (Primary Key)
- nombre: String(100)
- cargo: String(100)
- departamento: String(100)
- fecha_ingreso: Date

### Empresa
- id: Integer (Primary Key)
- nombre: String(100)
- sector: String(100)
- ubicacion: String(100)
- empleados: Integer

### Proyecto
- id: Integer (Primary Key)
- nombre: String(100)
- estado: String(50)
- fecha_inicio: Date
- fecha_fin: Date
- empresa_id: Integer (Foreign Key)

### Dato
- id: Integer (Primary Key)
- nombre: String(100)
- email: String(120)
- fecha: Date

## API Endpoints

### GET /api/{modelo}
Obtiene todos los registros del modelo especificado.

### POST /api/{modelo}
Crea un nuevo registro del modelo especificado.

### PUT /api/{modelo}/{id}
Actualiza un registro existente del modelo especificado.

### DELETE /api/{modelo}/{id}
Realiza un soft delete del registro especificado.

## Características Especiales

### Soft Delete
- Implementado a través de VisibilityMixin
- Campos: is_deleted, deleted_at
- Filtrado automático de registros eliminados

### DataTables
- Ordenamiento automático
- Búsqueda integrada
- Paginación
- Botones de acción por registro

### Formularios Dinámicos
- Generación automática basada en modelo
- Validación de tipos de datos
- Soporte para diferentes tipos de campos

## Desarrollo

### Agregar un Nuevo Modelo

1. Definir el modelo en `models.py`:
```python
class NuevoModelo(db.Model, VisibilityMixin):
    __tablename__ = 'nuevo_modelo'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    # ... otros campos
```

2. Implementar método seed:
```python
@classmethod
def seed(cls):
    # Lógica para generar datos de ejemplo
```

### Personalización de la Interfaz

1. Estilos personalizados en `custom-styles.css`
2. Lógica de interfaz en `main.js`
3. Estructura HTML en `index.html`

## Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request


Link del proyecto: [https://github.com/alejomejia/crud-flask-datatables](https://github.com/alejomejia/crud-flask-datatables)


## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/alejomejia/crud-flask-datatables.git
cd crud-flask-datatables
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# .flaskenv
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
```

5. Inicializar la base de datos:
```bash
flask init-db
```

## Uso

1. Iniciar el servidor:
```bash
flask run
```

2. Acceder a la aplicación:
```
http://localhost:5000
```

## Modelos de Datos

### Usuario
- id: Integer (Primary Key)
- nombre: String(100)
- cargo: String(100)
- departamento: String(100)
- fecha_ingreso: Date

### Empresa
- id: Integer (Primary Key)
- nombre: String(100)
- sector: String(100)
- ubicacion: String(100)
- empleados: Integer

### Proyecto
- id: Integer (Primary Key)
- nombre: String(100)
- estado: String(50)
- fecha_inicio: Date
- fecha_fin: Date
- empresa_id: Integer (Foreign Key)

### Dato
- id: Integer (Primary Key)
- nombre: String(100)
- email: String(120)
- fecha: Date

## API Endpoints

### GET /api/{modelo}
Obtiene todos los registros del modelo especificado.

### POST /api/{modelo}
Crea un nuevo registro del modelo especificado.

### PUT /api/{modelo}/{id}
Actualiza un registro existente del modelo especificado.

### DELETE /api/{modelo}/{id}
Realiza un soft delete del registro especificado.

## Características Especiales

### Soft Delete
- Implementado a través de VisibilityMixin
- Campos: is_deleted, deleted_at
- Filtrado automático de registros eliminados

### DataTables
- Ordenamiento automático
- Búsqueda integrada
- Paginación
- Botones de acción por registro

### Formularios Dinámicos
- Generación automática basada en modelo
- Validación de tipos de datos
- Soporte para diferentes tipos de campos

## Desarrollo

### Agregar un Nuevo Modelo

1. Definir el modelo en `models.py`:
```python
class NuevoModelo(db.Model, VisibilityMixin):
    __tablename__ = 'nuevo_modelo'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    # ... otros campos
```

2. Implementar método seed:
```python
@classmethod
def seed(cls):
    # Lógica para generar datos de ejemplo
```

### Personalización de la Interfaz

1. Estilos personalizados en `custom-styles.css`
2. Lógica de interfaz en `main.js`
3. Estructura HTML en `index.html`

## Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto


Link del proyecto: [https://github.com/usuario/proyecto](https://github.com/usuario/proyecto)


