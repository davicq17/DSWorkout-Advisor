<script>
    mensj="";
// pido los datos del formulario
const Registrar = () =>{
    nombreI=document.getElementById("inputNombre").value;
    guideI=document.getElementById("inputGuia").value;
    tipoI=document.getElementById("inputTipo").value;
    equipoI=document.getElementById("inputEquipo").value;
    nivelI=document.getElementById("inputNivel").value;
    repetitionsI=document.getElementById("inputRepeticion").value;
    seriesI=document.getElementById("inputSeries").value;
    durationI=document.getElementById("inputDuracion").value;
    console.log(nombreI,guideI,tipoI,equipoI,nivelI,repetitionsI,seriesI,durationI);
    //se verifica que no allán campos vacios
    if(nombreI !="" ||
        guideI !="" ||
        tipoI !="" ||
        equipoI !="" ||
        nivelI !="" ||
        repetitionsI !="" ||
        seriesI !="" ||
        durationI !=""
    ){
        axios({
            //se realiza el envio de los datos con la ruta
            method: "POST",
            url: "http://127.0.0.1:5000/registroEjercicio",
            data: {
                nombre: nombreI,
                guia: guideI,
                tipo: tipoI,
                equipo: equipoI,
                nivel: nivelI,
                repeticiones: repetitionsI,
                series: seriesI,
                duracion: durationI
            },
        }).then(function(response){
            alert(response.data.informacion)
            // se recarga la pagina
            window.location.href='crearEjercicio.html'
        }).catch((err)=>console.log("Error:", err));
    } else{
        // si hay campos vacios muestra una alerta
        alert("Verifique que no existan campos vacios!");
    }
};

// workoutTable.js

//const tabla= document.querySelector('#tablaWorkout tbody');

let tabla = new DataTable('#tablaWorkout', {
    paging:false,
    scrollY:400
});
const Init_Data =() =>{
    axios.get('http://127.0.0.1:5000/ejercicioTabla')
    .then(function(response){0
        botones=`<buttom type="buttom" class="btn btn-warning ms-3 btn-sm" data-bs-toggle="modal" data-bs-target="#Editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
</svg></Buttom>`
        data= response.data;
        for(let i = 0; i< data.length; i++){
            tabla.row.add([data[i].id,data[i].nombre,data[i].guia,data[i].tipo,data[i].equipo,data[i].nivel,data[i].repeticiones,data[i].series,data[i].duracion,botones]).draw();
            /*let row = tabla.insertRow(tabla.length);
            id = row.insertCell(0);
            id.innerHTML = data[i].id;
            
            row.insertCell(1).innerHTML = data[i].nombre;
            row.insertCell(2).innerHTML = data[i].guia;
            row.insertCell(3).innerHTML = data[i].tipo;
            row.insertCell(4).innerHTML = data[i].equipo;
            row.insertCell(5).innerHTML = data[i].nivel;
            row.insertCell(6).innerHTML = data[i].repeticiones;
            row.insertCell(7).innerHTML = data[i].series;
            row.insertCell(8).innerHTML = data[i].duracion;
            row.insertCell(9).innerHTML = `<button class="btn btn-danger btn-sm">Delete</button>`;*/
        }
    }).catch(err=> console.log('error:', err))
}
Init_Data();
</script>
<main>
    <div class="container col-lg-10 col-md-10 col-sm-12">
        <h3 class="mt-3">EJERCICIOS</h3>
        <a class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#AddEjercicio">Agregar ejercicio</a>                

        <div class="table-responsive">
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
        </div>
    </div>
                     
                    <!--Modal para creacion de ejercicios-->
    <div class="modal fade" tabindex="-1" id="AddEjercicio" >
        <div class="modal-dialog" >
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="text-center my-3">Nuevo ejercicio</h1>
                </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputNombre" class="form-label"><b>Nombre</b></label>
                                <input type="text" class="form-control" id="inputNombre" required>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputGuia" class="form-label"><b>Guia</b></label>
                                <textarea name="" id="inputGuia" class="form-control"></textarea required>                               
                            </div>
                        </div>
                        <div class="row">
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputTipo"><b>Tipo</b></label>
                                <select id="inputTipo" class="form-select">
                                    <option value="Strength" selected>Fuerza</option>
                                    <option value="Stretching">Estiramiento</option>
                                    <option value="Plyometrics">Pilometría</option>
                                    <option value="Powerlifting">Levantamiento de pesas</option>
                                    <option value="Cardio">Cardio</option>
                                </select>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputEquipo" class="form-label"><b>Equipo</b></label>
                                <input type="text" class="form-control" id="inputEquipo" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputNivel"><b>Nivel</b></label>
                                <select id="inputNivel" class="form-select">
                                    <option value="Beginner" selected>Principiante</option>
                                    <option value="Intermediate">Intermedio</option>
                                    <option value="Expert">Experto</option>
                                </select>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputRepeticion" class="form-label"><b>Repeticiones</b></label>
                                 <input type="number" class="form-control" id="inputRepeticion" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputSeries" class="form-label"><b>Series</b></label>
                                <input type="number" class="form-control" id="inputSeries" required>
                            </div>
                            <div class="mb-2 col-sm-12 col-xs-12 col-md-6 col-lg-6">
                                <label for="inputDuracion" class="form-label"><b>Duración (min)</b></label>
                                <input type="number" class="form-control" id="inputDuracion" placeholder="00" required>
                            </div>      
                        </div> 
                 </div>
                <div class="modal-footer d-flex justify-content-around">
                    <button type="button" class="btn btn-dark" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-success" >Agregar</button>
                    <!--onclick="Registrar()"-->
                </div>
                
            </div>
        </div>
    </div>
</main>
                 
