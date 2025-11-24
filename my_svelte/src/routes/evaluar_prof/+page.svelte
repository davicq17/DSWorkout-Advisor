<script lang="ts">
  import { onMount } from "svelte";
  import axios from "axios";
  import DataTable from 'datatables.net-dt';
	import 'datatables.net-dt/css/dataTables.dataTables.css';
	import { goto } from "$app/navigation";

  // estructura para resivir los datos 
  interface Datos{
    id:number;
    name: string;
    surname: string;
    age:number;
    gender:string;
    height:number;
    weight:number;
    fr_train:string;
    goal:string;
    restrictions:string;
  }
  // estrucutra de la rutina
  interface Rutina{
    id_routine:number;
  }
  // variables reactivas de carga de información 
  let contenido:Datos | null = $state(null);
  let C_nombre= $state("");
  let C_apellido= $state("");
  let C_age = $state(0);
  let C_genero=$state("");
  let C_altura=$state(0);
  let C_peso= $state(0);
  let C_fr_train= $state("");
  //let C_Duration_sesion =$state(0);
  let C_objetivo= $state("");
  //let C_Equipamiento =$state("");
  let C_Restriccion = $state("");

  // variables tabla de ejercicios
  let tablaPD:any;
  let ejercicios:any[]=[];
  let ejerciciosSeleccionados:{id:string,nombre:string}[]=$state([]);
  let totalDuracion = $state(0);

  let predicName = $state("");
  let predicType = $state("");
  let predicDescription = $state("");
  let predicEquipment= $state("");
  let predicLevel= $state("");

  // variables de registrar rutinas
  const {token}=$props();// el token vienen del servidor
  let txtnombreR=$state("");
  let txtdescripcionR=$state("");
  let txtnivelR =$state("");

  // variables para asignar rutina
  let tablaAR:any;
  let Rutinas:any[]=[];
  let rutinaAsignada=$state("");

  // variables de predicción 
  let predic = $state("");
  let predecirBool= $state(false);
  let P_equipamiento = $state("");
  let P_bodypart = $state("");
  let P_type = $state("");
  let P_level =$state("");

  // variables envio de DIagnostico
  let diagnostico = $state("");
  let pro= $state("");
  let cliente:Datos | null = $state(null);
  let rutina:Rutina|null = $state(null);
  // carga cuando ya estse renderizado el DOM
  onMount(()=>{
    CargarInfo();
  });
  // caragr la iformación de cliente a evaluar
  const CargarInfo= ()=>{
    const datos = localStorage.getItem('datos');
   if(datos){
      contenido= JSON.parse(datos) as Datos;
      if(contenido){
          C_nombre= contenido.name;
          C_apellido= contenido.surname;
          C_age = contenido.age;
          C_genero=contenido.gender;
          C_altura= contenido.height;
          C_peso= contenido.weight;
          C_fr_train= contenido.fr_train;
          C_Restriccion = contenido.restrictions;
          //C_Duration_sesion =contenido.duration;
          C_objetivo= contenido.goal;
          //C_Equipamiento = contenido.equipment;
        }
        CargarEjercicios();
    } else{
      alert("no hay datos seleccionados");
      goto('/fisicuser_prof');
    }
  }
