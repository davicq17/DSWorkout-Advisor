<script>
  //const tabla=document.querySelector("#tablab tbody");

let tabla = new DataTable('#tablab', {
  paging:false,
  scrollY:400
});
const Init_Data=()=>{
    botones=`<a id="evaluar" class="btn btn-success"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard2-check-fill" viewBox="0 0 16 16">
  <path d="M10 .5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5.5.5 0 0 1-.5.5.5.5 0 0 0-.5.5V2a.5.5 0 0 0 .5.5h5A.5.5 0 0 0 11 2v-.5a.5.5 0 0 0-.5-.5.5.5 0 0 1-.5-.5"/>
  <path d="M4.085 1H3.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1h-.585q.084.236.085.5V2a1.5 1.5 0 0 1-1.5 1.5h-5A1.5 1.5 0 0 1 4 2v-.5q.001-.264.085-.5m6.769 6.854-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708.708"/>
</svg></a>`
    axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/TableFisic',
        
      }).then(function (response) {
       
        //console.log(response)
            for (let i = 0; i < response.data.length; i++) {
                    
              tabla.row.add([response.data[i].id, response.data[i].name, response.data[i].surname, response.data[i].age, response.data[i].gender, response.data[i].height, response.data[i].weight, response.data[i].Fr_Train,botones]).draw();
               
            } 
              
      }).catch(err => console.log('Error: ', err))

    }

Init_Data();
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
                <th scope="col">Fr de entrenamiento</th>
                <th scope="col">Accion</th>
            </tr>
            </thead>
            <tbody>
              
            </tbody>
          </table>
      </div>