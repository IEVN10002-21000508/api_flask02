from flask import Flask, render_template, request
import forms
from flask import make_response,jsonify,json


app = Flask(__name__)

PRECIOS_TAMANO_MAP = {'chica': 40, 'mediana': 80, 'grande': 120}
PRECIO_UNITARIO_INGREDIENTE = 10

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
    estudiantes=[]
    datos={}
    temp=[]
    alumno_clas=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():

        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')
        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data

        datos={'matricula':mat,'nombre':nom.rstrip(),
               'apellido':ape.rstrip(),'email':email.rstrip()}  
        data_str = request.cookies.get("usuario")
        if not data_str:
             return "No hay cookie guardada", 404
        estudiantes = json.loads(data_str)
        estudiantes.append(datos)  
    response=make_response(render_template('Alumnos.html',
            form=alumno_clas, mat=mat, nom=nom, ape=ape, email=email))
   
   
    if request.method!='GET':
        response.set_cookie('usuario',json.dumps(temp))
    
    return response
    
@app.route("/get_cookie")
def get_cookie():
     
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No hay cookie guardada", 404
 
    estudiantes = json.loads(data_str)
 
    return jsonify(estudiantes)



@app.route('/')
def home():
    return "Hello World"

@app.route('/pizzeria', methods=['GET','POST'])
def pizzeria(): 
    
    PRECIOS_TAMANO_MAP = {'chica': 40, 'mediana': 80, 'grande': 120}
    PRECIO_UNITARIO_INGREDIENTE = 10 
    
    pizza_clas = forms.PizzaForm(request.form)
    
    pedido_str = request.cookies.get("cookie_pedido")
    pizzas_en_pedido = json.loads(pedido_str) if pedido_str else []
    
    ventas_str = request.cookies.get("cookie_ventas")
    ventas_del_dia = json.loads(ventas_str) if ventas_str else []

    total_general_dia = sum(venta.get('total', 0) for venta in ventas_del_dia)
    mensaje_confirmacion = None
    temp_pedido = pizzas_en_pedido.copy() 


    response = make_response(render_template('pizzeria.html',
        form=pizza_clas,pizzas_en_pedido=list(enumerate(pizzas_en_pedido)), ventas_del_dia=ventas_del_dia, total_general_dia=total_general_dia,mensaje_confirmacion=mensaje_confirmacion))
    

    if request.method == 'POST':
        action = request.form.get('action') 

        if action == 'quitar':
            indices_a_quitar_str = request.form.getlist('pizza_a_quitar')
            indices_a_quitar = [int(i) for i in indices_a_quitar_str]
            pizzas_actualizadas = [pizza for index, pizza in enumerate(pizzas_en_pedido) if index not in indices_a_quitar]
            temp_pedido = pizzas_actualizadas

        elif pizza_clas.validate(): 
            if action == 'agregar':
                
                tamano_key = pizza_clas.tamano.data
                costo_pizza_unitario = PRECIOS_TAMANO_MAP.get(tamano_key, 0)
                ingredientes_list = []
                
                if pizza_clas.jamon.data:
                    costo_pizza_unitario += PRECIO_UNITARIO_INGREDIENTE
                    ingredientes_list.append("Jamón")
                if pizza_clas.pina.data:
                    costo_pizza_unitario += PRECIO_UNITARIO_INGREDIENTE
                    ingredientes_list.append("Piña")
                if pizza_clas.champ.data:
                    costo_pizza_unitario += PRECIO_UNITARIO_INGREDIENTE
                    ingredientes_list.append("Champiñones")
                
                num_pizzas = pizza_clas.numPizzas.data
                subtotal = costo_pizza_unitario * num_pizzas
                
                nueva_pizza = {
                    'tamano': tamano_key.capitalize(),
                    'ingredientes': ', '.join(ingredientes_list) if ingredientes_list else 'Ninguno',
                    'num_pizzas': num_pizzas,
                    'subtotal': subtotal
                }
                
                pizzas_en_pedido.append(nueva_pizza)
                temp_pedido = pizzas_en_pedido 
                
            elif action == 'terminar':
                if not pizzas_en_pedido:
                    mensaje_confirmacion = 'El pedido está vacío. Agregue una pizza primero.'
                else:
                    total_pedido = sum(pizza['subtotal'] for pizza in pizzas_en_pedido)
                    mensaje_confirmacion = f'El costo total del pedido para {pizza_clas.nombre.data} es de ${total_pedido}.'

                    nueva_venta = {
                        'nombre': pizza_clas.nombre.data,
                        'direccion': pizza_clas.direccion.data,
                        'telefono': pizza_clas.telefono.data,
                        'fecha': pizza_clas.fecha.data.strftime('%Y-%m-%d'), 
                        'total': total_pedido
                    }
                    
                    ventas_del_dia.append(nueva_venta)
                    temp_pedido = [] # Limpia el pedido temporal

        total_general_dia = sum(venta.get('total', 0) for venta in ventas_del_dia)
        
        response = make_response(render_template('pizzeria.html',
            form=pizza_clas, pizzas_en_pedido=list(enumerate(temp_pedido)), ventas_del_dia=ventas_del_dia, total_general_dia=total_general_dia, mensaje_confirmacion=mensaje_confirmacion))
        
        # Guardado de Cookies (Patrón alumnos)
        response.set_cookie('cookie_ventas', json.dumps(ventas_del_dia))
        response.set_cookie('cookie_pedido', json.dumps(temp_pedido))

    # Retorno Final
    return response

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

