from wtforms import Form
# Deberás cambiar la importación a FlaskForm, ya que la lógica en app_01.py 
# lo requiere para manejar el CSRF y la validación en Flask POST.
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField, RadioField, SelectMultipleField, DateField
from wtforms import validators

tamano = [
    ('chica', 40),
    ('mediana', 80),
    ('grande', 120)
]

class UserForm(Form):
    matricula=IntegerField("Matricula", [ 
        validators.DataRequired(message='El campo es requerido')
    ])
    nombre=StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido')
    ])
    apellido=StringField("Apellido" ,[
        validators.DataRequired(message='El campo es requerido')
    ])
    correo = EmailField("Correo",[
        validators.Email(message='Ingrese Correo Valido')
    ])


class UserForm(Form):
    matricula=IntegerField("Matricula", [ 
        validators.DataRequired(message='El campo es requerido')
    ])
    nombre=StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido')
    ])
    apellido=StringField("Apellido" ,[
        validators.DataRequired(message='El campo es requerido')
    ])
    correo = EmailField("Correo",[
        validators.Email(message='Ingrese Correo Valido')
    ])


class PizzaForm(Form):
    nombre = StringField('Nombre completo', [
        validators.DataRequired(message='El campo es requerido')
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message='El campo es requerido')
    ])
    telefono = StringField('Teléfono', [
        validators.DataRequired(message='El campo es requerido')
    ])
    fecha = DateField('Fecha de Compra', [
        validators.DataRequired(message='El campo es requerido')
    ], format='%Y-%m-%d')
    
    tamano = RadioField('Tamaño Pizza', 
        choices=[
            ('chica', 'Chica $40'),
            ('mediana', 'Mediana $80'),
            ('grande', 'Grande $120')
        ],
        validators=[validators.DataRequired()]
    )
    numPizzas = IntegerField('Número de Pizzas', 
        [validators.DataRequired()]
    )

    jamon = BooleanField('Jamón $10')
    pina = BooleanField('Piña $10')
    champ = BooleanField('Champiñones $10')