from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import ORMExecuteState
from sqlalchemy.orm import with_loader_criteria
from datetime import datetime, timedelta
import random

db = SQLAlchemy()

class VisibilityMixin:
    """Mixin para implementar soft delete en los modelos."""

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)


@event.listens_for(db.session, 'do_orm_execute')
def _add_filtering_criteria(execute_state: ORMExecuteState):
    """
    Filtra automáticamente las consultas para excluir registros marcados como eliminados.

    Args:
        execute_state (ORMExecuteState): Estado de la ejecución ORM.

    Returns:
        None
    """
    if execute_state.is_select:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                VisibilityMixin,
                lambda cls: cls.is_deleted.is_(False),
                include_aliases=True,
            )
        )

class Usuario(db.Model, VisibilityMixin):
    """Modelo para representar usuarios en el sistema."""

    __tablename__ = 'usuarios'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.Date)

    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario.

        Returns:
            dict: Representación del usuario en formato diccionario.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cargo': self.cargo,
            'departamento': self.departamento,
            'fecha_ingreso': self.fecha_ingreso.strftime('%Y-%m-%d') if self.fecha_ingreso else None,
        }

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', cargo='{self.cargo}', departamento='{self.departamento}', fecha_ingreso='{self.fecha_ingreso}')>"

    @classmethod
    def seed(cls):
        """
        Genera datos de ejemplo para la tabla usuarios.

        Crea 20 usuarios con datos aleatorios utilizando combinaciones
        predefinidas de nombres, apellidos, cargos y departamentos.
        """
        nombres = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofia", "Miguel", "Isabel", "David"]
        apellidos = ["García", "Martínez", "López", "González", "Rodríguez", "Fernández", "Pérez", "Sánchez"]
        cargos = ["Desarrollador Senior", "Diseñador UX", "Project Manager", "Analista de Datos", "DevOps Engineer",
                 "Product Owner", "QA Engineer", "Frontend Developer", "Backend Developer", "Scrum Master"]
        departamentos = ["Tecnología", "Diseño", "Gestión de Proyectos", "Innovación", "Desarrollo",
                        "Calidad", "Operaciones", "Arquitectura", "Infraestructura"]

        for _ in range(20):
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
            fecha_ingreso = datetime.now() - timedelta(days=random.randint(0, 1000))

            usuario = cls(
                nombre=nombre,
                cargo=random.choice(cargos),
                departamento=random.choice(departamentos),
                fecha_ingreso=fecha_ingreso.date()
            )
            db.session.add(usuario)

