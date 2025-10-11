<script>
  tablaa = document.getElementById("tablab");

if(tablaa!=null){
tablaa.addEventListener('click',function(e){
    e.stopPropagation();
    if(e.target.id === 'evaluar'){
        e.stopPropagation();
        const id = e.target.parentNode.parentNode.children[0].textContent;
        
        //pedimos los datos en la base de datos en la tabla 
        //cliente para saber la demas informacion
        axios({
            method:'GET',
            url: 'http://127.0.0.1:5000/FisicById/'+id,
        }).then(function(response){
            conten={
                id:id,
                name:response.data.name,
                surname:response.data.surname,
                age:response.data.age,
                gender:response.data.gender,
                height:response.data.height,
                weight:response.data.weight,
                Fr_train:response.data.Fr_Train,
                duration:response.data.duration,
                goal:response.data.goal,
                equipment:response.data.equipment,
                restrictions:response.data.restrictions
            }
            localStorage.setItem('datos', JSON.stringify(conten));
            window.location.href = 'evaluar.html';
        })
    }
})
}

const CargarInfo=()=>{
    let contenido=JSON.parse(localStorage.getItem('datos'))
    if(localStorage.getItem('datos')!=null){
    //console.log(contenido)
    document.getElementById('inputnombre').value= contenido.name
    document.getElementById('inputApellido').value= contenido.surname
    document.getElementById('inputage').value= contenido.age
    document.getElementById('inputgenero').value= contenido.gender
    document.getElementById('inputAltura').value= contenido.height
    document.getElementById('inputpeso').value= contenido.weight
    document.getElementById('inputfr_train').value= contenido.Fr_train
    document.getElementById('inputDuration_sesion').value= contenido.duration
    document.getElementById('inputObjetivo').value= contenido.goal
    document.getElementById('inputEquipamiento').value= contenido.equipment
    document.getElementById('inputRestricción_alimenticia').value= contenido.restrictions
    CargarEjercicios()
    }else{
    alert('No hay datos seleccionados')
    window.location.href = 'FisicUsers.html';
    }
}
const tablaPD = new DataTable('#tablaWorkout_Personal', {
    paging:false,
    scrollY:200,
    
});
const CargarEjercicios=()=>{
    axios.get('http://127.0.0.1:5000/ejercicioTabla')
    .then(function(response){
        botones1=`<buttom type="buttom" class="btn btn-success btn-sm" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
</svg></Buttom> <buttom class= "btn btn-primary btn-sm" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
</svg></buttom>`
        data= response.data;
        ArregloDataPag1=[]
        tablaPD.clear().draw();
        for(let i = 0; i< data.length; i++){
            tablaPD.row.add([data[i].id,data[i].nombre,data[i].tipo,data[i].rating,botones1]).draw();

        }
        
        
    }).catch(err=> console.log('error:', err))
}
let tablaAR = new DataTable('#tablaRutinas', {
    paging:false,
    scrollY:200,
});
const CargarRutinas=()=>{
    //Cargar las rutinas al modal de las rutinas
    boton=`<a id="asignar" class="btn btn-success" data-bs-dismiss="modal">Asignar</a>`
    axios({
        method:'GET',
        url: 'http://127.0.0.1:5000/RutinaModal'
    }).then(function(response){
        tablaAR.clear().draw();
        for(let i=0;i<response.data.length;i++){
            tablaAR.row.add([response.data[i].id_routine,response.data[i].nombre,response.data[i].ejercicios,boton]).draw()
        }

    }).catch(err => console.log('Error: ', err))
    
}
tablaARevent=document.getElementById('tablaRutinas')
if(tablaARevent!=null){
tablaARevent.addEventListener('click',function(e){
    e.stopPropagation();
    if(e.target.id === 'asignar'){
        e.stopPropagation();
        const id = e.target.parentNode.parentNode.children[0].textContent;
        const nombre = e.target.parentNode.parentNode.children[1].textContent;
        document.getElementById('RutinaA').value=nombre;
        sessionStorage.setItem('Rutina', JSON.stringify({id_routine:id, nombre:nombre}));

    }
})
}
predecirBool=false
const predecir=() => {
    axios({
        method:'POST',
        url: 'http://127.0.0.1:5000/predictWorkout',
        data: {
            equipment: document.getElementById('inputEquipamiento').value,
            bodypart: document.getElementById('inputBodypartPredic').value,
            type:document.getElementById('inputTypePredic').value,
            level:document.getElementById('inputLevelPredic').value
        }
    }).then(function(response){
        document.getElementById('predic').value=response.data.Rating.toFixed(3)
        predecirBool=true
    }).catch(err => console.log('Error: ', err))
}
const EnvioDiagnostico=()=>{
    diagnostico=document.getElementById('diagnostico').value
    if(diagnostico!=""){
        axios({
            method:'GET',
            url: 'http://127.0.0.1:5000/verify_token/'+localStorage.getItem('token')
        }).then(function(response){
            pro=response.data.id
            Cliente=JSON.parse(localStorage.getItem('datos'))
            rutina=JSON.parse(sessionStorage.getItem('Rutina'))
            date = new Date();
            year = date.getFullYear();
            month = date.getMonth() + 1;
            day = date.getDate();
            fecha=year + '-' + (month < 10? '0' + month : month) + '-' + (day < 10? '0' + day : day);
            axios({
                method:'POST',
                url: 'http://127.0.0.1:5000/addDiagnostico',
                data:{
                    id_cliente:Cliente.id,
                    id_prof:pro,
                    fecha:fecha,
                    diagnostico:diagnostico,
                    rutina:rutina.id_routine
                }
                }).then(function(response){
                    alert(response.data.informacion)
                    localStorage.removeItem('datos')
                    window.location.href = 'FisicUsers.html';
                }).catch(err => console.log('Error: ', err))
            }).catch(err => console.log('Error: ', err))
    }else{
        alert("Diagnostico en blanco, porfavor verifique.")}
}

