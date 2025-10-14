##importacion de Pool de BD
from api.db import pool

#ruta para consultar por parametro
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
