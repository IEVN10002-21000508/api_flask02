from flask import Flask, render_template, request
import forms

app = Flask(__name__)

@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    listado = ['python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template('index.html', titulo = titulo, listado = listado)

@app.route('/distancia')
def distancia():
    if request.method =='POST':
        x1=request.form['numero1']
        x2=request.form['numero2']
        suma = int(numero1) + int(numero2)
        return render_template('distancia.html' ,res=res, numero1=numero1, numero2=numero2) 
    return render_template('distancia.html')

@app.route('/calculos', methods=['GET','POST'])
def calculos():
    if request.method =='POST':
        numero1=request.form['numero1']
        numero2=request.form['numero2']
        suma = int(numero1) + int(numero2)
        opcion = request.form['operacion']
        if opcion == 'suma':
            res = int(numero1) + int(numero2)
        if opcion == 'resta': 
           res = int(numero1) - int(numero2)
        if opcion == 'multplicación':
            res =int(numero1) * int(numero2)
        if opcion == 'división':
            res= int(numero1) / int(numero2)
        return render_template('calculos.html' ,res=res, numero1=numero1, numero2=numero2) 
    return render_template('calculo.html')

@app.route('/Alumnos', methods=["GET","POST"])
def alumnos():
    mat=0
    nom=""
    ape=""
    email=""
    alumno_clas=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():
        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data
    return render_template('Alumnos.html', form=alumno_clas, mat=mat, nom=nom, ape=ape, email=email)

@app.route('/')
def home():
    return "Hello World"

@app.route('/hola')
def about():
    return "hola"

@app.route('/user/<string:user>')
def user(user):
    return f"Hello, {user}!"

@app.route("/numero/<int:num>")
def func(num):
    return  f"El numero es: {num}"

@app.route("/suma/<int:num1>/<int:num2>")
def suma(num1,num2):
    return f"LA suma es {num1 + num2}"

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre {}".format(id,username)

@app.route("/user/<float:id>/<float:username>")
def func1(n1,n2):
    return "La suma es: {}".format(n1+n2)

@app.route("/default/")
@app.route("/default/<string:dft>")
def func2(dft="sss"):
    return "El valor de dft es:" + dft

@app.route("/prueba")
def func4():
    return '''
    <html>
    <head>
    <title> Página de prueba</title>
        </head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
        <body>
            <h1>PAgina de prueba</h1>
          <p>Esta es una pagina de prueba</p>  
        <body>
        </html>

        '''


if __name__ == '__main__':
    app.run(debug=True)

