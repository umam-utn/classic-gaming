#Importamos las clases que vamos a utilizar
import os
from datetime import datetime
from os import remove
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph

# Inicializar app en el servidor
app = Flask(__name__)

# Llave
app.secret_key = os.urandom(24)

# Base de datos
app.config['MYSQL_HOST'] = 'localhost' #Nombre servidor de BD
app.config['MYSQL_USER'] = 'utn' #Nombre usuario BD
app.config['MYSQL_PASSWORD'] = 'utn21' #Contraseña Usuario BD
app.config['MYSQL_DB'] = 'cgaming' #Nombre BD
mysql = MySQL(app)

#Configurar ruta de imagenes
app.config['IMG_FOLDER']="./img"
#Configurar ruta de imagenes juegos
app.config['IMG_GM_FOLDER']="./img/juegos"
#Configurar ruta de imagenes subida por usuarios
app.config['IMG_USU_FOLDER']="./img/usuarios"

#Imagenes
@app.route('/img/<string:img>', methods = ['POST','GET'])
def imagenes(img):
	return send_from_directory(app.config["IMG_FOLDER"], img)
@app.route('/img/juegos/<string:img>', methods = ['POST','GET'])
def imagenes_juegos(img):
	return send_from_directory(app.config["IMG_GM_FOLDER"], img)
@app.route('/img/usuarios/<string:img>', methods = ['POST','GET'])
def imagenes_usuarios(img):
	return send_from_directory(app.config["IMG_USU_FOLDER"], img)

#Configurar archivos de imagen permitidos en input
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

def allowed_file(filename):
	return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

#Consultas BD SELECT
def consultaSelect(consulta):
    cur = mysql.connection.cursor() #Iniciar conexión BD
    cur.execute(consulta) #Consulta
    resultados = cur.fetchall() #Guardamos resultados de consulta
    cur.close() #Cerrar conexión BD
    return resultados #Retornamos resultado

def consultaDelete(consulta):
    cur = mysql.connection.cursor() #Iniciar conexión BD
    cur.execute(consulta) #Consulta
    mysql.connection.commit() #Confirmar operación
    cur.close() #Cerrar conexión BD

def sentenciaBD(sql,datos):
    cur = mysql.connection.cursor() #Iniciar conexión BD
    cur.execute(sql,datos) #Realizamos operación
    mysql.connection.commit() #Confirmar operación
    cur.close() #Cerrar conexión BD

def consultaGeneros():
    consulta = 'SELECT * FROM generos'
    generos = consultaSelect(consulta)
    return generos

def consultaConsolas():
    consulta = 'SELECT * FROM consolas'
    consolas = consultaSelect(consulta)
    return consolas

def consultaDesarrolladoras():
    consulta = 'SELECT * FROM desarrolladoras'
    desarrolladoras = consultaSelect(consulta)
    return desarrolladoras

def consultaIdiomas():
    consulta = 'SELECT * FROM idiomas'
    idiomas = consultaSelect(consulta)
    return idiomas

def consultaRegiones():
    consulta = 'SELECT * FROM regiones'
    regiones = consultaSelect(consulta)
    return regiones

def consultaUsuarios():
    consulta = 'SELECT * FROM usuarios WHERE id_usuario != 1'
    usuarios = consultaSelect(consulta)
    return usuarios

def consultaRoles():
    consulta = 'SELECT * FROM roles'
    roles = consultaSelect(consulta)
    return roles

#Detalles Sesión
def registrar_sesion(id,correo,rol):
    cerrar_sesion()
    session['id'] = id
    session['correo'] = correo
    session['rol'] = rol

def cerrar_sesion():
    session.clear()

@app.before_request
def session_management():
  session.permanent = True

# Ruta Index
@app.route('/')
def index():
    sql = '''SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa 
        FROM juegos j, consolas c, idiomas i, desarrolladoras d
        WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora'''
    juegos = consultaSelect(sql)
    sql = '''SELECT j.id_juego, j.nombre, j.foto, j.precio, c.nombre_cons
        FROM juegos j, consolas c
        WHERE j.id_consola = c.id_consola ORDER BY id_juego DESC LIMIT 3'''
    ultimos = consultaSelect(sql)
    generos = consultaGeneros()
    consolas = consultaConsolas()
    desarrolladoras = consultaDesarrolladoras()
    idiomas = consultaIdiomas()
    return render_template('usuarios/index.html', juegos = juegos, ultimos = ultimos,generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, idiomas = idiomas)

