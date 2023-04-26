from flask import request, jsonify, render_template, redirect, url_for, flash
from models.tables import Admin, SorteosGuardados
from database.db import db
from helpers.forms import LoginForm
from flask_login import login_user, logout_user, login_required, LoginManager
from utils import appscript
from utils import randomizer
import json
from flask import jsonify
from datetime import timedelta
from flask import make_response
from werkzeug.utils import secure_filename
from flask import current_app


login_manager = LoginManager()


def init_app(app):

    login_manager.init_app(app)

    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def home_page():
        return render_template('index.html')

    @app.route("/about")
    def about_page():
        return render_template('about.html')
    
    @app.route("/legal")
    def legal_page():
        return render_template('legal.html')

    @app.route("/estadisticas")
    def combinations_page():
        return render_template('combinations.html')
    
    @app.route("/jugada-aleatoria")
    def random_bet_page():
        return render_template('randomnumbers.html')

    @app.route("/login", methods=['GET', 'POST'])
    def login_page():
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = Admin.query.filter_by(name=form.name.data).first()
            if attempted_user and attempted_user.check_password(password_attempt=form.password.data):
                login_user(attempted_user)
                flash(f'You are logeed in as: {attempted_user.name}', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('Username or password incorrect', category='danger')
        return render_template('login.html', form=form)
    
    @app.route("/logout")
    def logout_page():
        logout_user()
        flash('You are now Logged Out, See you soon!', category='info')
        return render_template('index.html')
    
    
    @app.route("/admin")
    @login_required
    def admin_page():
        sorteos_string = obtener_sorteos_string()
        return render_template('admin.html', sorteos_string=sorteos_string)


    @app.errorhandler(404)
    def not_found(e):
        return render_template('notfound.html')
    

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))


    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template('forbiden.html')
    

    @app.route('/generar_sorteo', methods=['POST'])
    def generar_sorteo():
        seleccion = int(request.form['seleccionar-numero-combinatoria'])  # Obtiene el valor seleccionado por el usuario
        sorteo_generado = randomizer.random_numbers(seleccion)  # Genera los números aleatorios
        return render_template('randomnumbers.html', resultado_combinatoria=sorteo_generado)
    

    @app.route('/generar_combinaciones', methods=['POST'])
    def generar_combinaciones_route():
        seleccion = int(request.form['seleccionar-sorteo'])
        resultado_combinatoria = appscript.generar_combinaciones(seleccion)
        return render_template('combinations.html', sorteo_generado=resultado_combinatoria)
    

    def obtener_sorteos_string():
        sorteos_guardados = SorteosGuardados.query.all()
        sorteos = []

        for sorteo in sorteos_guardados:
            sorteos.append({sorteo.fecha: json.loads(sorteo.resultados)})

        return json.dumps(sorteos, indent=2)
    

    @app.route('/modificar_sorteos', methods=['POST'])
    @login_required
    def modificar_sorteos():
        try:
            data = json.loads(request.form['sorteos_modificados'])
            with current_app.app_context():
                for sorteo in data:
                    fecha, resultados = list(sorteo.items())[0]
                    sorteo_db = SorteosGuardados.query.filter_by(fecha=fecha).first()
                    if sorteo_db:
                        sorteo_db.resultados = json.dumps(resultados)
                    else:
                        nuevo_sorteo = SorteosGuardados(fecha=fecha, resultados=json.dumps(resultados))
                        db.session.add(nuevo_sorteo)
                db.session.commit()
            flash("Sorteos modificados correctamente.", "success")
            return redirect(url_for("admin_page"))
        except Exception as e:
            flash(f'Error al modificar sorteos: {str(e)}', 'danger')
            return redirect(url_for("admin_page"))


    @app.route('/subir_sorteo', methods=['POST'])
    @login_required
    def subir_sorteo():
        archivo_json = request.files['archivo_json']
        if archivo_json and archivo_json.filename.endswith('.json'):
            try:
                sorteos = json.load(archivo_json)
                with current_app.app_context():
                    # Eliminar registros existentes en la tabla SorteosGuardados
                    SorteosGuardados.query.delete()
                    db.session.commit()

                    # Guardar nuevos sorteos en la tabla SorteosGuardados
                    for sorteo in sorteos:
                        fecha, resultados = list(sorteo.items())[0]
                        nuevo_sorteo = SorteosGuardados(fecha=fecha, resultados=json.dumps(resultados))
                        db.session.add(nuevo_sorteo)
                    db.session.commit()
                flash("Sorteos subidos correctamente.", "success")
                return redirect(url_for("admin_page"))
            except Exception as e:
                flash(f'Error al procesar el archivo JSON: {str(e)}', 'danger')
                return redirect(url_for("admin_page"))
        else:
            flash('El archivo no es válido. Por favor, sube un archivo JSON.', 'danger')
            return redirect(url_for("admin_page"))

