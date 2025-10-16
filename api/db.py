import tomllib
from psycopg_pool import ConnectionPool
from flask_mysqldb import MySQL
from flask import Flask

app = Flask(__name__)
""" pool = None""" 

 
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_fn'
mysql = MySQL(app)
"""with open("pyproject.toml","rb") as f:
        config = tomllib.load(f)
        pool = ConnectionPool(
            conninfo=(config["database"]["DATABASE_URL"]),
            min_size=1,
            max_size=10
        )"""
