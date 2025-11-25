<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
	import axios from "axios";
  import { onMount } from "svelte";
  import DataTable from 'datatables.net-dt';
  import 'datatables.net-dt/css/dataTables.dataTables.css';
  let token: string = $state('');
// variables de ejercicios
  let tabla:any;
  let ejercicios:any[]=[];
  let ejerciciosSeleccionados:{id:string,nombre:string}[]=$state([]);
  let totalDuracion = $state(0);

  let EName = $state("");
  let EType = $state("");
  let EDescription = $state("");
  let EEquipment= $state("");
  let ELevel= $state("");
// variables de rutinas
 let tablaR:any;
 let rutinas:any[]=$state([]);

 let nombreR=$state("");
 let descripcionR=$state("");
 let nivleR =$state("");

  //CARGA DE TABLAS PARA INTERFAZ DE PROFESIONAL
  onMount(() =>{
      CargarEjercicios()
      CargarRutinasBIG()
  });

  // FUNCIONES DE EJERCICIOS
  const CargarEjercicios = async ()=>{
    try{
      // realizamos la petición
      const response = await axios.get('http://127.0.0.1:8000/Workout/EjercicioTabla')
      ejercicios= response.data;
      if(tabla) tabla.destroy?.();
      tabla = new DataTable('#tablaWorkout_routine',{
        data: ejercicios.map(e =>[
          e.id,
          e.nombre,
          e.tipo,
          e.nivel,
          `<button type="button" class="btn btn-success btn-sm" data-id="${e.id}" data-name="${e.nombre}" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
              <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
              </svg></button> <button class= "btn btn-primary btn-sm" data-id="${e.id}" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
              <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
            </svg></button>`
        ]),
        paging:false,
        scrollY:"500px"
      })
      document.querySelector('#tablaWorkout_routine')?.removeEventListener("click",(e:Event)=>{
        ClickEjercicio(e as MouseEvent)
      });
      // se escuchan los eventos de click
      document.querySelector("#tablaWorkout_routine")?.addEventListener("click",(e: Event)=>{
        ClickEjercicio(e as MouseEvent);
      });

    }catch(err){
      console.error("Error cargando ejercicios:",err);
    }
  }
// se maneja el evento del click
  const ClickEjercicio = (e:MouseEvent)=>{
    const target = e.target as HTMLElement;
    const id = target.dataset.id || target.dataset.info;
    const nombre= target.dataset.name;
    if(!id)return;
    // verificamos sobre cual boton se hizo click
    if(target.classList.contains("btn-success")){
      if(!nombre)return;
      // agrega el ejercicio a la rutina
      AgregarEjercico(id,nombre);
    }else if(target.classList.contains("btn-primary")){
      //muestra la información del ejercicio  
      CargarInformacion(id);
    }
  }

  const CargarInformacion = async (id: string) => {
    try {
      const { data } = await axios.get(`http://127.0.0.1:8000/Workout/WorkoutById/${id}`);
      EName = data.nombre;
      EType = data.type;
      EDescription = data.desc;
      EEquipment = data.equipment;
      ELevel = data.level;
    } catch (err) {
      console.error("Error al cargar información:", err);
    }
  };

  const AgregarEjercico =  async (id:string, nombre:string)=>{
    // verica que el ejercicio no este en la rutina
    if(ejerciciosSeleccionados.some(e=> e.id === id)){
      alert("El ejerccio ya está en la lista");
      return;
    }
    // se actualiza la lista de la rutina
    ejerciciosSeleccionados = [...ejerciciosSeleccionados,{id, nombre}];

    // se actualiza la duración de la rutina
    try{
      const {data}= await axios.get(`http://127.0.0.1:8000/Workout/WorkoutById/${id}`);
      totalDuracion += data.duration;
    }catch(err){
      console.log("error :",err)
    }

  }

  // FUNCIONES DE RUTINAS
  const CargarRutinasBIG= async ()=>{
    try{
      // realizamos la petición de las rutinas 
      const respon = await axios.get('http://127.0.0.1:8000/Routine/getRoutines');
      rutinas= respon.data;
      if(tablaR) tablaR.destroy?.();
      tablaR = new DataTable('#tablaR',{
        paging:false,
        scrollY:"500px",
        data: rutinas.map(r=>[
          r.Autor,
          r.id_routine,
          r.nombre,
          r.descripcion,
          r.duracion,
          r.nivel,
          `<button class="btn btn-danger btn-sm">Delete</button>`
        ])
      })
    }catch(err){
      console.log("error:",err)
    }
  }

  const RegistrarRutina = async()=>{
    if(nombreR ==="" || descripcionR ==="" || totalDuracion ===0 || nivleR ===""){
        alert("verifique que no existan campos vacios!");
        return
     }
    try{
      token = localStorage.getItem('token') || '';
      // se define el creador de la rutina
      const verify = await axios.get(`http://127.0.0.1:8000/Login/verify_token/${token}`);
      const creadorR= verify.data.id;
      console.log("creador: ",creadorR)
      console.log("ejerciciso a guardar:",ejerciciosSeleccionados.map(e=>e.id).join(","))
      await axios.post("http://127.0.0.1:8000/Routine/regisRutina",{
          creador: creadorR,
          nombre: nombreR,
          descripcion: descripcionR,
          duracion: totalDuracion,
          nivel: nivleR,
          ejercicios: ejerciciosSeleccionados.map(e=> e.id).join(","), 
      });

      alert("Rutina registrada correctamente.");
      cancelar();
      CargarRutinasBIG();
    }catch(err){
      console.log('error :',err);
    }
  }

  const cancelar = ()=>{
    nombreR= "";
    descripcionR="";
    nivleR="";
    ejerciciosSeleccionados = [];
    totalDuracion=0;

  }
