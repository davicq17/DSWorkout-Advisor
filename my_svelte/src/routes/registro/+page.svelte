<script>
    mensj = "";
const Registrar = () => {
  usernameI = document.getElementById("inputUserName").value;
  nameI = document.getElementById("inputName").value;
  surnameI = document.getElementById("inputLastName").value;
  emailI = document.getElementById("inputEmail").value;
  passwordI = document.getElementById("inputPassword").value;
  passwordConfirm = document.getElementById("inputPassword2").value;
  CellI = document.getElementById("inputCell").value;
  rolI= document.getElementById("inputrol").value;
  especialidadI="";
  if(rolI ==='3'){
    especialidadI=document.getElementById("inputSpeciality").value;
  }
  console.log(usernameI, nameI, surnameI, emailI, passwordI, CellI,rolI);
  //evitar campos vacios
  if (
    usernameI != "" ||
    nameI != "" ||
    surnameI != "" ||
    emailI != "" ||
    passwordI != "" ||
    CellI != "" ||
    rolI!="0"
  ) {
    //Verificaciones de los datos ingresados
    var listbool = [false, false, false, false];
    console.log(listbool);
    mensj = "";
    //Nombre y apellido solo con letras
    listbool[0] = NombreLetras(nameI);
    listbool[1] = ApellidoLetras(surnameI);
    //email que contenga @ y .
    listbool[2] = EmailVerify(emailI);
    listbool[3] = PasswordVerify(passwordI, passwordConfirm);
    //todas las verificaciones deben ser TRUE para registrar
    permite = true;
    for (var i = 0; i < 4; i++) {
      permite = permite && listbool[i];
    }
    console.log("permite = " + permite);

    //Verificar si existe el usuario ingresado
    axios({
      method: "GET",
      url: "http://127.0.0.1:5000/VerifyUser/" + usernameI,
    })
      .then(function (response) {
        n = response.data.length;
        console.log(n);
        existe = n != 0 ? true : false;
        //Si no existe procede con el registro
        if (existe == false) {
          if (permite == true) {
            axios({
              method: "POST",
              url: "http://127.0.0.1:5000/registro",
              data: {
                username: usernameI,
                name: nameI,
                surname: surnameI,
                email: emailI,
                password: passwordI,
                cell: CellI,
                rol: rolI,
                status: 1,
                especialidad: especialidadI,
              },
            })
              .then(function (response) {
                alert("Registro exitoso");
                location.href = "./Login.html";
              })
              .catch((err) => console.log("Error: ", err));
          } else {
            //si alguna es false "permite será false, y se enviara el mensaje"
            alert("Mensaje" + mensj);
          }
        } else {
          alert("El usuario Ingresado ya existe,Por favor intenta con otro");
        }
      })
      .catch((err) => console.log("Error: ", err));
  } else {
    alert("Verifique que no existan campos vacios!");
  }
};

const NombreLetras = (nameI) => {
  let salida = true;
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

const ApellidoLetras = (surnameI) => {
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
const EmailVerify = (emailI) => {
  let salida = true;
  if (emailI.includes("@") && emailI.includes(".")) {
    salida = true;
  } else {
    salida = false;
    mensj += "Email erroneo, debe contener minimo @ y . \n";
  }
  return salida;
};
const PasswordVerify = (passwordI, passwordVerify) => {
  tamaño = true;
  verifypass = true;
  if (passwordI.length >= 8 && passwordI.length <= 12) {
    tamaño = true;
  } else {
    tamaño = false;
    mensj += "El tamaño de la contraseña debe ser de 8 a 12 caracteres \n ";
  }
  if (passwordI == passwordVerify) {
    verifypass = true;
  } else {
    verifypass = false;
    mensj += "Las Contraseñas ingresadas no son iguales\n";
  }
  return tamaño && verifypass;
};

// especialidad de profesional
const Speciality = () => {
  var rolselect = document.getElementById("inputrol");
  var specialityField = document.getElementById("specialityField");
  if (rolselect.value === "3") {
    specialityField.style.display = "block";
  } else {
    specialityField.style.display = "none";
  }
};
</script>
<!--formulario de registro-->
    <div class="container col-lg-7 mt-5">
        <form class="row g-3">
            <div class="col-12 d-flex justify-content-center">
                <h1 class="h1 ">REGISTRO</h1>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="text" class="form-control" id="inputName" placeholder="Nombres">
                <label for="inputName" class="text-secondary" >Nombre</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="text" class="form-control" id="inputLastName" placeholder="Apellidos">
                <label for="inputLastName" class="text-secondary">Apellido</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="text" class="form-control" id="inputUserName" placeholder="Usuario">
                <label for="inputUserName" class="text-secondary">Usuario</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="email" class="form-control" id="inputEmail" placeholder="Correo">
                <label for="inputEmail" class="text-secondary">Email</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="password" class="form-control" id="inputPassword" placeholder="Ingrese su contraseña" minlength="8">
                <label for="inputPassword" class="text-secondary">Contraseña</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="password" class="form-control" id="inputPassword2" placeholder="Ingrese su contraseña"  minlength="8">
                <label for="inputPassword2" class="text-secondary">Confirma la contraseña</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <input type="number" class="form-control" id="inputCell" placeholder="Ingrese su contraseña" maxlength="10" minlength="6">
                <label for="inputCell" class="text-secondary">Celular</label>
            </div>
            <div class="col-md-6 form-floating mb-3">
                <select class="form-select" name="role" id="inputrol">
                    <!--onchange="Speciality()"-->
                    <option value="0" selected></option>
                    <option value="2">Usuario</option>
                    <option value="3">Profesional</option>
                </select>
                <label for="inputrol" class="text-secondary">Rol</label>
            </div>
            <!--div de la especialidad del profesional-->
            <div id="specialityField" class="col-md-6 form-floating mb-3 offset-md-6" style="display:none;">
                <input type="text" class="form-control" id="inputSpeciality" placeholder="Especialidad del profesional">
                <label for="inputSpecialty" class="text-secondary">Especialidad</label>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">
                    <a class="text-decoration-none text-white" >Crear</a>
                    <!--onclick="Registrar()"-->
                </button>
                <button type="submit" class="btn btn-primary">
                    <a class="text-decoration-none text-white" href="/login">Volver</a>
                </button>
            </div>
        </form>
    </div>