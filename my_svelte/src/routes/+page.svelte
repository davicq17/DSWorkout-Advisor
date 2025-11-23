<script>
	import Navbar from '$lib/components/Navbar.svelte';
</script>

<!--para esta entrega-->
<Navbar/>
<!-- Contenido principal -->
<div class="d-flex-column container">
	<div class="justify-content-center p-2">
		<div class="row">
			<h4 class="h4">DS Workout Advisor</h4>

			<div class="col-12 col-md-6 text-justify">
				<p>
					Es una herramienta Web que lo ayudará en la asesoría de sus ejercicios, con ayuda de un
					asesor virtual llamado E-Trainer, el cual de acuerdo a su estado físico y objetivos
					propuestos podrá sugerir una rutina de ejercicio y un plan de alimentación para
					complementar y potenciar la actividad física, además cuenta con una guía de ejecución para
					cada ejercicio en caso de que se desconozca la forma correcta de realizarlo.
				</p>
				<p>
					Tenemos un amplio repertorio de ejercicios para asegurarnos de que cualquier tipo de
					persona pueda mejorar su estado físico de manera segura. Cada una de nuestras rutinas es
					verificada y aprobada por un instructor real, al igual que los planes de alimentación.
				</p>
			</div>

			<div class="col-12 col-md-6 d-flex justify-content-center">
				<img src="/img/ejemplo e-trainer.jpg" alt="E-Trainer" width="352" height="352" />
			</div>

			<h4 class="h4 mt-4">Ventajas</h4>
			<ul class="list-group col-12 col-lg-8 col-md-8">
				<li class="list-group-item d-flex justify-content-between align-items-center">
					Rutinas personalizadas
					<span class="badge text-bg-primary rounded-pill">1</span>
				</li>
				<li class="list-group-item d-flex justify-content-between align-items-center">
					Alimentación personalizada
					<span class="badge text-bg-primary rounded-pill">2</span>
				</li>
				<li class="list-group-item d-flex justify-content-between align-items-center">
					Asesoría de ejercicios
					<span class="badge text-bg-primary rounded-pill">3</span>
				</li>
				<li class="list-group-item d-flex justify-content-between align-items-center">
					Gestión del tiempo según disponibilidad
					<span class="badge text-bg-primary rounded-pill">4</span>
				</li>
				<li class="list-group-item d-flex justify-content-between align-items-center">
					Seguimiento del progreso
					<span class="badge text-bg-primary rounded-pill">5</span>
				</li>
			</ul>
		</div>
	</div>

	<!-- Mapa -->
	<div class="p-2 text-center">
		<h4>Nuestra oficina se encuentra en:</h4>
		<iframe
			src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d3916.6978586123314!2d-74.78630025991058!3d10.986163050876328!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8ef42d6495db4481%3A0xda626b57e9840495!2sInstituci%C3%B3n%20Universitaria%20de%20Barranquilla%20IUB!5e0!3m2!1ses!2sco!4v1718175030608!5m2!1ses!2sco"
			width="400"
			height="400"
			style="border:0;"
			loading="lazy"
			referrerpolicy="no-referrer-when-downgrade"
			title="Mapa de ubicación de la oficina - Institución Universitaria de Barranquilla IUB"
		></iframe>
	</div>
</div>
