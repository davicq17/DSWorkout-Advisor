<div class="container col-sm-10 col-lg-8 col-md-10  my-5" >
        <div>
            <div>
              <button class="btn"><a class="text-decoration-none text-dark" ><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-arrow-bar-left" viewBox="0 0 16 16">
                <!--onclick="volver()"-->
                  <path fill-rule="evenodd" d="M12.5 15a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5M10 8a.5.5 0 0 1-.5.5H3.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L3.707 7.5H9.5a.5.5 0 0 1 .5.5"/>
                </svg></a>
              </button>
            </div>
            <div class="justify-content-center">
                <h3 class="h3 fw-bold text-center">Estado Fisico</h3>
            </div>
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
        <div>
            <div class="justify-content-center">
              <h4 class="h4 fw-bold text-center">Diagnostico</h4>
            </div>
            <div class="form-floating mb-3 col-lg-12">
              <textarea class="form-control" placeholder="Leave a comment here" id="diagnostico" style="height: 100px" resize="false"></textarea>
              <label for="diagnostico">Escriba aqui su diagnostico</label>
            </div>
            <div>
                <div class="row">
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
              </div>
              <div class="row">
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
              </div>
              <div class="row">
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
              </div>
              
              <div class="col-lg-12 mt-2">
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
              </div>
              </div>
        </div>
        <!-- Modal Asignar Rutina -->
        <div class="modal fade modal-lg" tabindex="-1" id="Asignar">
          <div class="modal-dialog  col-lg-10">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="text-center my-1 ms-4">Asignar Rutina</h1>
              </div>
              <div class="modal-body">
                <p class="my-2">Seleccione Rutina a asignar:</p>
              <table id="tablaRutinas">
                <thead>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Ejercicios</th>
                  <th>Accion</th>
                </thead>
                <tbody></tbody>
              </table>
              <div class="modal-footer d-flex justify-content-center">
                <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
              </div>
            </div>
          </div>
        </div>
        </div>
      <!--Modal para formar rutina y ver prediccion-->
        <div class="modal fade modal-xl" tabindex="-1" id="rutinaPersonalizada">
          <div class="modal-dialog  col-lg-10">
            <div class="modal-content">
              <div class="modal-header d-flex justify-content-between">
                <div>
                  <h1 class="text-center my-1 ms-4">Nueva rutina</h1>
                </div>
                <div>
                  <a  class="btn btn-success my-2">Recomendacion</a>
                  <!--onclick="FiltroPredic()"-->
                  <a  class="btn btn-secondary">Quitar Recomendacion</a>
                  <!--onclick="CargarEjercicios()"-->
                </div>
              </div>
              <div class="modal-body">
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
                                <div class="col-lg-6 col-md-6 ">
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
                                  <form >
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
                            </div>
                        </div>
                        </div>
              <div class="modal-footer d-flex justify-content-center">
                <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
              </div>
            </div>
          </div>
            </div>
      </div>
    </div>