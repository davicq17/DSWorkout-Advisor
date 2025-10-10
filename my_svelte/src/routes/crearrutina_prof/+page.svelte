<script>
  //CARGA DE TABLAS PARA INTERFAZ DE PROFESIONAL
const Init_Data =() =>{
    CargarEjercicios()
    CargarRutinasBIG()

}
const CargarEjercicios=()=>{
    //TABLA DE EJERCICIOS PARA AGGREGAR A UNA RUTINA
    axios.get('http://127.0.0.1:5000/ejercicioTabla')
    .then(function(response){
        botones1=`<buttom type="buttom" class="btn btn-success btn-sm" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
</svg></Buttom> <buttom class= "btn btn-primary btn-sm" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
</svg></buttom>`
        data= response.data;
        ArregloDataPag2=[]
        for(let i = 0; i< data.length; i++){
            ArregloDataPag2.push([data[i].id,data[i].nombre,data[i].tipo,data[i].nivel,botones1]);
        }
        let tabla = new DataTable('#tablaWorkout_routine', {
            paging:false,
            scrollY:200,
            data:ArregloDataPag2
        });
        
    }).catch(err=> console.log('error:', err))
}
const CargarRutinasBIG=()=>{
    axios.get('http://127.0.0.1:5000/getRoutines')
    .then(function(response){
        botones2=`<button class="btn btn-danger btn-sm">Delete</button>`
        data= response.data;
        ArregloRutinas=[]
        for(let i = 0; i< data.length; i++){
            ArregloRutinas.push([data[i].Autor,data[i].id_routine,data[i].nombre,data[i].descripcion,data[i].duracion,data[i].nivel,botones2])
        }
        let tablaR = new DataTable('#tablaR', {
            paging:false,
            scrollY:500,
            data:ArregloRutinas
        });
    }).catch(err=> console.log('error:', err))
}
Init_Data();
// tomamos el tabla de los ejercicios
tablab= document.getElementById('tablaWorkout_routine');
// verificamos que no este vacia
if(tablab!=null){
    // creamos el evento de click
    tablab.addEventListener('click',function(e){
        e.stopPropagation();
        // se verifica que el elemento clicado tenga la clase correcta para evitar errores
        if(e.target.className=='btn btn-primary btn-sm'){
            e.stopPropagation();
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
   // }
}
// función para agregar ejercicios a la rutina
let ejerciciosSeleccionados=[];
let totalDuracion= 0;
if(tablab!=null){
    // creamos el evento del click del segundo boton
    tablab.addEventListener('click',function(e){
        e.stopPropagation();
        // verificamos que el elemeto clicado sea el segundo boton
        if(e.target.className == 'btn btn-success btn-sm'){
            e.stopPropagation();
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
            }   ).catch(err=> console.log('error:', err))
            }else{
                alert('El ejercicio ya se encuentra en la lista de la rutina')
            }
        }
    })
}

mensj="";
// se piden los datos del formulario
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