const tablaP= document.getElementById('tablaWorkout_Personal');
// verificamos que no este vacia
if(tablaP!=null){
    // creamos el evento de click
    tablaP.addEventListener('click',function(e){
        e.stopPropagation();
        // se verifica que el elemento clicado tenga la clase correcta para evitar errores
        if(e.target.className=='btn btn-primary btn-sm'){
            e.stopPropagation();
            InformacionEjercicio(e)
        }
        if(e.target.className=='btn btn-success btn-sm'){
            e.stopPropagation();
            AsignarEjercicio(e)
        }
    })
}
let ejerciciosSeleccionados=[];
let totalDuracion= 0;
const AsignarEjercicio=(e)=>{
    const id = e.target.parentNode.parentNode.children[0].textContent;
    const nombre = e.target.parentNode.parentNode.children[1].textContent;
    // verificamos si el ejercicio ya esta en la lista de la rutina
    console.log(ejerciciosSeleccionados.includes(id))
    if(!ejerciciosSeleccionados.includes(id)){
        ejerciciosSeleccionados.push(id);
        // se actualiza la lista de ejercicios
        let listaRutina= document.getElementById('listaRutina');
        let lista= document.createElement('li');
        lista.innerText= nombre;
        listaRutina.appendChild(lista);
        // se agrega el id al sessionStorage
        sessionStorage.setItem('Ejercicios',ejerciciosSeleccionados.join(','))

        // se hace la consulta para obtener la duración del ejercicio
        axios.get('http://127.0.0.1:5000/WorkoutById/'+id) 
        .then(function(response){
        duracionEjercicio = response.data.duration;
        console.log(duracionEjercicio);
        // se suma la duracion del nuevo ejercicio
        totalDuracion += duracionEjercicio;
        // se actualiza el input del total de la duracion de la rutina
        document.getElementById('txtduration').value = totalDuracion;               
    })
    }else{
        alert('El ejercicio ya se encuentra en la lista de la rutina')
    }
}
const InformacionEjercicio=(e)=>{
    const id = e.target.parentNode.parentNode.children[0].textContent;
    axios.get('http://127.0.0.1:5000/WorkoutById/'+id) 
    .then(function(response){
        conten={
            name:response.data.nombre,
            desc:response.data.desc,
            type:response.data.type,
            equipment:response.data.equipment,
            level:response.data.level
        }
        sessionStorage.setItem('ejercicio', JSON.stringify(conten));
        // cargamos la información
        CargarInformacion(conten);
    })
}
const CargarInformacion= (contenido) =>{
    //let contenido= JSON.parse(sessionStorage.getItem('ejercicio'))
    //if(contenido!=null){
        console.log(contenido)
        document.getElementById('predicName').value= contenido.name
        document.getElementById('predicType').value= contenido.type
        document.getElementById('predicDescription').value= contenido.desc
        document.getElementById('predicEquipment').value= contenido.equipment
        document.getElementById('predicLevel').value= contenido.level
    //}
}

