<script>
    const verificar = () => {
  if (
    document.getElementById("usertxt").value == "" ||
    document.getElementById("passwordtxt").value == "" // Verifica que no hayan campos vacios
  ) {
    alert("VERIFICAR CAMPOS VACIOS");
  } else {
    let IngUser = document.getElementById("usertxt").value; // recibe los datos en caso no esten vacios
    let IngPass = document.getElementById("passwordtxt").value;
    let IngRol = document.getElementById("rol").value;
    console.log(IngRol);
    let path =""
    if(IngRol=="1"){
      path="../html/admin.html"
    }else if(IngRol == "2"){
        path="../html/fit_intUser.html" 
    }else if(IngRol=="3"){
      path="../html/profesional.html"
    }
    Listbool = [true, true, true];
    let mens = "";
    if (IngPass.length >= 8) {
      Listbool[0] = true;
    } else {
      Listbool[0] = false;
      mens += "La contraseña debe tener minimo 8 caracteres";
    }

    def = true;
    for (i = 0; i < Listbool.length; i++) {
      def = Listbool[i] && def;
    }
    if (def) {
      axios({
        mehod: "GET",
        url: "http://127.0.0.1:5000/Login/" + IngUser,
      }).then(function (response) {
        if(response.data.length>0){
          if(response.data[0].status==1 && response.data[0].username == IngUser && response.data[0].password == IngPass &&response.data[0].rol == IngRol) {
                  localStorage.setItem("token",response.data[0].token);
                  window.location.href = path;
                  /*us={
                    id:response.data[0].id,
                    username: response.data[0].username,
                    name: response.data[0].name,
                    surname: response.data[0].surname,
                    rol:response.data[0].rol
                  }*/
                  

            }else{
              alert("Usuario y/o Contraseña erronea")
            }
          }else{
            alert("Usuario y/o Contraseña erronea")
          }
      }
      ).catch((err) => console.log("Error: ", err));
    } else {
      alert(mens);
    }
  }
};
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
                            <input type="text" class="form-control" placeholder="digite el usuario" id="usertxt"><br>
                            <label for="passwordtxt">CONTRASEÑA</label>
                            <input type="password" class="form-control" placeholder="ingrese la contraseña" id="passwordtxt">
                            <label for="rol">ROL</label>
                            <select  id="rol" class="form-control">
                                <option selected="true" value="0"></option>
                                <option value="3">Profesional</option>
                                <option value="2">Fit</option>
                                <option value="1">Administrador</option>
                            </select><br>
                            <button class="btn btn-primary">
                                <a  class="text-decoration-none text-white" href="#">INICIAR</a>
                                <!--onclick="verificar()"-->
                            </button>
                            <button class="btn btn-primary">
                                <a href="/registro" class="text-decoration-none text-white">REGISTRARSE</a>
                            </button>
                            <button class="btn btn-success">
                                <a href="/" class="text-decoration-none text-white ">VOLVER</a>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>