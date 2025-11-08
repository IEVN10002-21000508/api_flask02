from flask import Flask, jsonify
from flask_mysqldb import MYSQL
from flask_cors import CORS
from config import config

app = Flask (__name__)

CORS(app)

conexion = MYSQL(app)