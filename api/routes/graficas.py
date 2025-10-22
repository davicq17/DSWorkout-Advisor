from flask import Blueprint, jsonify
from flask_mysqldb import MySQL
from api.db import get_conn

graficas = Blueprint('graficas',__name__)


#peticion de datos generales para Estadisticas####
@graficas.route('/GetGeneral',methods=['GET'])
def get_general():
    """se obtienen lo datos generales a mostrar"""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT count(usuarios.id) as total,
                    (SELECT count(*) as evaluacion FROM evaluacion) as diagnosticos,
                    (SELECT count(*) FROM routine) as rutinas,
                    (SELECT count(*) FROM workout) as ejercicios
                    FROM usuarios where usuarios.status = 1''')
                rv = cur.fetchone()
        content={'totalUsuarios': rv[0],'diagnosticosTotales': rv[1], 'rutinas': rv[2], 'ejercicios':rv[3]}

        return jsonify(content)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})


@graficas.route('/GetGrafica1',methods=['GET'])
def get_grafica1():
    """petición de datos para la grafica 1"""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT
                                    e.weight AS peso,
                                    e.height AS altura
                                FROM evaluacion e
                                INNER JOIN usuarios u ON e.id_cliente = u.id
                                WHERE u.status = 1;

                    ''')
                rv = cur.fetchall()

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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT
                                    e.gender,
                                    COUNT(*) AS total,
                                    (SELECT COUNT(*) FROM evaluacion) AS total_evaluaciones
                                FROM evaluacion e
                                INNER JOIN usuarios u ON e.id_cliente = u.id
                                WHERE u.status = 1
                                GROUP BY e.gender;

                                """)
                rv = cur.fetchall()

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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT
                            e.goal,
                            COUNT(*) AS total
                        FROM evaluacion e
                        JOIN usuarios u ON e.id_cliente = u.id
                        WHERE u.status = 1
                        GROUP BY e.goal;
                        """)
                rv=cur.fetchall()
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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT rol,count(*) AS total FROM usuarios WHERE status=1 group by rol")
                rv=cur.fetchall()
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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                    CASE
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 0 AND 17 THEN '0-17'
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 46 AND 55 THEN '46-55'
                        WHEN CAST(e.age AS UNSIGNED) BETWEEN 56 AND 65 THEN '56-65'
                        WHEN CAST(e.age AS UNSIGNED) > 65 THEN '66+'
                        ELSE 'Unknown'
                    END AS rango_edad,
                    COUNT(*) AS numero_de_personas
                FROM evaluacion e
                JOIN usuarios u ON e.id_cliente = u.id
                WHERE u.status = 1
                GROUP BY rango_edad;
                """)
                rv = cur.fetchall()


        return jsonify(rv)
    except Exception as e:
        return jsonify({"error":str(e)})



@graficas.route('/getGrafica6',methods=['GET'])
def get_grafica6():

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT
                                    CASE
                                        WHEN CAST(e.height AS DECIMAL(4,2)) BETWEEN 155 AND 165 THEN '1.55-1.65'
                                        WHEN CAST(e.height AS DECIMAL(4,2)) BETWEEN 166 AND 175 THEN '1.66-1.75'
                                        WHEN CAST(e.height AS DECIMAL(4,2)) BETWEEN 176 AND 185 THEN '1.76-1.85'
                                        WHEN CAST(e.height AS DECIMAL(4,2)) BETWEEN 186 AND 195 THEN '1.86-1.95'
                                        ELSE 'Unknown'
                                    END AS rango_altura,
                                    COUNT(*) AS numero_de_personas
                                FROM evaluacion e
                                JOIN usuarios u ON e.id_cliente = u.id
                                WHERE u.status = 1
                                GROUP BY rango_altura;
                                ''')
            rv = cur.fetchall()

        return jsonify(rv)
    except Exception as e:
        return jsonify({"error":str(e)})
