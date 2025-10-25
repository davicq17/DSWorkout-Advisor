 <script lang="ts">
  import axios from "axios";

  // variables reactivas 
  const {token}=$props(); // el rol y el token vienen del servidor
  let ageI:any= $state(0);
  let genderI=$state("");
  let weightI:any= $state(0);
  let heightI:any= $state(0); 
  let Fr_trainI=$state("");
  let durationI=$state("");
  let goalI=$state("");
  let equipment=$state("");
  let restrictionsI=$state("");
  // arreglo reactivo para resivr usuarios 
  let user:any =$state(null);
  // estado de carga 
  let isLoading =$state(false);
  const RegistroFisicState= async ()=>{
    if(!ageI || !weightI || !heightI || !Fr_trainI || !goalI ){
        return alert("VERIFICAR CAMPOS VACÍOS");
      }
      isLoading=true;
      try{
        const response = await axios.get(`http://127.0.0.1:5000/verify_token/${token}`)
          user =response.data;

          const res = await axios.post("http://127.0.0.1:5000/regisFisicState",{
            id:user.id,
            age:ageI,
            gender:genderI,
            height:heightI,
            weight:weightI,
            Fr_train:Fr_trainI,
            duration:durationI,
            goal:goalI,
            equipment:equipment,
            restrictions:restrictionsI
          })
            alert(res.data.informacion)
            window.location.href="/fisicestate_cli"
      }catch(err){
        console.log("Error: ", err);
      }finally{
        isLoading=false;
      }
    }
 </script>
 <!--contenedor de todo-->
    <div class="container col-lg-7 col-sm-10  my-5">
      <div class="justify-content-center">
        <h3 class="mb-5 h3 fw-bold text-center">Estado Fisico</h3>
      </div>
        <form class="row g-3">
                <div class="col-sm-12 col-md-6 ">
                 <input bind:value={ageI} type="number" class="form-control" placeholder="Edad">
                </div>
                <div class="col-sm-12 col-md-6">
                  <select bind:value={genderI} class="form-select">
                    <option selected>Genero</option>
                    <option value="M">Masculino</option>
                    <option value="F">Femenino</option>
                  </select>
                </div>
  
            <div class="col-md-6">
              <input bind:value={weightI} type="number" class="form-control" placeholder="Peso(kg)">
            </div>
            <div class="col-sm-12 col-md-6">
              <input bind:value={heightI} type="number" class="form-control" placeholder="Altura(m)">
            </div>
            <div class="col-md-12">
              <label for="inputfr_train" class="form-label">¿Con que fecuencia realiza actividad fisica?</label>
              <select bind:value={Fr_trainI} id="inputfr_train" class="form-select">
                <option value="Nunca" selected>Nunca</option>
                <option value="ocacional">Ocasional (1-2 veces a la semana)</option>
                <option value="Regular">Regular(3-4 veces a la semana)</option>
                <option value="Frecuentemente">Frecuentemente(5 o mas veces a la semana)</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputDuration_sesion">¿Cúanto dura su sesión de ejercicio tipica?</label>
              <select bind:value={durationI} id="inputDuration_sesion" class="form-select">
                <option value="0" selected>0</option>
                <option value="1-2h">1-2 horas</option>
                <option value="3-4h">3-4 horas</option>
                <option value="5h+">5 o mas horas</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputObjetivo" class="form-label">Objetivo</label>
              <select bind:value={goalI}  id="inputObjetivo" class="form-select">
                <option value="" selected></option>
                <option value="Mantener salud" >Mantener salud</option>
                <option value="Perder peso">Perder peso</option>
                <option value="Ganar musculo">Ganar musculo</option>
              </select>
            </div>
            <div class="col-md-12">
              <label for="inputEquipamiento">¿Con qué equipamiento u herramienta cuenta, que lo ayude a ejercitarce?</label>
              <textarea bind:value={equipment} id="inputEquipamiento" class="form-control" placeholder="escriba su equipamiento o si asiste a un gimnasio"></textarea>
            </div>
            <div class="col-md-12">
              <label for="inputRestricción_alimenticia" class="form-label">Restricciones alimenticias</label>
              <input bind:value={restrictionsI} type="text" class="form-control" id="inputRestricción_alimenticia">
            </div>
            <div class=" col-6 mt-3 d-flex container" >
              
            <div class="col-3 me-5">
              <button onclick={RegistroFisicState} class="btn btn-primary" 
              disabled={isLoading}>{isLoading? "Enviando...":"Enviar"}</button>
            </div>
            <div class="col-3">
              <a  class="btn btn-danger" href="/intuser_cli">cancelar</a>
            </div>
          </div>
        </form>
    </div>