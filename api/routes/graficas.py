from flask import Blueprint, jsonify
from flask_mysqldb import MySQL
from ..db import mysql #pool#

graficas = Blueprint('graficas',__name__)


#peticion de datos generales para Estadisticas####
@graficas.route('/GetGeneral',methods=['GET'])
def get_general():
    """se obtienen lo datos generales a mostrar"""
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute('''SELECT count(usuarios.id) as total, 
                    (SELECT count(*) as evaluation FROM evaluation) as diagnosticos, 
                    (SELECT count(*) FROM routine) as rutinas, 
                    (SELECT count(*) FROM workout) as ejercicios  
                    FROM usuarios where usuarios.status = 1''')
        rv = cur.fetchone()
        cur.close()
        content={'totalUsuarios': rv[0],'diagnosticosTotales': rv[1], 'rutinas': rv[2], 'ejercicios':rv[3]}
        
        return jsonify(content)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})


@graficas.route('/GetGrafica1',methods=['GET'])
def get_grafica1():
    """petición de datos para la grafica 1"""
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute('''SELECT cliente.weight,cliente.height
            FROM cliente join usuarios ON (cliente.id_usuario=usuarios.id) where usuarios.status=1''')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'weight': result[0], 'height': result[1]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})




@graficas.route('/GetGrafica2', methods=['GET'])
def get_grafica2():
    """petición de datos para la grafica """
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute("SELECT cliente.gender, count(0) AS total,(SELECT count(*) as total from evaluation) FROM (cliente join usuarios on(cliente.id_usuario = usuarios.id)) WHERE usuarios.status = 1 GROUP BY cliente.gender")
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'gender': result[0], 'total': result[1], 'diagnosticosTotales': result[2]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})




@graficas.route('/GetGrafica3',methods=['GET'])
def get_grafica3():
    """petición de datos para la grafica 3"""
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute("Select cliente.goal ,count(*) AS total FROM( cliente JOIN usuarios ON (cliente.id_usuario=usuarios.id)) WHERE usuarios.status=1 group by cliente.goal")
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content = {'goal': result[0], 'total': result[1]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})


@graficas.route('/GetGrafica4',methods=['GET'])
def get_grafica4():
    """petición de datos para la grafica 4"""
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute("SELECT rol,count(*) AS total FROM usuarios WHERE status=1 group by rol")
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content = {'rol': result[0], 'total': result[1]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})


@graficas.route('/getGrafica5',methods=['GET'])
def get_grafica5():
    """petición de datos para la grafica 5"""
    try:
        """conn= pool.getconn()
        cur = conn.cursor()"""
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
                CASE 
                    WHEN age BETWEEN 0 AND 17 THEN '0-17'
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 45 THEN '36-45'
                    WHEN age BETWEEN 46 AND 55 THEN '46-55'
                    WHEN age BETWEEN 56 AND 65 THEN '56-65'
                    WHEN age > 65 THEN '66+'
                    ELSE 'Unknown'
                END AS rango_edad,
                COUNT(*) AS numero_de_personas
            FROM cliente join usuarios on cliente.id_usuario=usuarios.id where status=1
                GROUP BY rango_edad
                    ''')
        rv = cur.fetchall()
        cur.close()
        
        return jsonify(rv)
    except Exception as e:
        return jsonify({"error":str(e)})



@graficas.route('/getGrafica6',methods=['GET'])
def get_grafica6():
    """petición de datos para la grafica 6"""
    """conn= pool.getconn()
        cur = conn.cursor()"""
    try:
        cur=mysql.connection.cursor()
        cur.execute('''SELECT 
                CASE 
                    WHEN height BETWEEN 1.55 AND 1.65 THEN '1.55-1.65'
                    WHEN height BETWEEN 1.65 AND 1.75 THEN '1.65-1.75'
                    WHEN height BETWEEN 1.72 AND 1.85 THEN '1.75-1.85'
                    WHEN height BETWEEN 1.85 AND 1.95 THEN '1.85-1.95'
                    ELSE 'Unknown'
                END AS rango_altura,
                COUNT(*) AS numero_de_personas
            FROM cliente join usuarios on cliente.id_usuario=usuarios.id where status=1
            GROUP BY rango_altura''')
        rv = cur.fetchall()
        cur.close()
        
        return jsonify(rv)
    except Exception as e:
        return jsonify({"error":str(e)})