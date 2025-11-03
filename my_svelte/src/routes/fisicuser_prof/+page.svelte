<script lang="ts">
  import { onMount } from "svelte";
  import DataTable from "datatables.net-dt";
  import "datatables.net-dt/css/jquery.dataTables.css";
	import axios from "axios";

  let tabla:any;
  let usuarios:any[]= [];

  // preparación para evaluar al usuario
  const evaluarUsuario= async(id:number)=>{
    try{
      const response = await axios.get(`http://127.0.0.1:5000/FisicById/${id}`);
      const datos = response.data;
      // se guardan los datos del usuario en el localstorage
      localStorage.setItem("datos",JSON.stringify(datos));
      // manda al componente de evaluar
      window.location.href="/evaluar_prof";
    }catch(err){
      console.error("Error :",err);
    }
  }

  const Init_Data= async ()=>{
    try{
      const response = await axios.get("http://127.0.0.1:5000/TableFisic");
      //console.log(response)
       usuarios=response.data;
    }catch(err){
      console.log('Error: ',err);
    }
  }

  // carga la funcion antes de que cargue el DOM
  onMount(async()=>{
     await Init_Data();  
  })

  $effect(()=>{
    if(usuarios.length > 0 && !tabla){
      // creamos la tabla
      tabla= new DataTable("#tablab",{
        data: usuarios.map(u =>[
          u.id,
          u.name,
          u.surname,
          u.age,
          u.gender,
          u.height,
          u.weight,
          u.Fr_train,
          // boton 
          `<button aria-label="evaluar" class="btn btn-success evaluar-btn" data-id="${u.id}">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"class="bi bi-clipboard2-check-fill" viewBox="0 0 16 16">
                  <path d="M10 .5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5.5.5 0 0 1-.5.5.5.5 0 0 0-.5.5V2a.5.5 0 0 0 .5.5h5A.5.5 0 0 0 11 2v-.5a.5.5 0 0 1-.5-.5.5.5 0 0 0-.5-.5"/>
                  <path d="M4.085 1H3.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1h-.585q.084.236.085.5V2a1.5 1.5 0 0 1-1.5 1.5h-5A1.5 1.5 0 0 1 4 2v-.5q.001-.264.085-.5m6.769 6.854-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708.708"/>
                </svg>
            </button>`
        ]),
        paging:false,
        scrollY:"400px"
      })
      // escuhcamos los click del boton editar
      document.querySelector("#tablab")?.addEventListener("click",(e)=>{
        const target = e.target as HTMLElement;
        const btn =target.closest(".evaluar-btn") as HTMLButtonElement;
        if(btn){
          const id = btn.dataset.id;
          if(id) evaluarUsuario(Number(id));
        }
      })
    }
  })
  
</script>
<!--contenedor de todo-->
      <div class="container col-md-11 col-sm-11 my-5">
        <div>
          <h1 class="text-center mb-3">Estado fisico de Usuarios</h1>
        </div>
        <table id="tablab" class="table text-center table-bordered table-striped table-hover table-responsive table-responsive-sm table-responsive-lg table-responsive-md table-responsive-xl" data-page-length='10'>
            <thead class="table-dark">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Nombre</th>
                <th scope="col">Apellido</th>
                <th scope="col">Edad</th>
                <th scope="col">Genero</th>
                <th scope="col">Estatura</th>
                <th scope="col">Peso</th>
                <th scope="col">Frecuencia</th>
                <th scope="col">Accion</th>
            </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
      </div>