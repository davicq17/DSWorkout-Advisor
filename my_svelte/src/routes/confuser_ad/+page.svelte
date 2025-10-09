<div class="container my-5">
        <div class="col-12  d-flex justify-content-center">
            <h1 class="h1">Información de Usuarios logueados</h1>
        </div>
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
    <div class="modal fade" tabindex="-1" id="Eliminar">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="text-center my-3 ms-4">Eliminar Usuario</h1>
          </div>
          <div class="modal-body">
          <p class="text-start ms-4">Seguro que deseas eliminar este usuario?</p>
          </div>
          <div class="modal-footer d-flex justify-content-around">
            <a  class="btn btn-danger ms-5" data-bs-dismiss="modal" >Eliminar</a>
            <!--onclick="Eliminar()"-->
            <a class="btn btn-primary me-5 " data-bs-dismiss="modal">Cancelar</a>
          </div>
        </div>
      </div>
    </div>
    <!--Modal para la edicion de datos del usuario-->
    <div class="modal fade" tabindex="-1" id="Editar" >
      <div class="modal-dialog" >
        <div class="modal-content">
        <div class="modal-header">
        <h1 class="text-center my-3">Editar un registro</h1>
      </div>
      <div class="modal-body">
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
      </div>
        <div class="modal-footer d-flex justify-content-around">
          <a class="btn btn-primary ms-5" data-bs-dismiss="modal" >Actualizar</a>
          <!--onclick="Actualizar()" -->
          <a class="btn btn-danger me-5 " data-bs-dismiss="modal">Cancelar</a>
        </div>

      </div>
    </div>
    </div>


      </div>