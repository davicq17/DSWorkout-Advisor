<script lang="ts">
	import Navbar from '$lib/components/Navbar.svelte';
	import { onMount } from 'svelte';
	import { verifyToken } from '$lib/utils/AuthClient';
	onMount(async () => {
		// await verifyToken();
	});
</script>

<!--para está entrega-->
<Navbar />
<div class="col-lg-9 col-md-10 col-sm-12 container">
	<!--principal-->
	<iframe
		title="Usuarios"
		width="1140"
		height="541.25"
		src="https://app.powerbi.com/reportEmbed?reportId=027caf89-43e5-48bc-b79f-8a1c360a48b1&autoAuth=true&ctid=1e9aabe8-67f8-4f1c-a329-a754e92499ae"
		frameborder="0"
	></iframe>
</div>
<!--principal-->
