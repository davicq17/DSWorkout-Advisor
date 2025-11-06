############# importar librerias o recursos#####
import jwt, datetime
from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from .routes.graficas import graficas
from .db import get_conn

# initializations
app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})



mysql = MySQL(app)
# cargar la info de la BD del archivo toml

app.secret_key = "dsworkout"

#rutas de graficas
app.register_blueprint(graficas)

@app.route('/TableUser', methods=['GET'])
def TableUser():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE status = 1')
                rv = cur.fetchall()

        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'username': result[1], 'name': result[2], 'surname': result[3],'email': result[4],'password': result[5],'cell': result[6],'rol':result[7]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":str(e)})

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



# ruta para consultar todos los registros de estado fisico a traves de una vista creada en la base de datos
@app.route('/TableFisic', methods=['GET'])
def Table_Fisic_State():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('select usuarios.id_i ,usuarios.name, usuarios.surname, cliente.age ,cliente.gender, cliente.height, cliente.weight, cliente.fr_train, cliente.restrictions, cliente.duration_exerss, cliente.goal from (usuarios join cliente on(usuarios.id = cliente.id_usuario and usuarios.status = 1))')
                rv=cur.fetchall()
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
        content = {'id': rv[0], 'name': rv[1], 'surname': rv[2], 'age': rv[3],'gender': rv[4],'height': rv[5],'weight': rv[6],'fr_Train':rv[7],'restrictions':rv[8],'duration':rv[9],'goal':rv[10],'equipment':rv[11]}
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
#






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



# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