// PREDICCÓN CON MACHINE LEARNING
const predecir = async ()=>{
  try{
    // Validar campos antes de enviar
    if (!P_equipamiento || !P_bodypart || !P_type || !P_level) {
      alert("completa todos los campos para predecir el rendimiento.");
      return;
    }
    const res = await axios.post("http://127.0.0.1:8000/Evalucion/predictWorkout",{
      equipment: P_equipamiento,
      bodypart: P_bodypart,
      type: P_type,
      level: P_level
    });
    predic= Number(res.data.Rating).toFixed(3);
    predecirBool=true;
  }catch(err){
    console.log("Error: ",err);
  }
};
  // MODAL DE RUTINA PERSONALISADA
    // FILTRO DE PREDICCIÓN 
    const FiltroPredic = async ()=>{
      if(predecirBool){
        try{
           // realizamos la petición con la predicción
           const response = await axios.get(`http://127.0.0.1:5000/ejercicioFiltro/${predic}`)
           ejercicios= response.data;
           if(ejercicios.length>0){
             if(tablaPD) tablaPD.destroy?.();
              tablaPD = new DataTable('#tablaWorkout_Personal',{
              data: ejercicios.map(e =>[
                e.id,
                e.nombre,
                e.tipo,
                e.rating,
                `<button type="button" class="btn btn-success btn-sm" data-id="${e.id}" data-name="${e.nombre}" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                    </svg></button> <button class= "btn btn-primary btn-sm" data-id="${e.id}" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                  </svg></button>`
              ]),
              paging:false,
              scrollY:"200px"
            })
            const handleClick = (e: Event) => ClickEjercicio(e as MouseEvent);
            document.querySelector("#tablaWorkout_Personal")?.removeEventListener("click", handleClick);
            // se escuchan los eventos de click
            document.querySelector("#tablaWorkout_Personal")?.addEventListener("click", handleClick);
           }else{
            alert("No se encontraron ejercicios con puntaje similar a "+predic);
           }
        }catch(err){
          console.log("error: ",err);
        }
      }else{
        alert("Aun no haz realizado una predicción");
      }
    } 
    // FUNCIONES TABLA EJERCICIOS
    const CargarEjercicios = async ()=>{
    try{
      // realizamos la petición
      const response = await axios.get('http://127.0.0.1:8000/Workout/ejercicioTabla')
      ejercicios= response.data;
      if(tablaPD) tablaPD.destroy?.();
      tablaPD = new DataTable('#tablaWorkout_Personal',{
        data: ejercicios.map(e =>[
          e.id,
          e.nombre,
          e.tipo,
          e.rating,
          `<button type="button" class="btn btn-success btn-sm" data-id="${e.id}" data-name="${e.nombre}" data-bs-target="#Agregar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
              <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
              </svg></button> 
              <button class= "btn btn-primary btn-sm" data-id="${e.id}" data-bs-target="#Información"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
              <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
            </svg></button>`
        ]),
        paging:false,
        scrollY:"200px",
      })
      const handleClick = (e: Event) => ClickEjercicio(e as MouseEvent);
      document.querySelector("#tablaWorkout_Personal")?.removeEventListener("click", handleClick);
      // se escuchan los eventos de click
      document.querySelector("#tablaWorkout_Personal")?.addEventListener("click", handleClick);
    }catch(err){
      console.error("Error cargando ejercicios:",err);
    }
  }
