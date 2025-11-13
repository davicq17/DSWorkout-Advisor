<script lang="ts">
   import axios from "axios";
   // Recibimos la propiedad desde admin o usuario
   let {tipoRegistro}=$props<{tipoRegistro?:string}>();
   tipoRegistro??="usuario";// su valor por defecto es usuario
   let usernameI=$state("");
   let nameI = $state("");
   let surnameI =$state("");
   let emailI =$state("");
   let passwordI = $state("");
   let passwordConfirm = $state("");
   let CellI = $state("");
   let rolI= $state("");
   let especialidadI=$state("");
   let mensj="";
   // registro de usuario
   const Registrar = async ()=>{
    // evitar campos vacios
    if(
      usernameI.trim()==="" ||
      nameI.trim()===""||
      surnameI.trim()==="" ||
      emailI.trim()===""||
      passwordI.trim()===""||
      CellI==="" ||
      rolI==="0"
    ){ alert("VERIFICAR CAMPOS VACÍOS")
    return;
    }
    console.log(usernameI,nameI,surnameI,emailI,passwordI,CellI,rolI);
    // verificarción de los datos ingresados
    mensj="";
    var listbool=[false,false,false,false];
    console.log(listbool);
    //Nombre y apellido solo con letras
    listbool[0]=NombreLetras(nameI);
    listbool[1]=ApellidoLetras(surnameI);
    //email que contenga @ y .
    listbool[2]=EmailVerify(emailI);
    listbool[3]=PasswordVerify(passwordI,passwordConfirm);
    // todas las varificaciones deben ser TRUE para registrar
    let permite=listbool.every(i=>i);
    console.log("permite = " + permite);

    //verificar si existe el usuario ingresado
    try{
      //verificar si existe el usuario ingresado
      const response = await axios.get(`http://127.0.0.1:8000/Login/VerifyUser/${usernameI}`);
      const n = response.data["Existe"];
      console.log(n);
      let existe = n==1;
      // si el usuario no existe se procede con el registro
      if(existe==false){
        if(permite==true){
          await axios.post("http://127.0.0.1:8000/Usuarios/registro",{
                data:{
                  username: usernameI,
                  name: nameI,
                  surname: surnameI,
                  email: emailI,
                  password: passwordI,
                  cell: CellI,
                  rol: rolI,
                  status: 1,
                  especialidad: especialidadI,
              }
            }
          )
          .then(function(response){
            alert("registro exitoso");
            if(tipoRegistro ==="admin"){
                location.href="/confuser_ad";
            }else{
                location.href="/login";
            }
          }).catch((err)=> console.log("Error:", err));
        }else{
          // si alguna es false "permite sera false, y se enviara el mensaje"
          alert("mensaje"+mensj);
        }
      }else{
        alert("El usuario Ingreseado ya existe, por favor intenta con otro");
      }
    }catch(err:any){
      console.log("Error",err);
    };
   };
    // especialidad in/visible
    const Speciality=$derived(rolI==="3"? "block":"none");
    // rol admin
    const rolregist=$derived(tipoRegistro==="admin"?"block":"none");
    // funciones de verificación
    const NombreLetras = (nameI:string)=>{
      let salida=true;
      for (var i = 0; i < nameI.length; i++) {
      if (
          (nameI.charCodeAt(i) > 65 && nameI.charCodeAt(i) < 91) ||
          (nameI.charCodeAt(i) > 96 && nameI.charCodeAt(i) < 123)
        ) {
          salida = true;
        } else {
          salida = false;
          mensj += "El nombre no debe contener numeros o caracteres Especiales\n";
          break;
        }
      }
      return salida;
    };

    const ApellidoLetras=(surnameI:string)=>{
      let salida = true;
      for (var i = 0; i < surnameI.length; i++) {
        if (
          (surnameI.charCodeAt(i) > 65 && surnameI.charCodeAt(i) < 91) ||
          (surnameI.charCodeAt(i) > 96 && surnameI.charCodeAt(i) < 123)
        ) {
          salida = true;
        } else {
          salida = false;
          mensj += "El Apellido no debe contener numeros o caracteres Especiales\n";
          break;
        }
      }
      return salida;
    };

    const EmailVerify=(email:string)=>{
      let salida= true;
      if(email.includes("@") && email.includes(".")){
        salida=true;
      }else{
        salida=false;
        mensj+="Email erroneo, debe contener minimo @ y . \n";
      }
      return salida;
    };

    const PasswordVerify= (passwordI:string,passwordConfirm:string)=>{
      let tamaño = true;
      let verifypass = true;
      if (passwordI.length >= 8 && passwordI.length <= 12) {
        tamaño = true;
      } else {
        tamaño = false;
        mensj += "El tamaño de la contraseña debe ser de 8 a 12 caracteres \n ";
      }
      if (passwordI == passwordConfirm) {
        verifypass = true;
      } else {
        verifypass = false;
        mensj += "Las Contraseñas ingresadas no son iguales\n";
      }
      return tamaño && verifypass;
    };
</script>
<!--formulario de registro-->
    <div class="container col-lg-7 mt-5">
        <form class="row g-3">
            <div class="col-12 d-flex justify-content-center">
                <h1 class="h1 ">REGISTRO</h1>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={nameI} type="text" class="form-control" placeholder="Nombres">
                <label for="inputName" class="text-secondary" >Nombre</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={surnameI} type="text" class="form-control" placeholder="Apellidos">
                <label for="inputLastName" class="text-secondary">Apellido</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={usernameI} type="text" class="form-control"  placeholder="Usuario">
                <label for="inputUserName" class="text-secondary">Usuario</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={emailI} type="email" class="form-control" placeholder="Correo">
                <label for="inputEmail" class="text-secondary">Email</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={passwordI} type="password" class="form-control" placeholder="Ingrese su contraseña" minlength="8">
                <label for="inputPassword" class="text-secondary">Contraseña</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={passwordConfirm} type="password" class="form-control" placeholder="Ingrese su contraseña"  minlength="8">
                <label for="inputPassword2" class="text-secondary">Confirma la contraseña</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input bind:value={CellI} type="number" class="form-control" placeholder="Ingrese su contraseña" maxlength="10" minlength="6" >
                <label for="inputCell" class="text-secondary">Celular</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <select bind:value={rolI} class="form-select" name="role">
                    <option value="0" selected></option>
                    {#if tipoRegistro==="admin"}
                        <option value="1" style:display={rolregist}>Administrador</option>
                    {/if}
                    <option value="2">Usuario</option>
                    <option value="3">Profesional</option>
                </select>
                <label for="inputrol" class="text-secondary">Rol</label>
            </div>
            <!--div de la especialidad del profesional-->
            <div id="specialityField" class="col-md-6 form-floating mb-3 offset-md-6" style:display={Speciality};>
                <input type="text" class="form-control" id="inputSpeciality" placeholder="Especialidad del profesional">
                <label for="inputSpecialty" class="text-secondary">Especialidad</label>
            </div>
            <div class="col-12">
                <button onclick={Registrar} type="submit" class="btn btn-primary">
                 Crear
                </button>
                <button type="submit" class="btn btn-primary">
                    {#if tipoRegistro ==="admin" }
                         <a class="text-decoration-none text-white" href="/confuser_ad">Volver</a>
                    {:else }
                         <a class="text-decoration-none text-white" href="/login">Volver</a>
                    {/if}
                </button>
            </div>
        </form>
    </div>