</script>
<Navbar/>
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
              <input bind:value={nombreR} type="text" class="form-control" id="txtnombre" required>
            </div><!--div9.1-->
            <div class="mb-2"><!--div9.2-->
              <label for="txtdescripcion" class="form-label"><b>Descripción</b></label>
              <textarea bind:value={descripcionR} name="" id="txtdescripcion" class="form-control"></textarea required>                               
            </div><!--div9.2-->
            <div class="mb-2"><!--div9.3-->
              <label for="txtduration" class="form-label"><b>Duracción (min)</b></label>
              <input type="number" class="form-control" bind:value={totalDuracion} id="txtduration" required placeholder="00 min" readonly>
            </div><!--div9.3-->
            <div class="mb-2"><!--div9.4-->
              <label for="txtnivel" class="form-label"><b>Nivel</b></label>
              <select bind:value={nivleR} id="txtnivel" class="form-control">
                <option selected value="Principiante">Principiante</option>
                <option value="Intermedio">Intermedio</option>
                <option value="Avanzado">Avanzado</option>
              </select>
            </div><!--div9.4--> 
            <div class="mb-2"><!--div9.5-->
              <h4><b>Ejercicios</b></h4>
              <ul id="listaRutina">
                {#each ejerciciosSeleccionados as ejerc }
                  <li>{ejerc.nombre}</li>
                {/each}
              </ul>
            </div><!--div9.5-->                                   
            <div class="mb-2"><!--div9.6-->
              <button onclick={cancelar} type="button" class="btn btn-dark" >Cancelar</button>
              <button onclick={RegistrarRutina} type="button" class="btn btn-success">Agregar</button>
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
                    <input bind:value={EName} type="text" class="form-control" id="predicName" readonly>
                  </div><!--div11.4.1-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.4.2-->
                    <label for="predicType" class="form-label"><b>Tipo</b></label>
                    <input bind:value={EType} type="text" class="form-control" id="predicType" readonly>
                  </div><!--div11.4.2-->
                </div><!--div11.4-->
                <div class="mb-2 row"><!--div11.5-->
                  <div class="col-lg-12 col-md-12 col-sm-12"><!--div11.5.1-->
                    <label for="predicDescription"><b>Descripción</b></label>
                    <textarea bind:value={EDescription} name="" id="predicDescription" class="form-control" readonly></textarea> 
                  </div><!--div11.5.1-->
                </div><!--div11.5-->
                <div class="mb-2 row"><!--div11.6-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.6.1-->
                    <label for="predicEquipment" class="form-label"><b>Equipamiento</b></label>
                    <input bind:value={EEquipment} type="text" class="form-control" id="predicEquipment" readonly>
                  </div><!--div11.6.1-->
                  <div class="col-lg-6 col-md-6 col-sm-12"><!--div11.6.2-->
                    <label for="predicLevel" class="form-label"><b>Nivel</b></label>
                    <input bind:value={ELevel} type="text" class="form-control" id="predicLevel" readonly>
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
                                  
             