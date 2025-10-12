############# importar librerias o recursos#####
from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from fpdf import FPDF
import os 
import io
from dotenv import load_dotenv
import jwt, datetime

##importaciones necesarias para uso de Machine learning
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# initializations
app = Flask(__name__)
CORS(app)

# cargar el archivo.env para obtener las variables de entorno
load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQl_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQl_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQl_PASSWORD')
app.config['MYSQL_DB'] =os.getenv('MYSQl_DB')
app.config['MYSQL_PORT'] = 23566

mysql = MySQL(app)
"""
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_fn'
mysql = MySQL(app)"""
# settings A partir de ese momento Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "dsworkout"


# ruta para consultar todos los registros de estado fisico a traves de una vista creada en la base de datos
@app.route('/TableFisic', methods=['GET'])
def Table_Fisic_State():
    try:
        cur = mysql.connection.cursor()
        cur.execute('select usuarios.id ,usuarios.name, usuarios.surname, cliente.age ,cliente.gender, cliente.height, cliente.weight, cliente.fr_train, cliente.restrictions, cliente.duration_exerss, cliente.goal from (usuarios join cliente on(usuarios.id = cliente.id_usuario and usuarios.status = 1))')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'name': result[1], 'surname': result[2], 'age': result[3],'gender': result[4],'height': result[5],'weight': result[6],'Fr_Train':result[7]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

# ruta para saber informacion de un usuario con el id a traves de una vista creada en la base de datos
@app.route('/FisicById/<id>',methods=['GET'])
def FisicById(id):
    try:
        cur=mysql.connection.cursor()
        cur.execute('select usuarios.id ,usuarios.name, usuarios.surname, cliente.age ,cliente.gender, cliente.height, cliente.weight, cliente.fr_train, cliente.restrictions, cliente.duration_exerss, cliente.goal, cliente.equipment from (usuarios join cliente on(usuarios.id = cliente.id_usuario and usuarios.status = 1 AND id = %s))', (id,))
        rv = cur.fetchone()
        cur.close()
        content = {'id': rv[0], 'name': rv[1], 'surname': rv[2], 'age': rv[3],'gender': rv[4],'height': rv[5],'weight': rv[6],'Fr_Train':rv[7],'restrictions':rv[8],'duration':rv[9],'goal':rv[10],'equipment':rv[11]}
        return jsonify(content)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