// se maneja el evento del click
  const ClickEjercicio = (e:MouseEvent)=>{
    e.stopPropagation();
    const btn = (e.target as HTMLElement | null)?.closest('button') as HTMLButtonElement | null;
    if(!btn) return;
    const id = btn.dataset.id;
    const nombre= btn.dataset.name;
    if(!id)return;
    // verificamos sobre cual boton se hizo click
    if(btn.classList.contains("btn-success")){
      if(!nombre)return;
      // agrega el ejercicio a la rutina
      e.stopPropagation();
      AgregarEjercico(id,nombre);
    }else if(btn.classList.contains("btn-primary")){
      //muestra la información del ejercicio  
      e.stopPropagation();
      CargarInformacion(id);
    }
  }

  const CargarInformacion = async (id: string) => {
    try {
      const { data } = await axios.get(`http://127.0.0.1:8000/Workout/WorkoutById/${id}`);
      predicName = data.nombre;
      predicType = data.type;
      predicDescription = data.desc;
      predicEquipment = data.equipment;
      predicLevel = data.level;
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
  // FUNCIONES REGISTRAR RUTINA PERSONALIZADA 
  const RegistrarRutina = async()=>{
    try{
      // se define el creador de la rutina
      const verify = await axios.get(`http://127.0.0.1:8000/Login/verify_token/${token}`);
      const creadorR= verify.data.id;
      console.log("creador: ",creadorR)
      console.log("ejerciciso a guardar:",ejerciciosSeleccionados.map(e=>e.id).join(","))
      await axios.post("http://127.0.0.1:8000/Routine/regisRutina",{
          creador: creadorR,
          nombre: txtnombreR,
          descripcion: txtdescripcionR,
          duracion: totalDuracion,
          nivel: txtnivelR,
          ejercicios: ejerciciosSeleccionados.map(e=> e.id).join(";"), 
      });

      alert("Rutina registrada correctamente.");
      Cancelar();
    }catch(err){
      console.log('error :',err);
    }
  }

  const Cancelar = ()=>{
    txtnombreR= "";
    txtdescripcionR="";
    txtnivelR="";
    ejerciciosSeleccionados = [];
    totalDuracion=0;

  }

  // ASIGNAR RUTINA
  const AsignarRutina = async ()=>{
    try{
      // cargar las rutinas al modal de las rutinas
      const response = await axios.get("http://127.0.0.1:8000/Routine/RutinaModal");
      Rutinas = response.data;
      if(tablaAR) tablaAR.destroy?.();
      tablaAR = new DataTable('#tablaRutinas',{
        data: Rutinas.map(r =>[
          r.id_routine,
          r.nombre,
          r.ejercicios,
          `<button id="asignar" class="btn btn-success asignar" data-id='${r.id_routine}' data-name='${r.nombre}' data-bs-dismiss="modal">Asignar</button>`
        ]),
        paging:false,
        scrollY:"200px",
      })
      // menjo del click 
      document.querySelector("#tablaRutinas")?.addEventListener("click", (e) => {
        e.stopPropagation();
        const target = e.target as HTMLElement;
        const id = target.dataset.id;
        const nombre = target.dataset.name;
        if (target.classList.contains("asignar")) {
          e.stopPropagation();
          rutinaAsignada = nombre!;
          sessionStorage.setItem("Rutina", JSON.stringify({ id_routine: id, nombre }));
        }
      });
    }catch(err){
      console.log("Erro :",err);
    }
  }

  // DIAGNOSTICO
  const EnvioDiagnostico = async ()=>{
    if(diagnostico===""){
      alert("Diagnostico en blanco, porfavor verifique.");
      return
    }
    
    try{
      const response = await axios.get(`http://127.0.0.1:8000/Login/verify_token/${token}`);
      pro= response.data.id;
      const datos = localStorage.getItem('datos');
      const dataR= sessionStorage.getItem('Rutina');
      if(datos)cliente= JSON.parse(datos) as Datos;
      if(dataR)rutina = JSON.parse(dataR) as Rutina;
      const date = new Date();
      const fecha = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
      if(cliente && rutina){
        const postRes = await axios.post('http://127.0.0.1:5000/addDiagnostico',{
          id_cliente:cliente.id,
          id_prof:pro,
          fecha:fecha,
          diagnostico:diagnostico,
          rutina:rutina.id_routine  
      });
      alert(postRes.data.informacion || "Diagnostico enviado correctamente")
      }
      goto("/fisicuser_prof");
    }catch(err){
      console.log("Erro :",err);
    }
  }

  //VOLVER
  const volver=()=>{
    localStorage.removeItem('datos');
    goto("/fisicuser_prof")
  };
</script>
<div class="container col-sm-10 col-lg-8 col-md-10  my-5" ><!--principal-->
  <div><!--div1-->
    <button class="btn" aria-label="volver" >
      <a  onclick={volver} href="##" aria-label="volver" class="text-decoration-none text-dark" ><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-arrow-bar-left" viewBox="0 0 16 16">
      <path fill-rule="evenodd" d="M12.5 15a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5M10 8a.5.5 0 0 1-.5.5H3.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L3.707 7.5H9.5a.5.5 0 0 1 .5.5"/>
        </svg></a>
    </button>
  </div><!--div1-->
  <div class="justify-content-center"><!--div2-->
    <h3 class="h3 fw-bold text-center">Estado Fisico</h3>
  </div><!--div2-->
  <form class="row g-3">
    <div class="col-sm-12 col-md-6">
      <label class="fw-bold" for="inputnombre">Nombre</label>
      <input bind:value={C_nombre} type="text" class="form-control" placeholder="Nombre" aria-label="First name" id="inputnombre" readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label class="fw-bold" for="inputApellido">Apellido</label>
      <input bind:value={C_apellido} type="text" class="form-control" placeholder="Apellido" aria-label="Last name" id="inputApellido"readonly>
    </div>
    <div class="col-sm-12 col-md-6 ">
      <label class="fw-bold" for="inputage">Edad</label>
      <input bind:value={C_age} type="text" class="form-control" id="inputage" placeholder="Edad"readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label class="fw-bold" for="inputgenero">Genero</label>
      <input bind:value={C_genero} type="text" class="form-control" id="inputgenero"readonly>
    </div>
    <div class="col-md-6">
      <label class="fw-bold" for="inputpeso">Peso(kg)</label>
      <input bind:value={C_peso} type="text" class="form-control" id="inputpeso"readonly>
    </div>
    <div class="col-sm-12 col-md-6">
      <label class="fw-bold" for="inputAltura">Altura(m)</label>
      <input bind:value={C_altura} type="text" class="form-control" id="inputAltura" placeholder="Altura(m)"readonly>
    </div>
      <div class="col-sm-12 col-md-6">
        <label  for="inputfr_train" class="form-label fw-bold">Frecuencia con la que realiza actividad fisica</label>
        <input bind:value={C_fr_train} type="text" id="inputfr_train" class="form-control"readonly>
      </div>
      <!-- <div class="col-sm-12 col-md-6">
        <label for="inputDuration_sesion" class="form-label">Duracion de la sesión de ejerccio tipica</label>
        <input bind:value={C_Duration_sesion} type="text" class="form-control" id="inputDuration_sesion"readonly>
      </div> -->
      <div class="col-sm-12 col-md-6">
        <label for="inputObjetivo" class="form-label fw-bold">Objetivo</label>
        <input bind:value={C_objetivo} type="text" class="form-control" id="inputObjetivo"readonly>
      </div>
      <!--<div class="col-sm-12 col-md-6">
        <label for="inputEquipamiento" class="form-label">Equipamiento</label>
        <textarea bind:value={C_Equipamiento} name="" id="inputEquipamiento" class="form-control" readonly></textarea>
      </div> -->
      <div class="col-md-12">
        <label for="inputRestricción_alimenticia" class="form-label fw-bold">Restricciones alimenticias</label>
        <input bind:value={C_Restriccion} type="text" class="form-control" id="inputRestricción_alimenticia"readonly>
      </div>
  </form>
        <!--Diagnostico del cliente-->
  <div><!--div3-->
    <div class="justify-content-center"><!--div3.1-->
      <h4 class="h4 fw-bold text-center">Diagnostico</h4>
    </div><!--div3.1-->
    <div class="form-floating mb-3 col-lg-12"><!--div3.2-->
      <textarea class="form-control" placeholder="Leave a comment here" id="diagnostico" style="height: 100px; resize:none" ></textarea>
      <label for="diagnostico">Escriba aqui su diagnostico</label>
    </div><!--div3.2-->
    <div><!--div3.3-->
       <div class="row"><!--div3.4-->
          <div class="col-sm-12 col-md-6 mb-2">
            <label class="fw-bold" for="inputTypePredic">Tipo de ejercicios</label>
            <select bind:value={P_type} id="inputTypePredic" class="form-select">
              <option value="Strength" selected>Fuerza</option>
              <option value="Stretching">Estiramiento</option>
              <option value="Plyometrics">Pilometría</option>
              <option value="Powerlifting">Levantamiento de pesas</option>
              <option value="Cardio">Cardio</option>
            </select>
          </div>

          <div class="col-sm-12 col-md-6 mb-2">
              <label class="fw-bold" for="inputBodypartPredic">Parte del cuerpo</label>
              <select bind:value={P_bodypart} id="inputBodypartPredic" class="form-select">
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
            <label class="fw-bold" for="inputLevelPredic">Nivel del ejercicio</label>
            <select bind:value={P_level} id="inputLevelPredic" class="form-select">
              <option value="Beginner" selected>Principiante</option>
              <option value="Intermediate">Intermedio</option>
              <option value="Expert">Experto</option>
            </select>
          </div>
          <div class="col-sm-12 col-md-6">
            <label class="fw-bold" for="inputEquipamiento"> Equipamiento</label>
            <select bind:value={P_equipamiento} id="inputEquipamiento" class="form-select">
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
            <input bind:value={predic} type="text" readonly id="predic" class="form-control">
            <div class="col-md-6 my-1">
              <button onclick={predecir} type="button" class="btn btn-success my-2" >Predecir</button>
            </div>
          </div>
          <div class="col-lg-6 col-md-6">
            <label class="fw-bold" for="RutinaA">Rutina Asignada</label>
            <input bind:value={rutinaAsignada} type="text" id="RutinaA" class="form-control" readonly placeholder="Rutina sin asignar">
          </div>
        </div><!--div3.6--> 
          <div class="col-lg-12 mt-2"><!--div3.7-->
            <button class="btn btn-primary me-2 mb-2">
              <a onclick={AsignarRutina} href="##" data-bs-toggle="modal" data-bs-target="#Asignar" class="text-decoration-none text-white">asignar Rutina</a>
            </button>
            <button onclick={EnvioDiagnostico}  class="btn btn-success me-2 mb-2 text-decoration-none text-white">
              Enviar diagnostico
            </button>
            <button data-bs-toggle="modal" data-bs-target="#rutinaPersonalizada" class="btn btn-info me-2 text-decoration-none text-white">
              Crear Rutina Personalizada
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
            <button onclick={FiltroPredic} class="btn btn-success my-2">Recomendacion</button>
            <button onclick={CargarEjercicios}  class="btn btn-secondary">Quitar Recomendacion</button>
          </div>
        </div><!--div5.1.2-->
              <div class="modal-body"><!--div5.1.3-->
                <div class="row">
                   <div class="col-lg-6 col-md-6 ">
                       <div class="mb-2">
                         <label for="txtnombre" class="form-label"><b>Nombre</b></label>
                         <input bind:value={txtnombreR} type="text" class="form-control" id="txtnombre" required>
                      </div>
                      <div class="mb-2">
                        <label for="txtdescripcion" class="form-label"><b>Descripción</b></label>
                        <textarea bind:value={txtdescripcionR} name="" id="txtdescripcion" class="form-control"></textarea required>                               
                      </div>
                      <div class="mb-2">
                        <label for="txtduration" class="form-label"><b>Duracción (min)</b></label>
                        <input bind:value={totalDuracion} type="number" class="form-control" id="txtduration" required placeholder="00 min">
                      </div>
                      <div class="mb-2">
                        <label for="txtnivel" class="form-label"><b>Nivel</b></label>
                        <select bind:value={txtnivelR} id="txtnivel" class="form-control">
                          <option selected value="Principiante">Principiante</option>
                          <option value="Intermedio">Intermedio</option>
                          <option value="Avanzado">Avanzado</option>
                        </select>
                      </div> 
                      <div class="mb-2">
                        <h4><b>Ejercicios</b></h4>
                        <ul id="listaRutina">
                          {#each ejerciciosSeleccionados as ejerc }
                              <li>{ejerc.nombre}</li>
                          {/each}
                        </ul>
                      </div>
                                                                    
                      <div class="mb-2">
                        <button onclick={Cancelar} type="button" class="btn btn-dark" >Cancelar</button>
                          
                        <button onclick={RegistrarRutina} type="button" data-bs-dismiss="modal" class="btn btn-success" >Agregar</button>
                            
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
                            <input bind:value={predicName} type="text" class="form-control" id="predicName" readonly>
                          </div>
                          <div class="col-lg-6 col-md-6 col-sm-12">
                              <label for="predicType" class="form-label"><b>Tipo</b></label>
                              <input bind:value={predicType} type="text" class="form-control" id="predicType" readonly>
                          </div>
                        </div>
                        <div class="mb-2 row">
                          <div class="col-lg-12 col-md-12 col-sm-12">
                            <label for="predicDescription"><b>Descripción</b></label>
                            <textarea bind:value={predicDescription} name="" id="predicDescription" class="form-control" readonly></textarea> 
                          </div>
                        </div>
                        <div class="mb-2 row">
                          <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="predicEquipment" class="form-label"><b>Equipamiento</b></label>
                            <input bind:value={predicEquipment} type="text" class="form-control" id="predicEquipment" readonly>
                          </div>
                          <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="predicLevel" class="form-label"><b>Nivel</b></label>
                            <input bind:value={predicLevel} type="text" class="form-control" id="predicLevel" readonly>
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