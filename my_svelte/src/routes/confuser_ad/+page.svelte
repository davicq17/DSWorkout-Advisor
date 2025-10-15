<script lang="ts">
  import axios from "axios";
  import {onMount} from 'svelte';
  // almacen de datos
  let usuarios:any[] =$state([]);
  let userEdit:any = $state(null);
  let userEliminar:any = $state(null);

  onMount(()=>{
    Init_Data();
  });
  // pedir datos de la bd
  const Init_Data= async () =>{
    try{
      const response = await axios.get("http://127.0.0.1:5000/tableUser");
      usuarios= response.data.map((u:any)=>({
        ...u,
        // combertidor del rol en texto
        rolTxt:u.rol=== 1? "Administrador" : u.rol===2 ? "Usiario" : "Profesional",
      }));
      console.log("usuarios cargados:",usuarios);
    }catch(err){
      console.error("Error al cargar usuarios:",err);
    }
  };
  // actualizar usuarios
  const preEditar=(user:any)=>{userEdit={...user}}; 

  const Actualizar= async()=>{
    try{
      await axios.put(`http://127.0.0.1:5000/edituser/${userEdit.id}`,userEdit);
      alert("usuario actualizado correctamente");
      userEdit=null;
      await Init_Data();
    }catch(err){
      console.error("Error:",err);
    }
  };

  // Función para eliminar usuario
  const Eliminar= async ()=>{
    try{
      await axios.put(`http://127.0.0.1:5000/delete/${userEliminar.id}`);
      alert("Usuario eliminado correctamente");
      userEliminar = null;
      await Init_Data();
    }catch(err){
      console.error("Error al eliminar:",err);
    }
  };

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
      {#each usuarios as user }
        <tr>
          <td>{user.id}</td>
          <td>{user.username}</td>
          <td>{user.name}</td>
          <td>{user.surname}</td>
          <td>{user.email}</td>
          <td>{user.password}</td>
          <td>{user.cell}</td>
          <td>{user.rolTxt}</td>
          <td> 
            <button onclick={()=>preEditar(user)} class="btn btn-warning btn-sm ms-3" data-bs-toggle="modal"data-bs-target="#Editar"aria-label="Editar usuario">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
              <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
              </svg>
            </button>
            <button onclick={()=>userEliminar=user} class="btn btn-warning btn-sm ms-3" data-bs-toggle="modal"data-bs-target="#Editar"aria-label="Editar usuario">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
              <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
              </svg>
            </button>
          </td>
        </tr>
      {/each}
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
          <p class="text-start ms-4">¿Seguro que deseas eliminar al usuario <b>{userEliminar?.username}</b>? </p>
          </div><!--div2.2.2-->
          <div class="modal-footer d-flex justify-content-around"><!--div2.2.3-->
            <button onclick={Eliminar} class="btn btn-danger ms-5" data-bs-dismiss="modal" aria-label="eliminar usuario">Eliminar</button>
            <button class="btn btn-primary" data-bs-dismiss="modal">Cancelar</button>
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
          {#if userEdit}
            <div class="modal-body"><!--div7-->
              <div class="input-group"><!--div7.1-->
                <div class="col-md-6 pe-2 mb-3">
                  <input bind:value={userEdit.name} type="text" class="form-control pe-2" placeholder="Nombres">
                </div>
                <div class="col-md-6 mb-3">
                  <input bind:value={userEdit.surname} type="text" class="form-control"  placeholder="Apellidos">
                </div>
              </div><!--div7.1-->
              <div class="input-group"><!--div7.2-->
                <div class="col-md-6 pe-2 mb-3">
                  <input bind:value={userEdit.username} type="text" class="form-control pe-2"  placeholder="Usuario">
                </div>
                <div class="col-md-6 mb-3">
                  <input bind:value={userEdit.email} type="email" class="form-control"  placeholder="Correo">
                </div>
              </div><!--div7.2-->
              <div class="input-group"><!--div7.3-->
                <div class="col-md-6 mb-3 pe-2">
                  <input bind:value={userEdit.password} type="text" class="form-control pe-2" placeholder="Ingrese su contraseña" maxlength="12" minlength="6">
                </div>
                <div class="col-md-6 mb-3">
                  <input bind:value={userEdit.cell} type="number" class="form-control"  placeholder="Ingrese su contraseña" maxlength="10" minlength="10">
                </div>
              </div><!--div7.3-->
              <div class="col-6"><!--div7.4-->
                <select bind:value={userEdit.rol} class="form-select" >
                  <option value="1">Administrador</option>
                  <option value="2">Usuario</option>
                  <option value="3">Profesional</option>
                </select>
              </div><!--div7.4-->
            </div><!--div7-->
          {/if}
        <div class="modal-footer d-flex justify-content-around">
          <button onclick={Actualizar} class="btn btn-primary ms-5" data-bs-dismiss="modal" >Actualizar</button>
          <button class="btn btn-danger me-5 " data-bs-dismiss="modal">Cancelar</button>
        </div>
        </div><!--div5-->
      </div><!--div4-->
    </div><!--div3-->
</div><!--principal-->