const Cancelar = () =>{
    // limpiamos los inputs
    totalDuracion=0;
    ejerciciosSeleccionados=[];
    document.getElementById('txtnombre').value='';
    document.getElementById('txtdescripcion').value='';
    document.getElementById('txtduration').value='';
    document.getElementById('txtnivel').value='';
    sessionStorage.removeItem('Ejercicios');
    // se vacia la lista de ejercicios seleccionados
    document.getElementById('listaRutina').innerHTML='';
    // se vacia el input del total de la duracion de la rutina
    document.getElementById('txtduration').value = 0;
}
const Registrar_rutina = () =>{
    axios({
        method:'GET',
        url: 'http://127.0.0.1:5000/verify_token/'+localStorage.getItem('token')
        }).then(function(response){
        creadorI= response.data.id;
        nombreRutinaI= document.getElementById('txtnombre').value;
        descripRutinaI=document.getElementById('txtdescripcion').value;
        duracionRutinaI=document.getElementById('txtduration').value;
        nivelRutinaI=document.getElementById('txtnivel').value;
        ejerciciosI = sessionStorage.getItem('Ejercicios')
        axios({
            method:'POST',
            url: 'http://127.0.0.1:5000/regisRutina',
            data:{
                creador:creadorI,
                nombre:nombreRutinaI,
                descripcion:descripRutinaI,
                duracion:duracionRutinaI,
                nivel:nivelRutinaI,
                ejercicios:ejerciciosI
            }
        }).then(function(response){
            alert('Rutina registrada correctamente');
            if(response.data.informacion=='Registro de runtina Exitoso'){
                console.log('Rutina registrada correctamente');
                Cancelar();
            }
        }).catch(err=> console.log('error:', err))
    }).catch(err=> console.log('error:', err))
    
}
const FiltroPredic=()=>{
    if(predecirBool==true){
        axios.get('http://127.0.0.1:5000/ejercicioFiltro/'+document.getElementById('predic').value)
        .then(function(response){
            //console.log(response.data);
            if(response.data.length>0){
                botones1=`<buttom type="buttom" class="btn btn-success btn-sm" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
        </svg></Buttom> <buttom class= "btn btn-primary btn-sm" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
        </svg></buttom>`
                data= response.data;
                ArregloDataPag1=[]
                tablaPD.clear().draw();
                for(let i = 0; i< data.length; i++){
                    tablaPD.row.add([data[i].id,data[i].nombre,data[i].tipo,data[i].rating,botones1]).draw();

                }
                
            }else{
                alert('No se encontraron ejercicios con puntaje similar a '+document.getElementById('predic').value)
            }
        }).catch(err=> console.log('error:', err))
    }else{
        alert('Aun no haz realizado una predicción')
    }
}