#Detalles juego
@app.route('/detalles_juego/<int:id>', methods = ['POST','GET'])
def detalles_juego(id):
    sql = '''SELECT j.id_juego, j.nombre, j.foto, j.foto_dos, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa, r.nombre_reg 
        FROM juegos j, consolas c, idiomas i, desarrolladoras d, regiones r
        WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND j.id_region = r.id_region AND id_juego = {0}'''.format(id)
    juegos = consultaSelect(sql)
    generos = consultaGeneros()
    consolas = consultaConsolas()
    desarrolladoras = consultaDesarrolladoras()
    idiomas = consultaIdiomas()
    return render_template('usuarios/detalles.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, idiomas = idiomas)

# Ruta Resultados
@app.route('/resultados', methods = ['POST','GET'])
def resultados():
    datos = request.form['busqueda']
    sql = "SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa FROM juegos j, consolas c, idiomas i, desarrolladoras d WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND (j.nombre LIKE '%"+datos+"%' OR j.descripcion LIKE '%"+datos+"%' OR i.nombre_idioma LIKE '%"+datos+"%' OR c.nombre_cons LIKE '%"+datos+"%' OR d.nombre_desa LIKE '%"+datos+"%');"
    juegos = consultaSelect(sql)
    generos = consultaGeneros()
    consolas = consultaConsolas()
    desarrolladoras = consultaDesarrolladoras()
    idiomas = consultaIdiomas()
    return render_template('usuarios/resultados.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, idiomas = idiomas)

# Ruta Resultados BTN
@app.route('/resultados/<string:opt>/<int:id>', methods = ['POST','GET'])
def resultados_btn(opt,id):
    if opt == "consolas":
        inf = "SELECT * FROM consolas WHERE id_consola = {0};".format(id)
        info = consultaSelect(inf)
        sql = "SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa FROM juegos j, consolas c, idiomas i, desarrolladoras d WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND j.id_consola = {0};".format(id)
    if opt == "generos":
        inf = "SELECT * FROM generos WHERE id_genero = {0};".format(id)
        info = consultaSelect(inf)
        sql = "SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa FROM juegos j, consolas c, idiomas i, desarrolladoras d WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND j.id_genero = {0};".format(id)
    if opt == "idiomas":
        inf = "SELECT * FROM idiomas WHERE id_idioma = {0};".format(id)
        info = consultaSelect(inf)
        sql = "SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa FROM juegos j, consolas c, idiomas i, desarrolladoras d WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND j.id_idioma = {0};".format(id)
    if opt == "desarrolladoras":
        inf = "SELECT * FROM desarrolladoras WHERE id_desarrolladora = {0};".format(id)
        info = consultaSelect(inf)
        sql = "SELECT j.id_juego, j.nombre, j.foto, j.descripcion, j.lanzamiento, j.precio, c.nombre_cons, i.nombre_idioma, d.nombre_desa FROM juegos j, consolas c, idiomas i, desarrolladoras d WHERE j.id_consola = c.id_consola AND j.id_idioma = i.id_idioma AND j.id_desarrolladora = d.id_desarrolladora AND j.id_desarrolladora = {0};".format(id)
    juegos = consultaSelect(sql)
    generos = consultaGeneros()
    consolas = consultaConsolas()
    desarrolladoras = consultaDesarrolladoras()
    idiomas = consultaIdiomas()
    return render_template('usuarios/resultados.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, idiomas = idiomas, info = info)

#Ruta Terminos y condiciones
@app.route('/terminos_condiciones')
def terminos():
    return render_template('usuarios/terminos.html')

#Ruta Contacto
@app.route('/contacto')
def contacto():
    return render_template('usuarios/contacto.html')

#Ruta login
@app.route('/login')
def login():
    if 'rol' in session:
        if session['rol'] == 'adm':
            return render_template('administrador/index.html')
        else:
            return redirect(url_for('index'))
    else:
        return render_template('usuarios/ingresar.html')

#Registro Usuario
@app.route('/registro', methods = ['POST','GET'])
def registro():
    if request.method == "POST":
        #Recibimos datos del formulario
        correo = request.form['correo-usu']
        nombre = request.form['nom-usu']
        apellido = request.form['ap-usu']
        contra = request.form['contra-usu']
        contra2 = request.form['contra-r-usu']
        estado = request.form['estado-usu']
        tel = request.form['tel-usu']
        avatar = 'default.jpg'
        hash_contra = genph(contra)
        now = datetime.now()
        rol = 2
        fecha = "{}".format(now.year)+"-"+"{}".format(now.month)+"-"+"{}".format(now.day)
        #Validamos si ya existe un correo asi
        sqlValida ='SELECT COUNT(id_usuario) FROM usuarios WHERE correo = "'+correo+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = """INSERT INTO usuarios 
                    (nombre_usu,ape_usu,correo,contra,avatar,estado,fecha_reg,id_rol,telefono) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);"""
            datos = (nombre, apellido, correo, hash_contra, avatar, estado, fecha, rol, tel)
            sentenciaBD(sql,datos)
            flash('Usuario registrado ya puede iniciar sesión.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El correo ya se encuentra registrado.') #Mensaje de error
    return redirect(url_for('login')) #Redirecciona a la página login

#Ingresar
@app.route('/ingresar', methods = ['POST','GET'])
def ingresar():
    if request.method == "POST":
        #Recibimos datos del formulario
        correo = request.form['correo-usu']
        contra = request.form['contra-usu-login']
        sqlValida ='SELECT COUNT(id_usuario) FROM usuarios WHERE correo = "'+correo+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            flash('El correo no se encuentra registrado.') #Mensaje de error
            return redirect(url_for('login')) #Redirecciona al perfil
        if existe[0][0] > 0: # Si encontro otro registro igual
            sql ='SELECT u.id_usuario, u.nombre_usu, u.contra, u.correo, r.nombre_rol FROM usuarios u, roles r WHERE correo = "'+correo+'" AND u.id_rol = r.id_rol;'
            datos = consultaSelect(sql)
            idusu = datos[0][0]
            nomusu = datos[0][1]
            conusu = datos[0][2]
            correousu = datos[0][3]
            rolusu = datos[0][4]
            if rolusu == "NA":
                flash('Su cuenta se encuentra bloqueada, contacte con un administrador.') #Mensaje error
                return redirect(url_for('index')) #Redirecciona al index
            else:
                if checkph(conusu, contra):
                    registrar_sesion(idusu,correousu,rolusu)
                    if rolusu == "adm":
                        return redirect(url_for('adm_index')) #Redirecciona al perfil
                    else:
                        flash('Bienvenido ' + nomusu + '.') #Mensaje bienvenida
                        return redirect(url_for('index')) #Redirecciona al inicio
                else:
                    flash('Contraseña invalida.') #Mensaje error
                    return redirect(url_for('login')) #Redirecciona al login

#Cerrar sesion
@app.route('/salir')
def salir():
    cerrar_sesion()
    flash('Regrese pronto.') #Mensaje despedida
    return redirect(url_for('index')) #Redirecciona al index

#Ruta perfil
@app.route('/perfil')
def perfil():
    if 'id' in session:
        id = session['id']
        sql = "SELECT * FROM usuarios WHERE id_usuario = {0};".format(id)
        usuarios = consultaSelect(sql)
        if session['rol'] == 'adm':
            return render_template('administrador/perfil.html', usuarios = usuarios)
        if session['rol'] == 'usr':
            return render_template('usuarios/perfil.html', usuarios = usuarios)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza Perfil
@app.route('/update_perfil/<id>', methods=['POST'])
def update_perfil(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        correo = request.form['correo-usu']
        nombre = request.form['nom-usu']
        apellido = request.form['ap-usu']
        contra = request.form['contra-usu']
        contra2 = request.form['contra-r-usu']
        estado = request.form['estado-usu']
        tel = request.form['tel-usu']
        c_original = request.form['conf-contra-ori']
        original = request.form['contra-ori']
        avatar = request.files['avatar-usu']
        hash_contra = genph(contra)
        if checkph(original, c_original):
            #Validamos si ya existe un correo asi
            sqlValida ='SELECT COUNT(id_usuario) FROM usuarios WHERE correo = "'+correo+'" AND id_usuario != "'+id+'";'
            existe = consultaSelect(sqlValida)
            if existe[0][0] < 1: #Si no encontro otro registro igual
                sql = """UPDATE usuarios
                    SET nombre_usu = %s, 
                    ape_usu = %s, 
                    correo = %s, 
                    estado = %s,  
                    telefono = %s 
                    WHERE id_usuario = %s;"""
                datos = (nombre, apellido, correo, estado, tel, id)
                sentenciaBD(sql,datos)
                if avatar.filename != "" and allowed_file(avatar.filename):
                    sqlBuscaImg ='SELECT avatar FROM usuarios WHERE id_usuario = "'+id+'";'
                    data = consultaSelect(sqlBuscaImg)
                    img = data[0][0]
                    ext = avatar.filename.rsplit(".", 1)[1].lower()
                    now = datetime.now()
                    fecha = "{}".format(now.year)+"-"+"{}".format(now.month)+"-"+"{}".format(now.day)
                    avatar.filename = fecha+'-avatar-' + id + '.'+ext
                    if img != 'default.jpg':
                        os.remove("./img/usuarios/{}".format(img)) #Borra imagen vieja del servidor
                    avatar.save(os.path.join(app.config['IMG_USU_FOLDER'], avatar.filename))
                    sql = "UPDATE usuarios SET avatar = %s WHERE id_usuario = %s;"
                    datos = (avatar.filename, id)
                    sentenciaBD(sql,datos)
                if contra != "" and contra == contra2:
                    sql = "UPDATE usuarios SET contra = %s WHERE id_usuario = %s;"
                    datos = (hash_contra, id)
                    sentenciaBD(sql,datos)
                else:
                    flash('La contraseña no se modifico.') #Mensaje de no cambio de contraseña
                flash('Cuenta actualizada.') #Mensaje de Confirmación
            if existe[0][0] > 0: # Si encontro otro registro igual
                flash('El correo ingresado ya se encuentra registrado con otra persona.') #Mensaje de error
        else:
            flash('La contraseña actual no coincide.') #Mensaje de error
    return redirect(url_for('perfil')) #Redirecciona a la página perfil


#Ruta Index ADM
@app.route('/administrador')
def adm_index():
    if 'rol' in session:
        if session['rol'] == 'adm':
            return render_template('administrador/index.html')
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Catalogo Géneros
@app.route("/administrar_generos")
def generos():
    if 'rol' in session:
        if session['rol'] == 'adm':
            generos = consultaGeneros()
            return render_template('administrador/generos.html', generos = generos)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Agrega Géneros
@app.route("/add_genero", methods=['POST'])
def add_genero():
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-genero']
        desc = request.form['desc-genero']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_genero) FROM generos WHERE nombre_gen = "'+nombre+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "INSERT INTO generos (nombre_gen, descripcion_gen) VALUES (%s, %s);"
            datos = (nombre, desc)
            sentenciaBD(sql,datos)
            flash('Género registrado.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El Género no se agrego debido a que ya se encuentra registrado.') #Mensaje de error
    return redirect(url_for('generos')) #Redirecciona a la página géneros

#Elimina Género
@app.route("/delete_genero/<int:id>", methods = ['POST','GET'])
def delete_genero(id):
    #Validamos si existen registros en juegos
    sqlValida = 'SELECT COUNT(id_genero) FROM juegos WHERE id_genero = {0};'.format(id)
    existe = consultaSelect(sqlValida)
    if existe[0][0] < 1: #Si no encontro registros en juegos
        sql = 'DELETE FROM generos WHERE id_genero = {0};'.format(id)
        consultaDelete(sql)
        flash('Género borrado de manera correcta.') #Mensaje de confirmación
    if existe[0][0] > 0: # Si encontro registros en la tabla juegos
        flash('El Género no se puede borrar debido a que está asignado a uno o más juegos.') #Mensaje de Error
    return redirect(url_for('generos')) #Redirecciona a la página géneros

#Editar Género
@app.route("/edit_genero/<int:id>", methods = ['POST','GET'])
def edit_genero(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM generos WHERE id_genero = {0};'.format(id)
            generos = consultaSelect(sql)
            return render_template('administrador/generos-edit.html', generos = generos)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza Género
@app.route('/update_genero/<id>', methods=['POST'])
def update_genero(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-genero']
        desc = request.form['desc-genero']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_genero) FROM generos WHERE nombre_gen = "'+nombre+'" AND id_genero != "'+id+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "UPDATE generos SET nombre_gen = %s, descripcion_gen = %s WHERE id_genero = %s;"
            datos = (nombre, desc, id)
            sentenciaBD(sql,datos)
            flash('Género actualizado.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El Género no se actualizó debido a que ya se encuentra registrado otro con el mismo nombre.') #Mensaje de error
    return redirect(url_for('generos')) #Redirecciona a la página géneros

#Busqueda Géneros
@app.route("/busqueda_generos", methods=['POST'])
def busqueda_generos():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = "SELECT * FROM generos WHERE nombre_gen LIKE '%"+datos+"%';"
            generos  = consultaSelect(sql)
            return render_template('administrador/generos.html', generos = generos)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Catalogo Consolas
@app.route("/administrar_consolas")
def consolas():
    if 'rol' in session:
        if session['rol'] == 'adm':
            consolas = consultaConsolas()
            return render_template('administrador/consolas.html', consolas = consolas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Agrega Consola
@app.route("/add_consola", methods=['POST'])
def add_consola():
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-consola']
        desc = request.form['desc-consola']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_consola) FROM consolas WHERE nombre_cons = "'+nombre+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "INSERT INTO consolas (nombre_cons, descripcion_cons) VALUES (%s, %s);"
            datos = (nombre, desc)
            sentenciaBD(sql,datos)
            flash('Consola registrada.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('La consola no se agrego debido a que ya se encuentra registrada.') #Mensaje de error
    return redirect(url_for('consolas')) #Redirecciona a la página consolas

#Elimina Consola
@app.route("/delete_consola/<id>", methods = ['POST','GET'])
def delete_consola(id):
    #Validamos si existen registros en Juegos
    sqlValida = 'SELECT COUNT(id_consola) FROM juegos WHERE id_consola = {0};'.format(id)
    existe = consultaSelect(sqlValida)
    if existe[0][0] < 1: #Si no encontro registros en Juegos
        sql = 'DELETE FROM consolas WHERE id_consola = {0};'.format(id)
        consultaDelete(sql)
        flash('Consola borrada de manera correcta.') #Mensaje de confirmación
    if existe[0][0] > 0: # Si encontro registros en la tabla Juegos
        flash('La consola no se puede borrar debido a que está asignada a uno o más juegos.') #Mensaje de Error
    return redirect(url_for('consolas')) #Redirecciona a la página consolas

#Editar Consola
@app.route("/edit_consola/<int:id>", methods = ['POST','GET'])
def edit_consola(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM consolas WHERE id_consola = {0};'.format(id)
            consolas = consultaSelect(sql)
            return render_template('administrador/consolas-edit.html', consolas = consolas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza consolas
@app.route('/update_consola/<id>', methods=['POST'])
def update_consola(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-consola']
        desc = request.form['desc-consola']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_consola) FROM consolas WHERE nombre_cons = "'+nombre+'" AND id_consola != "'+id+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "UPDATE consolas SET nombre_cons = %s, descripcion_cons = %s WHERE id_consola = %s;"
            datos = (nombre, desc, id)
            sentenciaBD(sql,datos)
            flash('Consola actualizada.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('La consola no se actualizó debido a que ya se encuentra registrada otra con el mismo nombre.') #Mensaje de error
    return redirect(url_for('consolas')) #Redirecciona a la página consolas

#Busqueda Consolas
@app.route("/busqueda_consolas", methods=['POST'])
def busqueda_consolas():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = "SELECT * FROM consolas WHERE nombre_cons LIKE '%"+datos+"%';"
            consolas = consultaSelect(sql)
            return render_template('administrador/consolas.html', consolas = consolas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Catalogo Desarrolladoras
@app.route("/administrar_desarrolladoras")
def desarrolladoras():
    if 'rol' in session:
        if session['rol'] == 'adm':
            desarrolladoras = consultaDesarrolladoras()
            return render_template('administrador/desarrolladoras.html', desarrolladoras = desarrolladoras)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Agrega Desarrolladora
@app.route("/add_desarrolladora", methods=['POST'])
def add_desarrolladora():
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-desarrolladora']
        desc = request.form['desc-desarrolladora']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_desarrolladora) FROM desarrolladoras WHERE nombre_desa = "'+nombre+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "INSERT INTO desarrolladoras (nombre_desa, descripcion_desa) VALUES (%s, %s);"
            datos = (nombre, desc)
            sentenciaBD(sql,datos)
            flash('Desarrolladora registrada.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('La desarrolladora no se agrego debido a que ya se encuentra registrada.') #Mensaje de error
    return redirect(url_for('desarrolladoras')) #Redirecciona a la página desarrolladoras

#Elimina Desarrolladora
@app.route("/delete_desarrolladora/<id>", methods = ['POST','GET'])
def delete_desarrolladora(id):
    #Validamos si existen registros en Juegos
    sqlValida = 'SELECT COUNT(id_desarrolladora) FROM juegos WHERE id_desarrolladora = {0};'.format(id)
    existe = consultaSelect(sqlValida)
    if existe[0][0] < 1: #Si no encontro registros en Juegos
        sql = 'DELETE FROM desarrolladoras WHERE id_desarrolladora = {0};'.format(id)
        consultaDelete(sql)
        flash('Desarrolladora borrada de manera correcta.') #Mensaje de confirmación
    if existe[0][0] > 0: # Si encontro registros en la tabla Juegos
        flash('La desarrolladora no se puede borrar debido a que está asignada a uno o más juegos.') #Mensaje de Error
    return redirect(url_for('desarrolladoras')) #Redirecciona a la página desarrolladoras

#Editar Desarrolladora
@app.route("/edit_desarrolladora/<int:id>", methods = ['POST','GET'])
def edit_desarrolladora(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM desarrolladoras WHERE id_desarrolladora = {0};'.format(id)
            desarrolladoras = consultaSelect(sql)
            return render_template('administrador/desarrolladoras-edit.html', desarrolladoras = desarrolladoras)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza desarrolladora
@app.route('/update_desarrolladora/<id>', methods=['POST'])
def update_desarrolladora(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-desarrolladora']
        desc = request.form['desc-desarrolladora']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_desarrolladora) FROM desarrolladoras WHERE nombre_desa = "'+nombre+'" AND id_desarrolladora != "'+id+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "UPDATE desarrolladoras SET nombre_desa = %s, descripcion_desa = %s WHERE id_desarrolladora = %s;"
            datos = (nombre, desc, id)
            sentenciaBD(sql,datos)
            flash('Desarrolladora actualizada.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('La desarrolladora no se actualizó debido a que ya se encuentra registrada otra con el mismo nombre.') #Mensaje de error
    return redirect(url_for('desarrolladoras')) #Redirecciona a la página desarrolladoras

#Busqueda Desarrolladoras
@app.route("/busqueda_desarrolladoras", methods=['POST'])
def busqueda_desarrolladoras():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = "SELECT * FROM desarrolladoras WHERE nombre_desa LIKE '%"+datos+"%';"
            desarrolladoras = consultaSelect(sql)
            return render_template('administrador/desarrolladoras.html', desarrolladoras = desarrolladoras)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Catalogo Idiomas
@app.route("/administrar_idiomas")
def idiomas():
    if 'rol' in session:
        if session['rol'] == 'adm':
            idiomas = consultaIdiomas()
            return render_template('administrador/idiomas.html', idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Agrega Idiomas
@app.route("/add_idioma", methods=['POST'])
def add_idioma():
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-idioma']
        desc = request.form['desc-idioma']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_idioma) FROM idiomas WHERE nombre_idioma = "'+nombre+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "INSERT INTO idiomas (nombre_idioma, descripcion_idioma) VALUES (%s, %s);"
            datos = (nombre, desc)
            sentenciaBD(sql,datos)
            flash('Idioma registrado.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El idioma no se agrego debido a que ya se encuentra registrado.') #Mensaje de error
    return redirect(url_for('idiomas')) #Redirecciona a la página consolas

#Elimina Idioma
@app.route("/delete_idioma/<int:id>", methods = ['POST','GET'])
def delete_idioma(id):
    #Validamos si existen registros en juegos
    sqlValida = 'SELECT COUNT(id_idioma) FROM juegos WHERE id_idioma = {0};'.format(id)
    existe = consultaSelect(sqlValida)
    if existe[0][0] < 1: #Si no encontro registros en juegos
        sql = 'DELETE FROM idiomas WHERE id_idioma = {0};'.format(id)
        consultaDelete(sql)
        flash('Idioma borrado de manera correcta.') #Mensaje de confirmación
    if existe[0][0] > 0: # Si encontro registros en la tabla detalles
        flash('El idioma no se puede borrar debido a que está asignado a uno o más juegos.') #Mensaje de Error
    return redirect(url_for('idiomas')) #Redirecciona a la página idiomas

#Editar Idioma
@app.route("/edit_idioma/<int:id>", methods = ['POST','GET'])
def edit_idioma(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM idiomas WHERE id_idioma = {0};'.format(id)
            idiomas = consultaSelect(sql)
            return render_template('administrador/idiomas-edit.html', idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza idioma
@app.route('/update_idioma/<id>', methods=['POST'])
def update_idioma(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-idioma']
        desc = request.form['desc-idioma']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_idioma) FROM idiomas WHERE nombre_idioma = "'+nombre+'" AND id_idioma != "'+id+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = "UPDATE idiomas SET nombre_idioma = %s, descripcion_idioma = %s WHERE id_idioma = %s;"
            datos = (nombre, desc, id)
            sentenciaBD(sql,datos)
            flash('Idioma actualizado.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El idioma no se actualizó debido a que ya se encuentra registrado otro con el mismo nombre.') #Mensaje de error
    return redirect(url_for('idiomas')) #Redirecciona a la página consolas

#Busqueda Idiomas
@app.route("/busqueda_idiomas", methods=['POST'])
def busqueda_idiomas():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = "SELECT * FROM idiomas WHERE nombre_idioma LIKE '%"+datos+"%';"
            idiomas = consultaSelect(sql)
            return render_template('administrador/idiomas.html', idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Catalogo Juegos
@app.route("/administrar_juegos")
def juegos():
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = '''SELECT j.id_juego, j.nombre, j.descripcion, c.nombre_cons 
                FROM juegos j, consolas c
                WHERE j.id_consola = c.id_consola'''
            juegos = consultaSelect(sql)
            generos = consultaGeneros()
            consolas = consultaConsolas()
            desarrolladoras = consultaDesarrolladoras()
            regiones = consultaRegiones()
            idiomas = consultaIdiomas()
            return render_template('administrador/juegos.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, regiones = regiones, idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Agrega Juegos
@app.route("/add_juego", methods=['POST'])
def add_juego():
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-juego']
        consola = request.form['consola-juego']
        lanzamiento = request.form['lanzamiento-juego']
        precio = request.form['precio-juego']
        desc = request.form['desc-juego']
        desa = request.form['desa-juego']
        reg = request.form['reg-juego']
        genero = request.form['genero-juego']
        idioma = request.form['idioma-juego']
        stock = request.form['stock-juego']
        status = 1
        #Validamos la existencia de las fotografías y las guardamos
        if "foto-juego" not in request.files:
            flash("Error al recuperar el archivo fotografía 1")
            return redirect(url_for('juegos')) #Redirecciona a la página mantener
        foto1 = request.files['foto-juego']
        if "fotodos-juego" not in request.files:
            flash("Error al recuperar el archivo fotografía 2")
            return redirect(url_for('juegos')) #Redirecciona a la página mantener
        foto2 = request.files['fotodos-juego']
        #Valida el tipo de archivo
        if allowed_file(foto1.filename) and allowed_file(foto2.filename):
            #Validamos si ya existe un registro asi
            sqlValida ='SELECT COUNT(id_juego) FROM juegos WHERE nombre = "'+nombre+'";'
            existe = consultaSelect(sqlValida)
            if existe[0][0] < 1: #Si no encontro otro registro igual
                #obtenemos fecha actual
                now = datetime.now()
                #Cambiamos nombre a las fotografías
                nuevoNombre = "{}".format(now.day)+"-"+"{}".format(now.month)+"-"+"{}".format(now.year)+"-"+"{}".format(now.hour)+"-"+"{}".format(now.minute)+"-"+"{}".format(now.second)
                ext = foto1.filename.rsplit(".", 1)[1].lower()
                foto1.filename = nuevoNombre + '-foto-01.'+ext
                ext = foto2.filename.rsplit(".", 1)[1].lower()
                foto2.filename = nuevoNombre + '-foto-02.'+ext
                #Guardamos las fotografías en el servidor
                foto1.save(os.path.join(app.config['IMG_GM_FOLDER'], foto1.filename))
                foto2.save(os.path.join(app.config['IMG_GM_FOLDER'], foto2.filename))
                sql = """
                    INSERT 
                    INTO juegos (nombre, descripcion, precio, foto, foto_dos, lanzamiento, stock, id_consola, id_desarrolladora, id_region, id_genero, id_idioma, estado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                datos = (nombre, desc, precio, foto1.filename, foto2.filename, lanzamiento, stock, consola, desa, reg, genero, idioma, status)
                sentenciaBD(sql,datos)
                flash('Juego registrado.') #Mensaje de Confirmación
                return redirect(url_for('juegos')) #Redirecciona a la página juegos
            if existe[0][0] > 0: # Si encontro otro registro igual
                flash('El juego no se agrego debido a que ya se encuentra registrado.') #Mensaje de error
                return redirect(url_for('juegos')) #Redirecciona a la página juegos
        flash("Imagen no valida.")
        return redirect(url_for('juegos')) #Redirecciona a la página juegos

#Elimina Juego
@app.route("/delete_juego/<int:id>", methods = ['POST','GET'])
def delete_juego(id):
    #Recuperamos nombre de imágenes
    images = 'SELECT foto, foto_dos FROM juegos WHERE id_juego = {0};'.format(id)
    data = consultaSelect(images)
    foto1 = data[0][0]
    foto2 = data[0][1]
    #Realizamos el borrado
    sql = 'DELETE FROM juegos WHERE id_juego = {0};'.format(id)
    consultaDelete(sql)
    #Removemos imagenes del servidor
    os.remove("./img/juegos/{}".format(foto1)) #Borra foto 1 del servidor
    os.remove("./img/juegos/{}".format(foto2)) #Borra foto 2 del servidor
    flash('Juego borrado de manera correcta.') #Mensaje de confirmación
    return redirect(url_for('juegos')) #Redirecciona a la página desarrolladoras

#Editar Juego
@app.route("/edit_juego/<int:id>", methods = ['POST','GET'])
def edit_juego(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM juegos WHERE id_juego = {0};'.format(id)
            juegos = consultaSelect(sql)
            generos = consultaGeneros()
            consolas = consultaConsolas()
            desarrolladoras = consultaDesarrolladoras()
            regiones = consultaRegiones()
            idiomas = consultaIdiomas()
            return render_template('administrador/juegos-edit.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, regiones = regiones, idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza Juego
@app.route('/update_juego/<id>', methods=['POST'])
def update_juego(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        nombre = request.form['nombre-juego']
        consola = request.form['consola-juego']
        lanzamiento = request.form['lanzamiento-juego']
        precio = request.form['precio-juego']
        desc = request.form['desc-juego']
        desa = request.form['desa-juego']
        reg = request.form['reg-juego']
        genero = request.form['genero-juego']
        idioma = request.form['idioma-juego']
        stock = request.form['stock-juego']
        foto1 = request.files['foto-juego']
        foto2 = request.files['fotodos-juego']
        #Validamos si ya existe un registro asi
        sqlValida ='SELECT COUNT(id_juego) FROM juegos WHERE nombre = "'+nombre+'" AND id_juego != "'+id+'";'
        existe = consultaSelect(sqlValida)
        if existe[0][0] < 1: #Si no encontro otro registro igual
            sql = """UPDATE juegos 
            SET nombre = %s, 
            descripcion = %s, 
            precio = %s, 
            lanzamiento = %s,  
            stock = %s, 
            id_consola = %s, 
            id_desarrolladora = %s, 
            id_region = %s,
            id_genero = %s, 
            id_idioma = %s 
            WHERE id_juego = %s;"""
            datos = (nombre, desc, precio, lanzamiento, stock, consola, desa, reg, genero, idioma, id)
            sentenciaBD(sql,datos)
            #obtenemos fecha actual
            now = datetime.now()
            #Verificamos si cambio la foto 1
            if foto1.filename != "" and allowed_file(foto1.filename):
                sqlBuscaImg ='SELECT foto FROM juegos WHERE id_juego = "'+id+'";'
                data = consultaSelect(sqlBuscaImg)
                img = data[0][0]
                nuevoNombre = "{}".format(now.day)+"-"+"{}".format(now.month)+"-"+"{}".format(now.year)+"-"+"{}".format(now.hour)+"-"+"{}".format(now.minute)+"-"+"{}".format(now.second)
                ext = foto1.filename.rsplit(".", 1)[1].lower()
                foto1.filename = nuevoNombre + '-foto-01.'+ext
                os.remove("./img/juegos/{}".format(img)) #Borra imagen vieja del servidor
                foto1.save(os.path.join(app.config['IMG_GM_FOLDER'], foto1.filename))
                sql = "UPDATE juegos SET foto = %s WHERE id_juego = %s;"
                datos = (foto1.filename, id)
                sentenciaBD(sql,datos)
            #Verificamos si cambio la foto 2
            if foto2.filename != "" and allowed_file(foto2.filename):
                sqlBuscaImg2 ='SELECT foto_dos FROM juegos WHERE id_juego = "'+id+'";'
                data = consultaSelect(sqlBuscaImg2)
                img = data[0][0]
                nuevoNombre = "{}".format(now.day)+"-"+"{}".format(now.month)+"-"+"{}".format(now.year)+"-"+"{}".format(now.hour)+"-"+"{}".format(now.minute)+"-"+"{}".format(now.second)
                ext = foto2.filename.rsplit(".", 1)[1].lower()
                foto2.filename = nuevoNombre + '-foto-02.'+ext
                os.remove("./img/juegos/{}".format(img)) #Borra imagen vieja del servidor
                foto2.save(os.path.join(app.config['IMG_GM_FOLDER'], foto2.filename))
                sql = "UPDATE juegos SET foto_dos = %s WHERE id_juego = %s;"
                datos = (foto2.filename, id)
                sentenciaBD(sql,datos)
            flash('Juego actualizado.') #Mensaje de Confirmación
        if existe[0][0] > 0: # Si encontro otro registro igual
            flash('El Juego no se actualizó debido a que ya se encuentra registrado otro con el mismo nombre.') #Mensaje de error
    return redirect(url_for('juegos')) #Redirecciona a la página consolas

#Busqueda Juegos
@app.route("/busqueda_juegos", methods=['POST'])
def busqueda_juegos():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = '''SELECT j.id_juego, j.nombre, j.descripcion, c.nombre_cons 
                FROM juegos j, consolas c
                WHERE j.id_consola = c.id_consola AND j.nombre LIKE "%'''+datos+'''%"'''
            juegos = consultaSelect(sql)
            generos = consultaGeneros()
            consolas = consultaConsolas()
            desarrolladoras = consultaDesarrolladoras()
            regiones = consultaRegiones()
            idiomas = consultaIdiomas()
            return render_template('administrador/juegos.html', juegos = juegos, generos = generos, consolas = consolas, desarrolladoras = desarrolladoras, regiones = regiones, idiomas = idiomas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Administra usuarios
@app.route('/administra_usuarios')
def administra_usuarios():
    if 'rol' in session:
        if session['rol'] == 'adm':
            usuarios = consultaUsuarios()
            return render_template('administrador/usuarios.html', usuarios = usuarios)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Privilegios Usuario
@app.route("/privilegios_usu/<int:id>", methods = ['POST','GET'])
def privilegios_usu(id):
    if 'rol' in session:
        if session['rol'] == 'adm':
            sql = 'SELECT * FROM usuarios WHERE id_usuario = {0};'.format(id)
            usuarios = consultaSelect(sql)
            roles = consultaRoles()
            return render_template('administrador/usuarios-edit.html', usuarios = usuarios, roles = roles)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Actualiza Privilegios
@app.route('/update_privilegios/<id>', methods=['POST'])
def update_privilegios(id):
    if request.method == "POST": #Si los datos se reciben con el metodo POST
        #Recibimos datos del formulario
        privi = request.form['privilegios-usu']
        usu = request.form['nom-usu']
        sql = """UPDATE usuarios
                    SET id_rol = %s 
                    WHERE id_usuario = %s;"""
        datos = (privi, id)
        sentenciaBD(sql,datos)
        flash('Privilegios de '+usu+' actualizados.') #Mensaje de Confirmación
        return redirect(url_for('administra_usuarios'))

#Busqueda usuarios
@app.route('/busqueda_usuarios', methods=['POST'])
def busqueda_usuarios():
    if 'rol' in session:
        if session['rol'] == 'adm':
            datos = request.form['busqueda']
            sql = "SELECT * FROM usuarios WHERE id_usuario != 1 AND nombre_usu LIKE '%"+datos+"%';"
            usuarios = consultaSelect(sql)
            return render_template('administrador/usuarios.html', usuarios = usuarios)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('usuarios/404.html')

if __name__ == "__main__":
    app.run(debug=True)