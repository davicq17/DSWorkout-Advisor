<script lang="ts">
  const {data}=$props(); // el rol y el token vienen del servidor
  let {rol,token}=data;
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

	const cerranSesion =()=>{
		localStorage.removeItem("token");
		localStorage.removeItem("rol");
		window.location.href="/";
	};
</script>
<nav class="navbar navbar-expand-sm">
  <div class="container-fluid">
    <!--logo-->
          <img class="navbar-branad" src="/img/e-trainer.ico" alt="DS LOGO" widht="60px" height="60px">
			<h1 class="h5 text-decoration-none text-white">
			{#if data.user}
				Bienvenido(a) {data.user.name} 
			{/if}
		  	</h1>
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
				{#if token}
					<li class="nav-item">
				  		<button class="nav-link fw-bold" onclick={cerranSesion}>CERRAR SESIÓN</button>
                	</li>
			  	{/if}
            </ul>
          </div>
  </div>
</nav>