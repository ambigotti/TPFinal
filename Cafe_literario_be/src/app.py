from flask import Flask, render_template, request, redirect, url_for, session
import os           #modulo para acceder a las carpetas más fácilmente
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))    #indica el nombre de la carpeta donde está la aplicación
template_dir = os.path.join(template_dir,'src', 'templates')    #unir las carpetas src y templates a la carpeta principal

app = Flask(__name__, template_folder = template_dir)        # inicialización de Flask

""" app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Clave secreta para la sesión

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

# Ruta para manejar la autenticación
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Aquí hace la validación de usuario y contraseña con la lógica de autenticación

    # Autenticación simple para demostración
    if username == 'usuario' and password == 'contrasena':
        session['logged_in'] = True  # Establecer la sesión como iniciada
        return redirect(url_for('admin_panel'))  # Redirigir al panel de administrador
    else:
        return "Credenciales inválidas. Inténtalo de nuevo."


# Ruta para el panel de administrador
@app.route('/admin')
def admin_panel():
    if 'logged_in' in session and session['logged_in']:
        return "¡Bienvenido al panel de administración!"
    else:
        return redirect(url_for('show_login'))  # Si no está autenticado, redirigir al inicio de sesión

if __name__ == '__main__':
    app.run(debug=True, port=4000) """



#Rutas de la aplicación
@app.route('/')     #acceso a index.html
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM menu")
    myresult = cursor.fetchall()  #se obtiene una tupla
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

# Ruta para la Consulta a la bd
@app.route('/alta', methods=['GET'])
def consulta():
    cursor = db.database.cursor()
    sql = "SELECT * FROM menu"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    # result contendrá todos los registros de la tabla 'menu'
    return render_template('consulta.html', data=result)


# Ruta para el Alta de registros en la bd
@app.route('/menu', methods=['POST'])
def add_menu():
    Nombre_menu = request.form['Nombre_menu']
    Descripcion = request.form['Descripcion']
    Precio_menu = request.form['Precio_menu']

    # si tenemos todos los datos vamos a hacer la consulta a la bd
    if Nombre_menu and Descripcion and Precio_menu:
        cursor = db.database.cursor()
        sql = "INSERT INTO menu (Nombre_menu, Descripcion, Precio_menu) VALUES (%s, %s, %s)"
        data =(Nombre_menu, Descripcion, Precio_menu)    #tupla con los datos
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home')) #Actualización de la vista

@app.route('/delete/<string:idMenu>')
def delete(idMenu):
    cursor = db.database.cursor()
    sql = "DELETE FROM menu WHERE idMenu=%s"
    data =(idMenu,)    #dato para la búsqueda
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:idMenu>', methods=['POST'])
def edit(idMenu):
    Nombre_menu = request.form['Nombre_menu']
    Descripcion = request.form['Descripcion']
    Precio_menu = request.form['Precio_menu']
    #idMenu = request.form['idMenu'] # Obtener el idMenu del formulario

    if Nombre_menu and Descripcion and Precio_menu:
        cursor = db.database.cursor()
        sql = "UPDATE menu SET Nombre_menu = %s, Descripcion = %s, Precio_menu = %s WHERE idMenu = %s"
        data =(Nombre_menu, Descripcion, Precio_menu, idMenu)    #tupla con los datos
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home')) #Actualización de la vista



if __name__ == '__main__':          #iniciar la aplicación en modo desarrollo
    app.run(debug=True, port=4000)

# resultado correcto, el path al archivo .html está correcto


