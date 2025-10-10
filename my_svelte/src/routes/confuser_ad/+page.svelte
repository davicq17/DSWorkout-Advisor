<script>
  const Actualizar=()=>{
  idUpt=localStorage.getItem("idUpdate")
  nameI=document.getElementById('inputName').value;
  surnameI=document.getElementById('inputLastName').value;
  usernameI=document.getElementById('inputUsername').value;
  emailI=document.getElementById('inputEmail').value;
  passwordI=document.getElementById('inputPassword').value;
  cellI=document.getElementById('inputCell').value;
  rolI=document.getElementById('SelecRol').value;
  axios({
    method:'PUT',
    url:'http://127.0.0.1:5000/editUser/'+idUpt,
    data:{
      id:idUpt,
      username:usernameI,
      name:nameI,
      surname:surnameI,
      email:emailI,
      password:passwordI,
      cell:cellI,
      rol:rolI,
    }
  }).then(function(response){
    alert(response.data.informacion)

    document.getElementById("inputName").value = "";
    document.getElementById("inputLastName").value = "";
    document.getElementById("inputUsername").value = "";
    document.getElementById("inputEmail").value = "";
    document.getElementById("inputPassword").value = "";
    document.getElementById("inputCell").value = "";
    document.getElementById("SelecRol").value = 1;
    localStorage.removeItem("idUpdate");
    Init_Data()
  }).catch(err => console.log('Error: ', err))
}
</script>
<div class="container my-5"><!--principal-->
  <div class="col-12  d-flex justify-content-center"><!--div1-->
    <h1 class="h1">Información de Usuarios logueados</h1>
  </div><!--div1-->
  <table id="tablaa" class="table table-bordered table-striped table-hover table-responsive table-responsive-sm table-responsive-lg table-responsive-md table-responsive-xl">
    <thead class="table-dark">
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Usuario</th>
        <th scope="col">Nombre</th>
        <th scope="col">Apellidos</th>
        <th scope="col">Correo</th>
        <th scope="col">Contraseña</th>
        <th scope="col">Celular</th>
        <th scope="col">Rol</th>
        <th scope="col">Acciones</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
      <!--Modal para confirmar la eliminacion de un usuario--> 
  <div class="modal fade" tabindex="-1" id="Eliminar"><!--div2-->
    <div class="modal-dialog"><!--div2.1-->
        <div class="modal-content"><!--div2.2-->
          <div class="modal-header"><!--div2.2.1-->
            <h1 class="text-center my-3 ms-4">Eliminar Usuario</h1>
          </div><!--div2.2.1-->
          <div class="modal-body"><!--div2.2.2-->
          <p class="text-start ms-4">Seguro que deseas eliminar este usuario?</p>
          </div><!--div2.2.2-->
          <div class="modal-footer d-flex justify-content-around"><!--div2.2.3-->
            <a  class="btn btn-danger ms-5" data-bs-dismiss="modal" >Eliminar</a>
            <!--onclick="Eliminar()"-->
            <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
          </div><!--div2.2.3-->
        </div><!--div2.2-->
    </div><!--div2.1-->
  </div><!--div2-->
    <!--Modal para la edicion de datos del usuario-->
    <div class="modal fade" tabindex="-1" id="Editar" ><!--div3-->
      <div class="modal-dialog" ><!--div4-->
        <div class="modal-content"><!--div5-->
          <div class="modal-header"><!--div5.1-->
            <h1 class="text-center my-3">Editar un registro</h1>
          </div><!--div5.1-->
        <div class="modal-body"><!--div7-->
          <div class="input-group">
          <div class="col-md-6 pe-2 mb-3">
            <input type="text" class="form-control pe-2" id="inputName" placeholder="Nombres">
          </div>
          <div class="col-md-6 mb-3">
              <input type="text" class="form-control" id="inputLastName" placeholder="Apellidos">
          </div>
        </div>
        <div class="input-group">
          <div class="col-md-6 pe-2 mb-3">
              <input type="text" class="form-control pe-2" id="inputUsername" placeholder="Usuario">
          </div>
          <div class="col-md-6 mb-3">
              <input type="email" class="form-control" id="inputEmail" placeholder="Correo">
          </div>
        </div>
        <div class="input-group">
          <div class="col-md-6 mb-3 pe-2">
              <input type="text" class="form-control pe-2" id="inputPassword" placeholder="Ingrese su contraseña" maxlength="12" minlength="6">
          </div>
          <div class="col-md-6 mb-3">
              <input type="number" class="form-control" id="inputCell" placeholder="Ingrese su contraseña" maxlength="10" minlength="10">
          </div>
        </div>
        <div class="col-6">
          <select class="form-select"  id="SelecRol">
            <option value="1">Administrador</option>
            <option value="2">Usuario</option>
            <option value="3">Profesional</option>
        </select>
        </div>
        </div><!--div7-->
        <div class="modal-footer d-flex justify-content-around">
          <a class="btn btn-primary ms-5" data-bs-dismiss="modal" >Actualizar</a>
          <!--onclick="Actualizar()" -->
          <a class="btn btn-danger me-5 " data-bs-dismiss="modal">Cancelar</a>
        </div>
        </div><!--div5-->
      </div><!--div4-->
    </div><!--div3-->
</div><!--principal-->