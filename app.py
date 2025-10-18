from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    listado = ['python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template('index.html', titulo = titulo, listado = listado)

@app.route('/distancia')
def distancia():
    return render_template('index.html')

@app.route('/calculos')
def calculos():
    return render_template('calculo.html')

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