#ruta para registrar el ejercicio
@app.route('/registroEjercicio',methods=['POST'])
def registroEjercicio():
    try:
        if request.method== 'POST':
            data = request.get_json()
            #print(f"datos recibidos:{data}")
            nombre=data['nombre']
            guide=data['guia']
            tipo=data['tipo']
            equipo=data['equipo']
            nivel=data['nivel']
            repetitions=data['repeticiones']
            series=data['series']
            duration=data['duracion']
            cur= mysql.connection.cursor()
            cur.execute("INSERT INTO workout( nombre, guide, tipo, equipo, nivel, repetitions, series, duration) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(nombre,guide,tipo,equipo,nivel,repetitions,series,duration))
            #print("inserción de ejercicion realizada")
            mysql.connection.commit()
            cur.close()
            return jsonify({"información":"Registro exitoso"})
    except Exception as e:
        print(f"Error:{e}")
        return jsonify({"informacion":str(e)})
#ruta para  mostrar los ejercicios en la tabla
@app.route('/ejercicioTabla',methods=['GET'])
def ejercicioTabla():
    try: 
        if request.method =='GET':
            cur=mysql.connection.cursor()
            cur.execute('SELECT * FROM workout')
            #print("consulta realizada")
            rv = cur.fetchall()
            cur.close()
            content = {}
            payload = []
            #print("antes del for")
            for result in rv:
                #print("dentro del for")
                if result[9]==None :
                    re=0
                else:
                    re=result[9]
                content={'id':result[0],
                         'nombre':result[1], 
                         'guia':result[2], 
                         'tipo':result[3],
                         'equipo':result[4],
                         'nivel':result[5],
                         'repeticiones':result[6],
                         'series':result[7],
                         'duracion':result[8],
                         'rating':re}
                payload.append(content)
            #print("despues del for")
            return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
# ruta para Pedir mas informacion del ejercicio
@app.route('/WorkoutById/<id>',methods=['GET'])
def WorkoutById(id):
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT nombre, guide, tipo, equipo, nivel,duration FROM workout WHERE id_workout = %s",(id,))
        rv = cur.fetchone()
        cur.close()
        content = {'nombre': rv[0], 'desc': rv[1], 'type': rv[2], 'equipment': rv[3],'level': rv[4], 'duration': rv[5]}
        return jsonify(content)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
# ruta para registrar el diagnostico del profesional
@app.route('/addDiagnostico', methods=['POST'])
def addDiagnostico():
    try:
        id_cliente=request.json['id_cliente']
        id_prof=request.json['id_prof']
        fecha=request.json['fecha']
        diagnostico=request.json['diagnostico']
        id_routine=request.json['rutina']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO evaluation (id_cliente, id_prof, fech_evaluation, diagnostico,id_routine) VALUES (%s,%s,%s,%s,%s)", (id_cliente,id_prof,fecha,diagnostico,id_routine))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion":"Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

##predecir Ejercicio
@app.route('/predictWorkout',methods=['POST'])
def predictWorkout():
    data = request.get_json()
    Equipment=data['equipment']
    BodyPart=data['bodypart']
    Type=data['type']
    Level=data['level']
    file_path = 'api/megaGymDataset.csv'
    data = pd.read_csv(file_path)

    # Imputar valores faltantes
    data.fillna({'Rating':data['Rating'].mean()}, inplace=True)
    data.fillna({'RatingDesc':'No Description'}, inplace=True)

    # Seleccionar características y la variable objetivo
    features = ['Type', 'BodyPart', 'Equipment', 'Level']
    X = data[features]
    y = data['Rating']

    # Codificación de variables categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, features)
        ])

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir el modelo Gradient Boosting Regressor
    model = GradientBoostingRegressor(random_state=42)

    # Crear el pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', model)])

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # Hacer predicciones
    y_pred = clf.predict(X_test)

    # Evaluar el modelo
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'RMSE: {rmse}')

    # Ejemplo de predicción con nuevos datos
    new_data = pd.DataFrame({
        'Type': [Type],
        'BodyPart': [BodyPart],
        'Equipment': [Equipment],
        'Level': [Level]
    })

    # Predecir el rating para los nuevos datos
    new_pred = clf.predict(new_data)
    print(new_pred[0])
    return jsonify({'Rating': new_pred[0]})



