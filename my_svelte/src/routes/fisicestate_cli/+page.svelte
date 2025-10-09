 <!--contenedor de todo-->
    <div class="container col-lg-7 col-sm-10  my-5">
      <div class="justify-content-center">
        <h3 class="mb-5 h3 fw-bold text-center">Estado Fisico</h3>
      </div>
        <form class="row g-3">
              <div class=" input-group">
              <div class="col-sm-12 col-md-6 ">
                <input type="number" class="form-control" id="inputage" placeholder="Edad">
              </div>
              
              <div class="form-check form-check-inline ps-5">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="M" value="M" checked>
                <label class="form-check-label" for="M">M</label>
              </div>
              <div class="form-check form-check-inline ps-5">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="F" value="F">
                <label class="form-check-label" for="F">F</label>
              </div>
            </div>
            <div class="col-md-6">
              <input type="number" class="form-control" id="inputpeso" placeholder="Peso(kg)">
            </div>
            <div class="col-sm-12 col-md-6">
              <input type="number" class="form-control" id="inputAltura" placeholder="Altura(m)">
            </div>
            <div class="col-md-12">
              <label for="inputfr_train" class="form-label">¿Con que fecuencia realiza actividad fisica?</label>
              <select id="inputfr_train" class="form-select">
                <option value="Nunca" selected>Nunca</option>
                <option value="ocacional">Ocasional (1-2 veces a la semana)</option>
                <option value="Regular">Regular(3-4 veces a la semana)</option>
                <option value="Frecuentemente">Frecuentemente(5 o mas veces a la semana)</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputDuration_sesion">¿Cúanto dura su sesión de ejercicio tipica?</label>
              <select id="inputDuration_sesion" class="form-select">
                <option value="0" selected>0</option>
                <option value="1-2h">1-2 horas</option>
                <option value="3-4h">3-4 horas</option>
                <option value="5h+">5 o mas horas</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputObjetivo" class="form-label">Objetivo</label>
              <select  id="inputObjetivo" class="form-select">
                <option value="" selected></option>
                <option value="Mantener salud" >Mantener salud</option>
                <option value="Perder peso">Perder peso</option>
                <option value="Ganar musculo">Ganar musculo</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputEquipamiento">¿Con qué equipamiento u herramienta cuenta, que lo ayude a ejercitarce?</label>
              <textarea  id="inputEquipamiento" class="form-control" placeholder="escriba su equipamiento o si asiste a un gimnasio"></textarea>
            </div>
            <div class="col-md-12">
              <label for="inputRestricción_alimenticia" class="form-label">Restricciones alimenticias</label>
              <input type="text" class="form-control" id="inputRestricción_alimenticia">
            </div>
            <div class=" col-6 mt-3 d-flex container" >
              
            <div class="col-3 me-5">
              <a  class="btn btn-primary" >Enviar</a>
              <!--onclick="RegistroFisicState()"-->
            </div>
            <div class="col-3">
              <a type="submit" class="btn btn-danger">cancelar</a>
            </div>
          </div>
        </form>
    </div>