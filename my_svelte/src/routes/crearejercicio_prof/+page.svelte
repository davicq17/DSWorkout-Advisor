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
                 
