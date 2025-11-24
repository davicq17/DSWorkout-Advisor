<script lang="ts">
	//import '../app.css';
	//import favicon from '$lib/assets/favicon.svg';
	//se importan el menu o navbar y el pie de pagina para todas las paginas
	//import Navbar from "$lib/components/Navbar.svelte";
	import Footer from "$lib/components/Footer.svelte";
	let { children,data } = $props();  // traemos la data de +layout.server.ts
</script>


{@render children?.()}
<Footer/>