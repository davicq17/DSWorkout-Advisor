<script lang="ts">
  let rol = $state(0);
	const increment = ()=>{if (rol < 3){rol++}};
	const decrement = ()=>{if (rol > 0){rol--}};
	function paths(rol: number) {
		switch(rol){
			case 0: 
      // navbar de los visitantes
				return [
					{name:'INICIO', url:"/"},
					{name:'COMO EMPEZAR', url:"/howstart"},
					{name:'INICIAR SESIÓN', url:"/login"}
				];
			case 1:
        //navbar de administrador
				return[
					{name:'ESTADISTICAS', url:"/estadisticas_ad"},
					{name:'USUARIOS', url:"/confuser_ad"},
					{name:'REGISTRAR', url:"/register_ad"}
					];
			case 2:
        // navbar de cliente o atleta
				return[
          {name:'INICIO', url:"/intuser_cli"},
					{name:'HISTORIAL', url:"/fisicestate_cli"},
					];	
			case 3:
        //navbar de profesional
				return[
					{name:'EJERCICIOS', url:"/crearejercicio_prof"},
					{name:'RUTINAS', url:"/crearrutina_prof"},
					{name:'ATLETAS', url:"/fisicuser_prof"}
				];
			default:
				return[]
		}	
	}
	const paginas = $derived(paths(rol));
</script>
<nav class="navbar navbar-expand-sm">
        <div class="container-fluid">
          <!--logo-->
          <img class="navbar-branad" src="/img/e-trainer.ico" alt="DS LOGO" widht="60px" height="60px">
            <!--boton para abrir el menu-->
          <button class="navbar-toggler " type="button" data-bs-toggle="collapse" data-bs-target="#menu-navbar" aria-controls="menu-navbar" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
            <!--menu-->
          <div class="collapse navbar-collapse justify-content-end" id="menu-navbar">
            <ul class="navbar-nav">
              {#each paginas as pagina }
                <li class="nav-item">
                  <a class="nav-link fw-bold" href={pagina.url}>{pagina.name}</a>
                </li>
              {/each}
            </ul>
          </div>
          <!--prueba del navbar reactivo, el rol lo debe tomar de una petición en la api
          por ahora se hace la prueba con los botones 
          0) visitante 1) admin 2) cliente 3) prof -->
          <h1>{rol}</h1>
          <button onclick={increment}>rol siguiente</button>
          <button onclick={decrement}>rol anterior</button>
        </div>
      </nav>