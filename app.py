from flask import Flask, render_template, jsonify, request
from models import db, Usuario, Empresa, Proyecto, Dato
from datetime import datetime
import os

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        # Configuración por defecto
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            DATABASE=os.path.join(app.instance_path, 'database.db')
        )
    else:
        # Cargar la configuración de prueba si se proporciona
        app.config.from_mapping(test_config)

    # Asegurar que existe el directorio de instancia
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar rutas
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/datos')
    def get_datos():
        datos = Dato.query.all()
        return jsonify({"data": [dato.to_dict() for dato in datos]})

    @app.route('/api/usuarios')
    def get_usuarios():
        usuarios = Usuario.query.all()
        return jsonify({"data": [usuario.to_dict() for usuario in usuarios]})

    @app.route('/api/empresas')
    def get_empresas():
        empresas = Empresa.query.all()
        return jsonify({"data": [empresa.to_dict() for empresa in empresas]})

    @app.route('/api/proyectos')
    def get_proyectos():
        proyectos = Proyecto.query.all()
        return jsonify({"data": [proyecto.to_dict() for proyecto in proyectos]})

    # Rutas para crear registros
    @app.route('/api/<string:modelo>', methods=['POST'])
    def crear_registro(modelo):
        try:
            datos = request.json

            if modelo == 'datos':
                nuevo = Dato(
                    nombre=datos['nombre'],
                    email=datos['email'],
                    fecha=datetime.strptime(datos['fecha'], '%Y-%m-%d').date() if datos.get('fecha') else None
                )
            elif modelo == 'usuarios':
                nuevo = Usuario(
                    nombre=datos['nombre'],
                    cargo=datos['cargo'],
                    departamento=datos['departamento'],
                    fecha_ingreso=datetime.strptime(datos['fecha_ingreso'], '%Y-%m-%d').date() if datos.get('fecha_ingreso') else None
                )
            elif modelo == 'empresas':
                nuevo = Empresa(
                    nombre=datos['nombre'],
                    sector=datos['sector'],
                    ubicacion=datos['ubicacion'],
                    empleados=datos['empleados']
                )
            elif modelo == 'proyectos':
                nuevo = Proyecto(
                    nombre=datos['nombre'],
                    estado=datos['estado'],
                    fecha_inicio=datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date() if datos.get('fecha_inicio') else None,
                    fecha_fin=datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date() if datos.get('fecha_fin') else None,
                    empresa_id=datos['empresa_id']
                )
            else:
                return jsonify({'error': 'Modelo no válido'}), 400

            db.session.add(nuevo)
            db.session.commit()
            return jsonify({'mensaje': 'Registro creado exitosamente'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    # Rutas para actualizar registros
    @app.route('/api/<string:modelo>/<int:id>', methods=['PUT'])
    def actualizar_registro(modelo, id):
        try:
            datos = request.json

            if modelo == 'datos':
                registro = Dato.query.get_or_404(id)
            elif modelo == 'usuarios':
                registro = Usuario.query.get_or_404(id)
            elif modelo == 'empresas':
                registro = Empresa.query.get_or_404(id)
            elif modelo == 'proyectos':
                registro = Proyecto.query.get_or_404(id)
            else:
                return jsonify({'error': 'Modelo no válido'}), 400

            for key, value in datos.items():
                if hasattr(registro, key):
                    if 'fecha' in key and value:
                        setattr(registro, key, datetime.strptime(value, '%Y-%m-%d').date())
                    else:
                        setattr(registro, key, value)

            db.session.commit()
            return jsonify({'mensaje': 'Registro actualizado exitosamente'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    # Rutas para eliminar registros
    @app.route('/api/<string:modelo>/<int:id>', methods=['DELETE'])
    def eliminar_registro(modelo, id):
        try:
            if modelo == 'datos':
                registro = Dato.query.get_or_404(id)
            elif modelo == 'usuarios':
                registro = Usuario.query.get_or_404(id)
            elif modelo == 'empresas':
                registro = Empresa.query.get_or_404(id)
            elif modelo == 'proyectos':
                registro = Proyecto.query.get_or_404(id)
            else:
                return jsonify({'error': 'Modelo no válido'}), 400
            # Implementación de soft delete
            if hasattr(registro, 'is_deleted'):
                setattr(registro, 'is_deleted', True)
            registro.deleted_at = datetime.now()
            db.session.commit()
            return jsonify({'mensaje': 'Registro eliminado exitosamente'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    # Comando para inicializar la base de datos
    @app.cli.command('init-db')
    def init_db_command():
        """Inicializar la base de datos."""
        init_db()
        print('Base de datos inicializada.')

    def init_db():
        with app.app_context():
            db.create_all()

            # Agregar datos de ejemplo si la base de datos está vacía
            if not Dato.query.first():
                Dato.seed()
                db.session.commit()

            if not Usuario.query.first():
                Usuario.seed()
                db.session.commit()

            if not Empresa.query.first():
                Empresa.seed()
                db.session.commit()

            if not Proyecto.query.first():
                Proyecto.seed()
                db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)