const volver=()=>{
    localStorage.removeItem('datos')
    window.location.href = 'FisicUsers.html';
}
</script>
<div class="container col-sm-10 col-lg-8 col-md-10  my-5" ><!--principal-->
  <div><!--div1-->
    <button class="btn">
      <a class="text-decoration-none text-dark" ><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-arrow-bar-left" viewBox="0 0 16 16">
                <!--onclick="volver()"-->
      <path fill-rule="evenodd" d="M12.5 15a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5M10 8a.5.5 0 0 1-.5.5H3.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L3.707 7.5H9.5a.5.5 0 0 1 .5.5"/>
        </svg></a>
    </button>
  </div><!--div1-->
  <div class="justify-content-center"><!--div2-->
    <h3 class="h3 fw-bold text-center">Estado Fisico</h3>
  </div><!--div2-->
  <form class="row g-3">
    <div class="col-sm-12 col-md-6">
      <label for="inputnombre">Nombre</label>
      <input type="text" class="form-control" placeholder="Nombre" aria-label="First name" id="inputnombre" readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label for="inputApellido">Apellido</label>
      <input type="text" class="form-control" placeholder="Apellido" aria-label="Last name" id="inputApellido"readonly>
    </div>
    <div class="col-sm-12 col-md-6 ">
      <label for="inputage">Edad</label>
      <input type="text" class="form-control" id="inputage" placeholder="Edad"readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label for="inputgenero">Genero</label>
      <input type="text" class="form-control" id="inputgenero"readonly>
    </div>
    <div class="col-md-6">
      <label for="inputpeso">Peso(kg)</label>
      <input type="text" class="form-control" id="inputpeso"readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label for="inputAltura">Altura(m)</label>
      <input type="text" class="form-control" id="inputAltura" placeholder="Altura(m)"readonly>
    </div>
      <div class="col-sm-12 col-md-6">
        <label for="inputfr_train" class="form-label">Frecuencia con la que realiza actividad fisica</label>
        <input type="text" id="inputfr_train" class="form-control"readonly>
      </div>
      <div class="col-sm-12 col-md-6">
        <label for="inputDuration_sesion" class="form-label">Duracion de la sesión de ejerccio tipica</label>
        <input type="text" class="form-control" id="inputDuration_sesion"readonly>
      </div>
      <div class="col-sm-12 col-md-6">
        <label for="inputObjetivo" class="form-label">Objetivo</label>
        <input type="text" class="form-control" id="inputObjetivo"readonly>
      </div>
      <div class="col-sm-12 col-md-6">
        <label for="inputEquipamiento" class="form-label">Equipamiento</label>
        <textarea name="" id="inputEquipamiento" class="form-control" readonly></textarea>
      </div>
      <div class="col-md-12">
        <label for="inputRestricción_alimenticia" class="form-label">Restricciones alimenticias</label>
        <input type="text" class="form-control" id="inputRestricción_alimenticia"readonly>
      </div>
  </form>
        <!--Diagnostico del cliente-->
  <div><!--div3-->
    <div class="justify-content-center"><!--div3.1-->
      <h4 class="h4 fw-bold text-center">Diagnostico</h4>
    </div><!--div3.1-->
    <div class="form-floating mb-3 col-lg-12"><!--div3.2-->
      <textarea class="form-control" placeholder="Leave a comment here" id="diagnostico" style="height: 100px" resize="false"></textarea>
      <label for="diagnostico">Escriba aqui su diagnostico</label>
    </div><!--div3.2-->
    <div><!--div3.3-->
       <div class="row"><!--div3.4-->
          <div class="col-sm-12 col-md-6 mb-2">
            <label for="inputTypePredic">Tipo de ejercicios</label>
            <select id="inputTypePredic" class="form-select">
              <option value="Strength" selected>Fuerza</option>
              <option value="Stretching">Estiramiento</option>
              <option value="Plyometrics">Pilometría</option>
              <option value="Powerlifting">Levantamiento de pesas</option>
              <option value="Cardio">Cardio</option>
            </select>
          </div>

          <div class="col-sm-12 col-md-6 mb-2">
              <label for="inputBodypartPredic">Parte del cuerpo</label>
              <select id="inputBodypartPredic" class="form-select">
                <option value="Abdominals" selected>Abdomen</option>
                <option value="Adductors">Adductores</option>
                <option value="Forearms">Antebrazos</option>
                <option value="Biceps">Bíceps</option>
                <option value="Neck">Cuello</option>
                <option value="Quadriceps">Cuádriceps</option>
                <option value="Lats">Dorsales</option>
                <option value="Lower Back">Espalda baja</option>
                <option value="Middle Back">Espalda media</option>
                <option value="Glutes">Glúteos</option>
                <option value="Shoulders">Hombros</option>
                <option value="Hamstrings">Isquiotibiales</option>
                <option value="Chest">Pecho</option>
                <option value="Calves">Pantorrillas</option>
                <option value="Traps">Trapecios</option>
                <option value="Triceps">Tríceps</option>
              </select>        
          </div>
       </div><!--div3.4-->
        <div class="row"><!--div3.5-->
          <div class="col-sm-12 col-md-6 mb-2">
            <label for="inputLevelPredic">Nivel del ejercicio</label>
            <select id="inputLevelPredic" class="form-select">
              <option value="Beginner" selected>Principiante</option>
              <option value="Intermediate">Intermedio</option>
              <option value="Expert">Experto</option>
            </select>
          </div>
          <div class="col-sm-12 col-md-6">
            <label for="inputEquipamiento"> Equipamiento</label>
            <select id="inputEquipamiento" class="form-select">
              <option value="Body Only" selected>Ninguno</option>
              <option value="Bands">Bandas</option>
              <option value="Barbell">Pesas con barrra</option>
              <option value="Cable">Cuerda para saltar</option>
              <option value="Dumbbell">Pesas</option>
              <option value="E-Z Curl Bar">Barra E-Z Curl</option>
              <option value="Exercise Ball">Balón de ejercicios</option>
              <option value="Foam Roll">Rodillo de espuma</option>
              <option value="Kettlebells">Pesas rusas</option>
              <option value="Machine">Máquina</option>
              <option value="Medicine Ball">Balónn medicinal</option>
              <option value="Other">Otro</option>
            </select>
          </div>        
        </div><!--div3.5-->
        <div class="row"><!--div3.6-->
          <div class="col-md-6 mt-4">
            <input type="text" readonly id="predic" class="form-control">
            <div class="col-md-6 my-1">
              <button type="button" class="btn btn-success my-2" >Predecir</button>
              <!--onclick="predecir()"-->
            </div>
          </div>
          <div class="col-lg-6 col-md-6">
            <label for="RutinaA">Rutina Asignada</label>
            <input type="text" id="RutinaA" class="form-control" readonly placeholder="Rutina sin asignar">
          </div>
        </div><!--div3.6--> 
          <div class="col-lg-12 mt-2"><!--div3.7-->
            <button class="btn btn-primary me-2 mb-2">
              <a data-bs-toggle="modal" data-bs-target="#Asignar" class="text-decoration-none text-white">asignar Rutina</a>
              <!-- onclick="CargarRutinas()"-->
            </button>
            <button  class="btn btn-success me-2 mb-2">
              <a href="#"  class="text-decoration-none text-white">Enviar diagnostico</a>
              <!--onclick="EnvioDiagnostico()"-->
            </button>
            <button class="btn btn-info me-2">
              <a data-bs-toggle="modal" data-bs-target="#rutinaPersonalizada" class="text-decoration-none text-white">Crear Rutina Personalizada</a>
            </button>
          </div><!--div3.7-->
    </div><!--div3.3-->
  </div><!--div3-->
        <!-- Modal Asignar Rutina -->
  <div class="modal fade modal-lg" tabindex="-1" id="Asignar"><!--div4-->
    <div class="modal-dialog  col-lg-10"><!--div4.1--> 
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="text-center my-1 ms-4">Asignar Rutina</h1>
        </div>
        <div class="modal-body">
          <p class="my-2">Seleccione Rutina a asignar:</p>
          <table id="tablaRutinas">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Ejercicios</th>
                <th>Accion</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
          <div class="modal-footer d-flex justify-content-center">
            <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
          </div>
        </div>
      </div>   
    </div><!--div4.1-->
  </div><!--div4-->
      <!--Modal para formar rutina y ver prediccion-->
  <div class="modal fade modal-xl" tabindex="-1" id="rutinaPersonalizada"><!--div5-->
    <div class="modal-dialog  col-lg-10"><!--div5.1-->
      <div class="modal-content"><!--div5.1.1-->
        <div class="modal-header d-flex justify-content-between"><!--div5.1.2-->
          <div>
            <h1 class="text-center my-1 ms-4">Nueva rutina</h1>
          </div>
          <div>
            <a  class="btn btn-success my-2">Recomendacion</a>
                <!--onclick="FiltroPredic()"-->
            <a  class="btn btn-secondary">Quitar Recomendacion</a>
              <!--onclick="CargarEjercicios()"-->
          </div>
        </div><!--div5.1.2-->
              <div class="modal-body"><!--div5.1.3-->
                <div class="row">
                   <div class="col-lg-6 col-md-6 ">
                       <div class="mb-2">
                         <label for="txtnombre" class="form-label"><b>Nombre</b></label>
                         <input type="text" class="form-control" id="txtnombre" required>
                      </div>
                      <div class="mb-2">
                        <label for="txtdescripcion" class="form-label"><b>Descripción</b></label>
                        <textarea name="" id="txtdescripcion" class="form-control"></textarea required>                               
                      </div>
                      <div class="mb-2">
                        <label for="txtduration" class="form-label"><b>Duracción (min)</b></label>
                        <input type="number" class="form-control" id="txtduration" required placeholder="00 min">
                      </div>
                      <div class="mb-2">
                        <label for="txtnivel" class="form-label"><b>Nivel</b></label>
                        <select id="txtnivel" class="form-control">
                          <option selected value="Principiante">Principiante</option>
                          <option value="Intermedio">Intermedio</option>
                          <option value="Avanzado">Avanzado</option>
                        </select>
                      </div> 
                      <div class="mb-2">
                        <h4><b>Ejercicios</b></h4>
                        <ul id="listaRutina"></ul>
                      </div>
                                                                    
                      <div class="mb-2">
                        <button type="button" class="btn btn-dark" >Cancelar</button>
                          <!--onclick="Cancelar()"-->
                        <button type="button" data-bs-dismiss="modal" class="btn btn-success" >Agregar</button>
                            <!--onclick="Registrar_rutina()"-->
                      </div>             
                  </div>
                            <!--ejercicios--> 
                  <div class="col-lg-6 col-md-6 "><!--ejdiv1-->
                    <div class="mb-2">
                      <div class="mb-2">
                         <h4 class="text-center"><b>Ejercicios</b></h4>
                         <div class="table-responsive">
                          <table id="tablaWorkout_Personal" class=" table text-center table-bordered table-striped table-hover" style="width:100%">
                            <thead>
                              <tr>
                                <th scope="col"><b>Id</b></th>
                                <th scope="col"><b>Nombre</b></th>
                                <th scope="col"><b>Tipo</b></th>
                                <th scope="col"><b>Puntaje</b></th>
                                <th scope="col"><b>Acccion</b></th>
                              </tr>
                            </thead>
                            <tbody>
                            </tbody>
                          </table>
                         </div>
                      </div>
                              <!--PREDICCION DE E-TRAINER-->    
                      <div class="justify-content-center">
                        <h4 class="h4 text-center">Información</h4>
                      </div>         
                      <form>
                        <div class="mb-2 row">
                          <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="predicName" class="form-label"><b>Ejercicio</b></label>
                            <input type="text" class="form-control" id="predicName" readonly>
                          </div>
                          <div class="col-lg-6 col-md-6 col-sm-12">
                              <label for="predicType" class="form-label"><b>Tipo</b></label>
                              <input type="text" class="form-control" id="predicType" readonly>
                          </div>
                        </div>
                        <div class="mb-2 row">
                          <div class="col-lg-12 col-md-12 col-sm-12">
                            <label for="predicDescription"><b>Descripción</b></label>
                            <textarea name="" id="predicDescription" class="form-control"></textarea readonly> 
                          </div>
                        </div>
                        <div class="mb-2 row">
                          <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="predicEquipment" class="form-label"><b>Equipamiento</b></label>
                            <input type="text" class="form-control" id="predicEquipment" readonly>
                          </div>
                          <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="predicLevel" class="form-label"><b>Nivel</b></label>
                            <input type="text" class="form-control" id="predicLevel" readonly>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div><!--ejdiv1-->
                </div>
              </div><!--div5.1.3-->
              <div class="modal-footer d-flex justify-content-center">
                <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
              </div>
      </div><!--div5.1.1-->
    </div><!--div5.1-->
  </div><!--div5-->
</div><!--principal-->