</script>
<div class="container-fluid col-lg-10 px-4"><!--principal-->
  <h3 class="mt-3">RUTINAS</h3>
  <div class="nav nav-tabs" id="nav-tab" role="tablist"><!--div1-->
    <button class="nav-link  btn btn-success active" id="nav-listado-tab" data-bs-toggle="tab" data-bs-target="#nav-listado" type="button" role="tab" aria-controls="nav-listado" aria-selected="true">Listado</button>
    <button class="nav-link  btn btn-success" id="nav-nueva-tab" data-bs-toggle="tab" data-bs-target="#nav-nueva" type="button" role="tab" aria-controls="nav-nueva" aria-selected="false">Nueva</button>
  </div><!--div1-->
  <div class="tab-content" id="nav-tabContent"><!--div2-->
    <div class="tab-pane fade show active" id="nav-listado" role="tabpanel" aria-labelledby="nav-listado-tab"> <!--div3-->
         <!--- TAB LISTADO--->
          <div class="container">
            <div class="table-responsive">
              <table id="tablaR" class="table text-center table-bordered table-striped table-hover table-responsive table-responsive-sm table-responsive-lg table-responsive-md table-responsive-xl" style="width:100%">
                <thead>
                  <tr>
                    <th><b>Creador</b> </th>
                    <th><b>Codigo de rutina</b></th>
                    <th><b>Nombre</b></th>
                    <th><b>Descripción</b></th>
                    <th><b>Duración</b></th>
                    <th><b>Nivel</b></th>
                    <!--<th><b>Acccion</b></th>-->
                  </tr>
                </thead>
                <tbody>
                </tbody>
              </table>
            </div>
          </div>
      <!--FIN TAB LISTADO--->
    </div><!--div3-->
    <div class="tab-pane fade" id="nav-nueva" role="tabpanel" aria-labelledby="nav-nueva-tab"><!--div4-->
      <!--TAB NUEVO--->
    <div class="card border-success mb-3" ><!--div5-->
      <div class="card-header"><b>Nueva rutina</b></div><!--div6-->
      <div class="card-body "><!--div7-->
         <div class="row"><!--div8-->
          <div class="col-lg-6 col-md-6 "><!--div9-->
            <div class="mb-2"><!--div9.1-->
              <label for="txtnombre" class="form-label"><b>Nombre</b></label>
              <input type="text" class="form-control" id="txtnombre" required>
            </div><!--div9.1-->
            <div class="mb-2"><!--div9.2-->
              <label for="txtdescripcion" class="form-label"><b>Descripción</b></label>
              <textarea name="" id="txtdescripcion" class="form-control"></textarea required>                               
            </div><!--div9.2-->
            <div class="mb-2"><!--div9.3-->
              <label for="txtduration" class="form-label"><b>Duracción (min)</b></label>
              <input type="number" class="form-control" id="txtduration" required placeholder="00 min">
            </div><!--div9.3-->
            <div class="mb-2"><!--div9.4-->
              <label for="txtnivel" class="form-label"><b>Nivel</b></label>
              <select id="txtnivel" class="form-control">
                <option selected value="Principiante">Principiante</option>
                <option value="Intermedio">Intermedio</option>
                <option value="Avanzado">Avanzado</option>
              </select>
            </div><!--div9.4--> 
            <div class="mb-2"><!--div9.5-->
              <h4><b>Ejercicios</b></h4>
              <ul id="listaRutina"></ul>
            </div><!--div9.5-->                                   
            <div class="mb-2"><!--div9.6-->
              <button type="button" class="btn btn-dark" >Cancelar</button>
                  <!--onclick="Cancelar()"-->
              <button type="button" class="btn btn-success">Agregar</button>
                  <!--onclick="Registrar_rutina()""-->
            </div><!--div9.6-->
          </div><!--div9-->
                  <!--ejercicios--> 
          <div class="col-lg-6 col-md-6 "><!--div 10-->
             <div class="mb-2"><!--div11-->
              <div class="mb-2"><!--div11.1-->
                <h4 class="text-center"><b>Ejercicios</b></h4>
                <div class="table-responsive"><!--div11.2-->
                  <table id="tablaWorkout_routine" class=" table text-center table-bordered table-striped table-hover" style="width:100%">
                    <thead>
                      <tr>
                        <th scope="col"><b>Id</b></th>
                        <th scope="col"><b>Nombre</b></th>
                        <th scope="col"><b>Tipo</b></th>
                        <th scope="col"><b>Nivel</b></th>
                        <th scope="col"><b>Acccion</b></th>
                      </tr>
                    </thead>
                    <tbody>
                    </tbody>
                  </table>
                </div><!--div11.2-->
              </div><!--div11.1-->
                              <!--PREDICCION DE E-TRAINER-->    
              <div class="justify-content-center"><!--div11.3-->
                <h4 class="h4 text-center">Información</h4>
              </div><!--div11.3-->        
              <form >
                <div class="mb-2 row"><!--div11.4-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.4.1-->
                    <label for="predicName" class="form-label"><b>Ejercicio</b></label>
                    <input type="text" class="form-control" id="predicName" readonly>
                  </div><!--div11.4.1-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.4.2-->
                    <label for="predicType" class="form-label"><b>Tipo</b></label>
                    <input type="text" class="form-control" id="predicType" readonly>
                  </div><!--div11.4.2-->
                </div><!--div11.4-->
                <div class="mb-2 row"><!--div11.5-->
                  <div class="col-lg-12 col-md-12 col-sm-12"><!--div11.5.1-->
                    <label for="predicDescription"><b>Descripción</b></label>
                    <textarea name="" id="predicDescription" class="form-control"></textarea readonly> 
                  </div><!--div11.5.1-->
                </div><!--div11.5-->
                <div class="mb-2 row"><!--div11.6-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.6.1-->
                    <label for="predicEquipment" class="form-label"><b>Equipamiento</b></label>
                    <input type="text" class="form-control" id="predicEquipment" readonly>
                  </div><!--div11.6.1-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.6.2-->
                    <label for="predicLevel" class="form-label"><b>Nivel</b></label>
                    <input type="text" class="form-control" id="predicLevel" readonly>
                  </div><!--div11.6.2-->
                </div><!--div11.6-->
              </form>
             </div><!--div11-->
          </div><!--div10-->
         </div><!--div8-->
      </div><!--div7-->
    </div><!--div5-->          
    </div><!--div4-->  
  </div><!--div2-->                 
</div><!--pincipal-->
                                  
             