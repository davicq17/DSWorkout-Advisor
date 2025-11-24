<script lang="ts">
	import { onMount } from 'svelte';
	import { cerrarSesion, verifyToken } from '../utils/AuthClient';
	import type { UserData } from '../utils/AuthClient';

	let data: UserData | null = $state(null);

	onMount(async () => {
		if (window.location.pathname !== '/' && window.location.pathname !== '/login' && window.location.pathname !== '/registro' && window.location.pathname !== '/howstart') {
			data = await verifyToken();
		}
	});

	function paths() {
		const rol = data?.rol ?? 0;
		switch (rol) {
			case 0:
				// navbar de los visitantes
				return [
					{ name: 'INICIO', url: '/' },
					{ name: 'COMO EMPEZAR', url: '/howstart' },
					{ name: 'INICIAR SESIÓN', url: '/login' }
				];
			case 1:
				//navbar de administrador
				return [
					{ name: 'ESTADISTICAS', url: '/estadisticas_ad' },
					{ name: 'USUARIOS', url: '/confuser_ad' },
					{ name: 'REGISTRAR', url: '/register_ad' }
				];
			case 2:
				// navbar de cliente o atleta
				return [
					{ name: 'INICIO', url: '/intuser_cli' },
					{ name: 'HISTORIAL', url: '/fisicestate_cli' }
				];
			case 3:
				//navbar de profesional
				return [
					{ name: 'EJERCICIOS', url: '/crearejercicio_prof' },
					{ name: 'RUTINAS', url: '/crearrutina_prof' },
					{ name: 'ATLETAS', url: '/fisicuser_prof' }
				];
			default:
				return [];
		}
	}

	const paginas = $derived(paths());
</script>

<nav class="navbar navbar-expand-sm">
	<div class="container-fluid">
		<!--logo-->
		<img class="navbar-branad" src="/img/e-trainer.ico" alt="DS LOGO" width="60px" height="60px" />

		<h1 class="h5 text-decoration-none text-white">
			{#if data}
				Bienvenido(a) {data.name}
			{/if}
		</h1>

		<!--menu-->
		<div class="navbar-collapse justify-content-end collapse" id="menu-navbar">
			<ul class="navbar-nav">
				{#each paginas as pagina}
					<li class="nav-item">
						<a class="nav-link fw-bold" href={pagina.url}>{pagina.name}</a>
					</li>
				{/each}
				{#if data}
					<li class="nav-item">
						<button class="nav-link fw-bold" onclick={cerrarSesion}>CERRAR SESIÓN</button>
					</li>
				{/if}
			</ul>
		</div>
	</div>
</nav>