class Empresa(db.Model, VisibilityMixin):
    """Modelo para representar empresas en el sistema."""

    __tablename__ = 'empresas'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100))
    ubicacion = db.Column(db.String(100))
    empleados = db.Column(db.Integer)
    proyectos = db.relationship('Proyecto', backref='empresa', lazy=True)

    def to_dict(self):
        """
        Convierte el objeto Empresa a un diccionario.

        Returns:
            dict: Representación de la empresa en formato diccionario.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sector': self.sector,
            'ubicacion': self.ubicacion,
            'empleados': self.empleados,
        }

    @classmethod
    def seed(cls):
        """
        Genera datos de ejemplo para la tabla empresas.

        Crea 10 empresas con datos aleatorios utilizando combinaciones
        predefinidas de nombres, sectores y ubicaciones.
        """
        nombres_empresas = [
            "TechSolutions", "Innovación Digital", "Desarrollo Global", "DataSys", "CloudTech",
            "Software Plus", "WebMasters", "AppDev", "SystemPro", "NetCorp"
        ]
        sectores = ["Tecnología", "Consultoría", "Software", "E-commerce", "Fintech",
                   "HealthTech", "EdTech", "IoT", "Inteligencia Artificial"]
        ubicaciones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao",
                      "Málaga", "Zaragoza", "Alicante", "Vigo", "San Sebastián"]

        for _ in range(10):
            empresa = cls(
                nombre=f"{random.choice(nombres_empresas)} {random.choice(['SA', 'SL', 'Inc', 'Corp'])}",
                sector=random.choice(sectores),
                ubicacion=random.choice(ubicaciones),
                empleados=random.randint(50, 500)
            )
            db.session.add(empresa)

class Proyecto(db.Model, VisibilityMixin):
    """Modelo para representar proyectos en el sistema."""

    __tablename__ = 'proyectos'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    def to_dict(self):
        """
        Convierte el objeto Proyecto a un diccionario.

        Returns:
            dict: Representación del proyecto en formato diccionario.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cliente': self.empresa.nombre if self.empresa else None,
            'estado': self.estado,
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d') if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else None,
        }

    @classmethod
    def seed(cls):
        """
        Genera datos de ejemplo para la tabla proyectos.

        Crea 30 proyectos con datos aleatorios y los asocia
        a empresas existentes en la base de datos.
        """
        nombres_proyectos = [
            "Sistema ERP", "App Móvil", "Portal Web", "Plataforma E-learning",
            "Sistema de Gestión", "Dashboard Analytics", "API REST", "Microservicios",
            "CRM Empresarial", "Plataforma IoT", "Sistema de Pagos", "Red Social",
            "Marketplace", "Backend Services", "Frontend SPA"
        ]
        estados = ["En Progreso", "Planificación", "Completado", "En Pausa", "Cancelado"]

        # Obtener todas las empresas
        empresas = Empresa.query.all()

        if empresas:
            for _ in range(30):
                fecha_inicio = datetime.now() - timedelta(days=random.randint(0, 365))
                fecha_fin = fecha_inicio + timedelta(days=random.randint(90, 365))

                proyecto = cls(
                    nombre=f"{random.choice(nombres_proyectos)} {random.randint(1, 100)}",
                    estado=random.choice(estados),
                    fecha_inicio=fecha_inicio.date(),
                    fecha_fin=fecha_fin.date(),
                    empresa_id=random.choice(empresas).id
                )
                db.session.add(proyecto)

class Dato(db.Model, VisibilityMixin):
    """Modelo para representar datos generales en el sistema."""

    __tablename__ = 'datos'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha = db.Column(db.Date)

    def to_dict(self):
        """
        Convierte el objeto Dato a un diccionario.

        Returns:
            dict: Representación del dato en formato diccionario.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha': self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
        }

    @classmethod
    def seed(cls):
        """
        Genera datos de ejemplo para la tabla datos.

        Crea 20 registros de datos con nombres, emails y fechas
        predefinidos.
        """
        nombres = ["Dato 1", "Dato 2", "Dato 3", "Dato 4", "Dato 5", "Dato 6", "Dato 7", "Dato 8", "Dato 9", "Dato 10", "Dato 11", "Dato 12", "Dato 13", "Dato 14", "Dato 15", "Dato 16", "Dato 17", "Dato 18", "Dato 19", "Dato 20"]
        emails = ["dato1@ejemplo.com", "dato2@ejemplo.com", "dato3@ejemplo.com", "dato4@ejemplo.com", "dato5@ejemplo.com", "dato6@ejemplo.com", "dato7@ejemplo.com", "dato8@ejemplo.com", "dato9@ejemplo.com", "dato10@ejemplo.com", "dato11@ejemplo.com", "dato12@ejemplo.com", "dato13@ejemplo.com", "dato14@ejemplo.com", "dato15@ejemplo.com", "dato16@ejemplo.com", "dato17@ejemplo.com", "dato18@ejemplo.com", "dato19@ejemplo.com", "dato20@ejemplo.com"]
        fechas = [datetime.now() for _ in range(20)]

        for nombre, email, fecha in zip(nombres, emails, fechas):
            dato = cls(nombre=nombre, email=email, fecha=fecha)
            db.session.add(dato)
        db.session.commit()