<script>
   import axios from "axios";
    // variables
    let IngUser ="";
    let IngPass ="";
    let IngRol="";
    const verificar = async ()=>{
      // validación de campos vacios
      if(IngUser.trim() ==="" || IngPass.trim()=== ""){
        alert("VERIFICAR CAMPOS VACÍOS")
        return;
      }
      // ruta segun el rol
      console.log(IngRol);
      let path="";
      if(IngRol==="1"){
        path="/confuser_ad";
      } else if(IngRol==="2"){
        path="/intuser_cli";
      }else if(IngRol==="3"){
        path="/fisicuser_prof"
      }
      //validacion de contraseña
     let ListBool =[true,true,true];
      let mens="";
      if(IngPass.length < 8){
         ListBool[0]=false;
         mens+="La contraseña debe tener mínimo 8 caracteres";
      }

      // verifica todas las validaciones
      const todoOk =ListBool.every(v=>v===true);

      if(!todoOk){
        alert(mens)
        return;
      }

      // si pasa las validaciones, se realiza la petición 
      try{
        const response= await axios.get(`htttp://127.0.0.1:5000/Login/${IngUser}`);
        const data= response.data;

        if(data.length >0){
          const user = data[0];
          if(
            user.status == 1 &&
            user.username === IngUser &&
            user.password === IngPass &&
            user.rol == IngRol
          ){
            localStorage.setItem("token", user.token);
            localStorage.setItem("rol",user.rol);
           window.location.href = path;
          }else {
            alert("Usuario y/o Contraseña errónea");
          }
        }else {
          alert("Usuario y/o Contraseña errónea");
        }
      }catch(err){
        console.error("Error", err);
        alert("Ocurrio un erro al iniciar sesión");
      }
    }
</script>
<!--inicio de sesion-->
    <div class="container ">
        <div class="card  mx-auto mt-5" style="max-width:50rem;">
            <div class="card-header text-white ">
                <center class="fw-bold">INICIAR SESION</center>
            </div>
            <div class="card-body text-dark">
                <div class="card-text">
                    <div class="row">
                        <div class="col-xl6 col-lg-6 col-md-6 col-sm12 col-12 d-flex justify-content-center">
                            <img src="../img/e-trainer.ico" alt="icono">
                        </div>
                        <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12 col-12">
                            <br>
                            <label for="usertxt">USUARIO</label>
                            <input type="text" class="form-control" placeholder="digite el usuario" bind:value={IngUser}><br>
                            <label for="passwordtxt">CONTRASEÑA</label>
                            <input type="password" class="form-control" placeholder="ingrese la contraseña" bind:value={IngPass}>
                            <label for="rol">ROL</label>
                            <select  bind:value={IngRol} class="form-control">
                                <option selected value="0"></option>
                                <option value="3">Profesional</option>
                                <option value="2">Fit</option>
                                <option value="1">Administrador</option>
                            </select><br>
                             
                            <button class="btn btn-primary"  onclick={verificar}>
                                INICIAR
                            </button>
                             <!--
                              <a class="btn btn-primary" href="/confuser_ad"> INICIAR</a>
                             -->
                            <a href="/registro" class=" btn btn-primary text-decoration-none text-white">REGISTRARSE</a>
                            
                            <a href="/" class="btn btn-success text-decoration-none text-white ">VOLVER</a>
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>