#ruta para mostrar el diagnostico al cliente
@app.route('/GetDiagnostico/<id>',methods=['GET'])
def GetDiagnostico(id):
    try:
        cur=mysql.connection.cursor()
        cur.execute('SELECT e.id_cliente,e.id_prof,e.fech_evaluation,e.diagnostico,r.id_routine,r.nombre,r.nivel,r.descripcion FROM evaluation e join routine r on e.id_routine=r.id_routine WHERE e.id_cliente = %s ORDER BY e.fech_evaluation DESC LIMIT 1', (id,))
        rv = cur.fetchone()
        cur.close()
        if rv:
            content={'id_cliente':rv[0],
                     'id_prof':rv[1],
                     'fech_evaluation':rv[2],
                     'diagnostico':rv[3],
                     'idR':rv[4],
                     'nombreR':rv[5],
                     'nivelR':rv[6],
                     'descripcion':rv[7]}
            return jsonify(content)
        else:
            return jsonify({'informacion':"SinDiagnostico"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

#Ruta para Mostrar los ejercicios que estan asignados al usuario
@app.route('/EjerciciosUser/<idRutina>',methods=['GET'])
def EjerciciosUser(idRutina):
    try:
        cur=mysql.connection.cursor()
        cur.execute("Select w.id_workout, w.nombre, w.duration, w.repetitions, w.series from workout w join routine_workout rw on rw.id_workout=w.id_workout where rw.id_routine=%s ",(idRutina,))
        rv=cur.fetchall()
        content={}
        payload=[]
        for result in rv:
            content={"id":result[0],
                     "nombre":result[1],
                     "duracion":result[2],
                     "repeticiones":result[3],
                     "series":result[4]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
    
####RUTA PARA CARGAR LA INFORMACION DE CONFIGURACION DE LOS USUARIOS##
@app.route('/TableUser', methods=['GET'])
def TableUser():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE status = 1')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'username': result[1], 'name': result[2], 'surname': result[3],'email': result[4],'password': result[5],'cell': result[6],'rol':result[7]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


# ruta para verificar token
@app.route('/verify_token/<token>', methods=['GET'])
def verify_token(token):
    try:
        payload = jwt.decode(token, app.secret_key,algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'message': 'The token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 403
# ruta para consultar por parametro
@app.route('/Login/<username>',methods=['GET'])
def Login(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id,username,name,surname,password,rol,status FROM usuarios WHERE username = %s', (username,))
        rv = cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            jpayload={'id':result[0],
                    'username':result[1],
                    'name':result[2],
                    'surname':result[3],
                    'rol':result[5],
                    'exp': datetime.datetime.now() + datetime.timedelta(hours=6),
                    'iat': datetime.datetime.now()
                 }
            token=jwt.encode(jpayload, app.secret_key, algorithm='HS256')
            #print(token)
            content= {"id":result[0],"username":result[1],"name":result[2],"surname":result[3],"password":result[4],"rol":result[5],"status":result[6],'token':token}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


#### ruta para verificar la existencia de un usuario ###
@app.route('/VerifyUser/<username>',methods=['GET'])
def VerifyUser(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT username FROM usuarios WHERE username = %s', (username,))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content= {"username":result[0]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
####EDITAR UN USUARIO DESDE ADMIN####
@app.route('/editUser/<id>', methods=['PUT'])
def editUser(id):
    try:
        if request.method == 'PUT':
            username= request.json['username']
            name = request.json['name']
            surname = request.json['surname']
            email= request.json['email']  
            password = request.json['password']
            cell= request.json['cell']
            rol=request.json['rol']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE usuarios SET username=%s,name=%s,surname=%s,email=%s,password=%s,cell=%s,rol=%s WHERE id=%s", (username,name,surname,email,password,cell,rol,id))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion":"Actualizacion realizada con exito"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


#### ruta para crear un registro########
@app.route('/registro', methods=['POST'])
def registro():
    try:
        if request.method == 'POST':
            data = request.get_json()
            #print(f"datos recibidos: {data}")
            username= data['username']
            name = data['name']
            surname = data['surname']
            email= data['email']  
            password = data['password']
            cell= data['cell']
            rol=data['rol']
            speciality = data.get('especialidad',None)
            #print(f"especialidad resivida:{speciality}")
            cur = mysql.connection.cursor()
            # iniciamos la transacción
            cur.execute("START TRANSACTION")
            print("transacción iniciada")
            #inserción tabla usuarios
            cur.execute("INSERT INTO usuarios (username,name,surname,email,password,cell,rol,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (username,name,surname,email,password,cell,rol,1))
            print("inserción de usuario realizada")
            #obtengo el ultimo ID insertdo
            cur.execute("SELECT LAST_INSERT_ID()")
            id_usuario =cur.fetchone()[0]
            #print(f"id usuario: {id_usuario}")
            #verifica que el usuario es profesional
            if rol == '3' and speciality:
                # inserción en la tabla del profesional con el id obtenido 
                cur.execute("INSERT INTO profesional (id_usuario, `specialty`) VALUES (%s,%s)",(id_usuario,speciality))
                print("inserccón de profesional realizada")
            mysql.connection.commit()
            print("Transacción confirmada")
            cur.close()
            return jsonify({"informacion":"Registro exitoso"})
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error:{e}")
        return jsonify({"informacion":str(e)})

@app.route("/regisFisicState",methods=['POST'])
def regisFisicState():
    try:
        if request.method=='POST':
            id=request.json['id']
            age=request.json['age']
            gender=request.json['gender']
            height=request.json['height']
            weight=request.json['weight']
            Fr_train=request.json['Fr_train']
            duration=request.json['duration']
            goal=request.json['goal']
            equipment=request.json['equipment']
            restrictions=request.json['restrictions']
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO cliente (id_usuario,age,gender,height,weight,fr_train,duration_exerss,goal,equipment,restrictions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,age,gender,height,weight,Fr_train,duration,goal,equipment,restrictions))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion":"Registro de estado fisico Exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

######### ruta para actualizar################
@app.route('/update/<id>', methods=['PUT'])
def update_contact(id):
    try:
        fullname = request.json['fullname']
        phone = request.json['phone']
        email = request.json['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})



@app.route('/delete/<id>', methods = ['PUT'])
def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET status = %s WHERE id = %s', (0, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
##peticion de datos generales para Estadisticas####
@app.route('/GetGeneral',methods=['GET'])
def GetGeneral():
    try:
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
        return jsonify({"informacion":e})

###Peticion de datos para la grafica 1####
@app.route('/GetGrafica1',methods=['GET'])
def GetGrafica1():
    try:
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
        return jsonify({"informacion":e})


####Peticion de datos para la grafica 2####

@app.route('/GetGrafica2', methods=['GET'])
def GetGrafica2():
    try:
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
        return jsonify({"informacion":e})


####Peticion de datos para la grafica 3####

@app.route('/GetGrafica3',methods=['GET'])
def GetGrafica3():
    try:
        cur=mysql.connection.cursor()
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
        return jsonify({"informacion":e})


@app.route('/GetGrafica4',methods=['GET'])
def GetGrafica4():
    try:
        cur=mysql.connection.cursor()
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
        return jsonify({"informacion":e})
####Peticion de datos para la grafica 5####
@app.route('/getGrafica5',methods=['GET'])
def getGrafica5():
    try:
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


###Peticion de datos para la grafica 6###
@app.route('/getGrafica6',methods=['GET'])
def getGrafica6():
    try:
        cur = mysql.connection.cursor()
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


###RUTA PARA REGISTRAR UNA RUTINA##
@app.route('/regisRutina',methods=['POST'])
def regisRutina():
    try:
        id_prof=request.json['creador']
        nombre=request.json['nombre']
        descripcion=request.json['descripcion']
        duracion=request.json['duracion']
        nivel=request.json['nivel']
        ejercicios=request.json['ejercicios']
        #print(ejercicios)
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO routine (id_prof,nombre,descripcion,duration,nivel) VALUES (%s,%s,%s,%s,%s)',(id_prof,nombre,descripcion,duracion,nivel))
        
        cur.execute("SELECT LAST_INSERT_ID()")
        id_routine=cur.fetchone()[0]

        peticion='INSERT INTO routine_workout (id_routine,id_workout, orden) VALUES '
        exer=ejercicios.split(',')
        
        for i in range(len(exer)):
            n=i+1	
            peticion=peticion+' ('+str(id_routine)+','+str(exer[i])+','+str(n)+')'
            if i!=len(exer)-1:
                peticion=peticion+','
        cur.execute(peticion)
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion":"Registro de rutina Exitoso"})
    except Exception as e:
        return jsonify({"error":e})
    
@app.route('/getRoutines', methods=['GET'])
def getRoutines(): 
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT CONCAT(usuarios.name,' ',usuarios.surname) as profesional,routine.id_routine,routine.nombre,descripcion,duration,nivel FROM routine JOIN usuarios ON routine.id_prof=usuarios.id ")
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content={'Autor':result[0],'id_routine':result[1],'nombre':result[2],'descripcion':result[3],'duracion':result[4],'nivel':result[5]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error":str(e)})

##Lista de rutinas para modal###
@app.route('/RutinaModal', methods=['GET'])
def RutinaModal():
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT rw.id_routine,ro.nombre,(SElECT GROUP_CONCAT(w.nombre ORDER BY rw.orden SEPARATOR ', ') from workout w join routine_workout rw on w.id_workout=rw.id_workout where rw.id_routine=ro.id_routine) FROM routine ro JOIN routine_workout rw ON rw.id_routine=ro.id_routine group BY ro.id_routine")
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content={'id_routine':result[0],'nombre':result[1],'ejercicios':result[2]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error":str(e)})
    
####Filtro de ejercicios con rating####
@app.route('/ejercicioFiltro/<Rating>', methods=['GET'])
def ejercicioFiltro(Rating):
    try:
        rating=float(Rating)
        min=rating-1
        max=rating+1
        print(min,max)
        cur=mysql.connection.cursor()
        cur.execute("SELECT w.id_workout,w.nombre,w.tipo,w.rating FROM workout w where w.rating BETWEEN %s and %s",(min,max,))
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content={'id':result[0],
                     'nombre':result[1],
                     'tipo':result[2],
                     'rating':result[3]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error":str(e)})

## ruta para generar y descargar el informe
@app.route('/generarPDF')
def generarPDF():
    try:
        cur=mysql.connection.cursor()
        ## consulta de todas las evaluaciones
        cur.execute('''SELECT evaluation.id_evaluation,
                    cliente.name AS cliente, 
                    profesional.name AS profesional,
                    routine.nombre, 
                    evaluation.fech_evaluation 
                    FROM evaluation 
                    JOIN usuarios AS cliente on evaluation.id_cliente = cliente.id 
                    JOIN routine on  evaluation.id_routine = routine.id_routine 
                    JOIN usuarios AS profesional on evaluation.id_prof= profesional.id
                    WHERE evaluation.fech_evaluation >= now() - INTERVAL 7 DAY''')
        rv = cur.fetchall()
        payload=[]
        content={}
        for result in rv:
            content={'id_evaluation':result[0],'cliente':result[1],'profesional':result[2],'nombre_rutina':result[3],'fecha_evaluacion':result[4]}
            payload.append(content)
        ## segunda consulta, numero de usuarios activos
        cur.execute("SELECT count(usuarios.id) FROM usuarios WHERE usuarios.status = 1")
        US= cur.fetchone()
        ## tercera consulta de las evaluaciones hechas en la ultima semana
        cur.execute("SELECT count(evaluation.id_evaluation)  FROM evaluation WHERE evaluation.fech_evaluation >= now() - INTERVAL 7 DAY")
        ev= cur.fetchone()
        ## cuarta consulta, cantidad  de tipos de ejercicios 
        cur.execute("SELECT workout.tipo, count(workout.id_workout) FROM workout  GROUP BY workout.tipo;")
        wk= cur.fetchall()
        payload2=[]
        content2={}
        for result in wk:
            content2={'tipo':result[0], 'workouts':result[1]}
            payload2.append(content2) 
        cur.close()
        ## creacion del pdf
        pdf = FPDF()
        pdf.add_page()
        ## sección de la evaluacion
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(page_width, 10, txt='Reporte de Evaluaciones',ln=True, align='C')
        pdf.set_font('Arial', 'B', 12)
        ## evaluaciones de la semana
        pdf.cell(0,10, txt='Usuarios activos: '+str(US[0]), ln=True)
        pdf.cell(0, 10, txt='Evaluaciones realizadas en la última semana: '+str(ev[0]), ln=False)
        col_width= page_width/6
        col_width2= page_width/3
        pdf.ln(10)
        th=pdf.font_size
        ## encabezados de la tabla de las evaluaciones
        pdf.cell(col_width, th, txt='# Evaluación', border=1)
        pdf.cell(col_width, th, txt='Cliente', border=1)
        pdf.cell(col_width, th, txt='Profesional', border=1)
        pdf.cell(col_width2, th, txt='Rutina', border=1)
        pdf.cell(col_width, th, txt='Fecha', border=1)
        pdf.ln(th)
        pdf.set_font('Arial', '', 12)
        for row in payload:
            ##print("fila escrita")
            pdf.cell(col_width,th, str(row['id_evaluation']), border=1)
            pdf.cell(col_width,th, row['cliente'], border=1)
            pdf.cell(col_width,th, row['profesional'], border=1)
            pdf.cell(col_width2,th, row['nombre_rutina'], border=1)
            pdf.cell(col_width,th, str(row['fecha_evaluacion']), border=1)
            pdf.ln(th)
        pdf.ln(10)
        ## sección de ejercicio
        pdf.set_font('Arial','B', 16)
        pdf.cell(page_width,10,txt='Reporte de Ejercicios',ln=True, align='C')
        pdf.set_font('Arial','B',12)
        ## encabezado de la tabla ejercicios 
        col_width = page_width/2
        pdf.ln(5)  
        th = pdf.font_size
        headers = ['Tipo','Cantidad']
        for header in headers:
            pdf.cell(col_width,th,txt=header,border=1, align='C')
        pdf.ln(th)
        pdf.set_font('Arial','',12)
        for row in payload2:
            pdf.cell(col_width,th, row['tipo'], border=1,align='C')
            pdf.cell(col_width,th, str(row['workouts']), border=1,align='C')
            pdf.ln(th)
        pdf.ln(10)
        pdf.set_font('Arial','',10)
        pdf.cell(page_width,0.0, txt='Fin de reporte', align='C')

        pdf_output = io.BytesIO()
        pdf.output(dest='S')  # Guardar el PDF en una cadena de bytes
        pdf_output.write(pdf.output(dest='S').encode('latin1'))  # Escribir el contenido PDF en BytesIO
        pdf_output.seek(0)

        #print("PDF listo para mandar")
        return send_file(pdf_output, as_attachment=True, download_name='Informe.pdf', mimetype='application/pdf')
    except Exception as e:
        return f"Se produjo un error: {str(e)}"
# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)

