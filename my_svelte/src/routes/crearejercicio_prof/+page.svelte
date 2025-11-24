<script lang="ts">
    import Navbar from '$lib/components/Navbar.svelte';
   import axios from "axios";
   import { onMount } from "svelte";
   import DataTable from 'datatables.net-dt';
   import 'datatables.net-dt/css/dataTables.dataTables.css';
 // variables del registro de un ejercicio
   let nombreI= $state("");
   let guideI= $state("");
   let tipoI= $state("");
   let equipoI= $state("");
   let nivelI= $state("");
   let repetitionsI= $state(0);
   let seriesI = $state(0);
   let durationI = $state(0);
 // variables de la tabla de ejercicios
 let tabla:any;
 let ejercicios:any[]= [];

   // inciar datos de la tabla de ejercicos
   const Init_Data = async()=>{
    try{
        // se realiza la petición
        const response = await axios.get("http://127.0.0.1:8000/Workout/ejercicioTabla");
        ejercicios = await response.data;
        console.log('ejerciios cargados:',ejercicios)
    }catch(err){
        console.log("Error:", err);
    }
   }
   // registro de un ejercicio 
   const Registrar = async ()=>{
    console.log("se registrara un ejericicio")
    // verificamos campos vacios 
     if(nombreI ==="" || guideI ==="" ||tipoI ==="" ||equipoI ==="" ||nivelI ==="" ||repetitionsI ===0 ||seriesI ===0 
     ||durationI ===0){
        alert("verifique queno existan campos vacios!");
        return
     }
     try{
        // se envian los datos a la ruta de la api
        await axios.post("http://127.0.0.1:8000/Workout/registroEjercicio",{
            nombre:nombreI,
            guia:guideI,
            tipo:tipoI,
            equipo:equipoI,
            nivel:nivelI,
            repeticiones:repetitionsI,
            series:seriesI,
            duracion:durationI
        });

        // se recarga la pagina
        window.location.href="/crearejercicio_prof"
     }catch(err){
        console.log("Error:",err);
     }
   }
   // se carga los datos antes qde que cargue el don
 onMount(async()=>{
    await Init_Data();
    if(tabla){
        tabla.destroy();
        tabla=null;
    }
    if(ejercicios.length > 0 && !tabla){
      // creamos la tabla
      tabla= new DataTable("#tablaWorkout",{
        data: ejercicios.map(e =>[
            e.id,
            e.nombre,
            e.guia,
            e.tipo,
            e.equipo,
            e.nivel,
            e.repeticiones,
            e.series,
            e.duracion,
            // boton
            `<button aria-label="editar ejercicio" data-id="${e.id}" class="btn btn-warning ms-3 btn-sm btn-editar" data-bs-toggle="modal" data-bs-target="#Editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                </svg>
            </button>`
        ]),
        paging:false,
        scrollY:"400px"
      });

      // se captan los click del boton 
      document.querySelector("#tablaWorkout")?.addEventListener("click", (e)=>{
        const btn = (e.target as HTMLElement).closest(".btn-editar");
        if (btn) {
            const id = btn.getAttribute("data-id");
            // Aquí llamas a la función que abre el modal o carga los datos
            console.log("Editar ejercicio con id:", id);
            // Ejemplo: abrir modal o llenar campos si ya lo tienes implementado
        }
      })
    }
 })
// se crea la data Table luego de confirmar que existen datos
 $effect(()=>{});
</script>
<Navbar/>
<main>
    <div class="container col-lg-10 col-md-10 col-sm-12"><!--div1-->
        <h3 class="mt-3">EJERCICIOS</h3>
        <button class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#AddEjercicio">Agregar ejercicio</button>                
        <div class="table-responsive"><!--div1.1-->
            <table id="tablaWorkout" class=" table text-center table-bordered table-striped table-hover table-responsive table-responsive-sm table-responsive-lg table-responsive-md table-responsive-xl" style="width:100%">
                <thead>
                    <tr>
                        <th><b>Id</b> </th>
                        <th><b>Nombre</b></th>
                        <th><b>Guia</b></th>
                        <th><b>Tipo</b></th>
                        <th><b>Equipo</b></th>
                        <th><b>Nivel</b></th>
                        <th><b>Repeticiones</b></th>
                        <th><b>Series</b></th>
                        <th><b>Duración</b></th>
                        <!--<th><b>Acccion</b></th>-->
                    </tr>
                </thead>
                <tbody class="text-center">
                </tbody>
            </table>
        </div><!--div.1.1-->
    </div><!--div1-->               
                    <!--Modal para creacion de ejercicios-->
    <div class="modal fade" tabindex="-1" id="AddEjercicio" ><!--div2-->
        <div class="modal-dialog" ><!--div2.1-->
            <div class="modal-content"><!--div2.2-->
                <div class="modal-header"><!--div2.3-->
                    <h1 class="text-center my-3">Nuevo ejercicio</h1>
                </div><!--div2.3-->
                    <div class="modal-body"><!--div2.4-->
                        <div class="row"><!--div2.4.1-->
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputNombre" class="form-label"><b>Nombre</b></label>
                                <input bind:value={nombreI} type="text" class="form-control" required>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputGuia" class="form-label"><b>Guia</b></label>
                                <textarea bind:value={guideI} class="form-control" required></textarea>                               
                            </div>
                        </div><!--div2.4.1-->
                        <div class="row"><!--div2.4.2-->
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputTipo"><b>Tipo</b></label>
                                <select bind:value={tipoI} class="form-select">
                                    <option value="Strength" selected>Fuerza</option>
                                    <option value="Stretching">Estiramiento</option>
                                    <option value="Plyometrics">Pilometría</option>
                                    <option value="Powerlifting">Levantamiento de pesas</option>
                                    <option value="Cardio">Cardio</option>
                                </select>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputEquipo" class="form-label"><b>Equipo</b></label>
                                <input bind:value={equipoI} type="text" class="form-control" required>
                            </div>
                        </div><!--div2.4.2-->
                        <div class="row"><!--div2.4.3-->
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputNivel"><b>Nivel</b></label>
                                <select bind:value={nivelI} class="form-select">
                                    <option value="Beginner" selected>Principiante</option>
                                    <option value="Intermediate">Intermedio</option>
                                    <option value="Expert">Experto</option>
                                </select>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputRepeticion" class="form-label"><b>Repeticiones</b></label>
                                 <input bind:value={repetitionsI} type="number" class="form-control" required>
                            </div>
                        </div><!--div2.4.3-->
                        <div class="row"><!--2.4.4-->
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputSeries" class="form-label"><b>Series</b></label>
                                <input bind:value={seriesI} type="number" class="form-control" id="inputSeries" required>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputDuracion" class="form-label"><b>Duración (min)</b></label>
                                <input bind:value={durationI} type="number" class="form-control" id="inputDuracion" placeholder="00" required>
                            </div>      
                        </div><!--div2.4.4-->
                 </div><!--div2.4-->
                 <div class="modal-footer d-flex justify-content-around"><!--div2.5-->
                    <button type="button" class="btn btn-dark" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" onclick={Registrar} class="btn btn-success" >Agregar</button>
                 </div><!--div2.5-->
            </div><!--div2.2-->
        </div><!--div2.1-->
    </div><!--div2-->
</main>
                 
