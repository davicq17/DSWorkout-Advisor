<script lang="ts">
	import Navbar from '$lib/components/Navbar.svelte';
	import axios from 'axios';
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import { verifyToken } from '$lib/utils/AuthClient';

	Chart.register(...registerables);
	// variables para de datos generales
	let totalUsuarios = $state(0);
	let diagnosticosTotales = $state(0);
	let ejercicios = $state(0);
	let rutinas = $state(0);

	// variables de graficas
	let grafica1: HTMLCanvasElement;
	let grafica2: HTMLCanvasElement;
	let grafica3: HTMLCanvasElement;
	let grafica4: HTMLCanvasElement;
	let grafica5: HTMLCanvasElement;
	let grafica6: HTMLCanvasElement;

	onMount(async () => {
		// Verificar token antes de cargar datos
		await verifyToken();
		Init_Graficas();
	});

	// Funcion general
	const Init_Graficas = async () => {
		try {
			// peticion de datos generales
			const general = await axios.get('http://127.0.0.1:5000/GetGeneral');
			totalUsuarios = general.data.totalUsuarios;
			diagnosticosTotales = general.data.diagnosticosTotales;
			ejercicios = general.data.ejercicios;
			rutinas = general.data.rutinas;

			// Grafica 1 del IMC
			const g1 = await axios.get('http://127.0.0.1:5000/GetGrafica1');
			const counts = [0, 0, 0, 0];
			console.log('resuesta de grafica 1:', g1.data);
			let alturaM = 0;
			for (let p of g1.data) {
				alturaM = parseFloat(p.height) / 100;
				let IMC = parseFloat(p.weight) / (alturaM * alturaM);
				if (IMC <= 18.5) counts[0]++;
				else if (IMC > 18.5 && IMC <= 24.9) counts[1]++;
				else if (IMC <= 30 && IMC > 24.9) counts[2]++;
				else if (IMC > 30) counts[3]++;
			}
			new Chart(grafica1, {
				type: 'pie',
				data: {
					labels: ['Bajo peso', 'Peso normal', 'Sobrepeso', 'Obesidad'],
					datasets: [
						{
							label: 'IMC',
							data: counts,
							backgroundColor: [
								getRandomColor(0.3),
								getRandomColor(0.3),
								getRandomColor(0.3),
								getRandomColor(0.3)
							]
						}
					]
				}
			});

			// Grafica 2
			const g2 = await axios.get('http://127.0.0.1:5000/GetGrafica2');
			console.log(g2.data);
			new Chart(grafica2, {
				type: 'pie',
				data: {
					labels: ['Hombres', 'Mujeres'],
					datasets: [
						{
							label: 'Género',
							data: [g2.data[1].total, g2.data[0].total],
							backgroundColor: [getRandomColor(0.3), getRandomColor(0.3)]
						}
					]
				}
			});
			// Grafica 3
			const g3 = await axios.get('http://127.0.0.1:5000/GetGrafica3');
			new Chart(grafica3, {
				type: 'bar',
				data: {
					labels: g3.data.map((x: any) => x.goal),
					datasets: [
						{
							label: 'Objetivos',
							data: g3.data.map((x: any) => x.total),
							backgroundColor: getRandomColor(0.3)
						}
					]
				},
				options: { scales: { y: { beginAtZero: true } } }
			});

			//Gracfica 4
			const g4 = await axios.get('http://127.0.0.1:5000/GetGrafica4');
			const labels4: string[] = [];
			const datos4: number[] = [];
			for (const r of g4.data) {
				if (r.rol === 1) labels4.push('Administrador');
				else if (r.rol === 2) labels4.push('Usuario');
				else if (r.rol === 3) labels4.push('Profesional');
				datos4.push(r.total);
			}
			new Chart(grafica4, {
				type: 'bar',
				data: {
					labels: labels4,
					datasets: [
						{
							label: 'Roles',
							data: datos4,
							backgroundColor: getRandomColor(0.3)
						}
					]
				},
				options: { scales: { y: { beginAtZero: true } } }
			});

			// Grafica 5
			const g5 = await axios.get('http://127.0.0.1:5000/getGrafica5');
			const nombres5 = g5.data.map((i: any) => i[0]);
			const datos5 = g5.data.map((i: any) => i[1]);
			new Chart(grafica5, {
				type: 'bar',
				data: {
					labels: nombres5,
					datasets: [
						{
							label: 'Rangos de edad',
							data: datos5,
							backgroundColor: getRandomColor(0.3)
						}
					]
				},
				options: { scales: { y: { beginAtZero: true } } }
			});
		} catch (err) {
			console.error('Error al inicializar graficas:', err);
		}
	};

	// Grafica 6 - Commented out for now
	// 		const g6 = await axios.get('http://127.0.0.1:5000/getGrafica6');
	// 		console.log(g6.data);
	// 		for (i in g6.data) {
	// 			lab = g6.data[i];
	// 			labels.push(lab[0]);
	// 			datos.push(lab[1]);
	// 		}
	// 		new Chart(grafica6, {
	// 			type: 'bar',
	// 			data: {
	// 				labels: labels, // etiqueta de los rangos
	// 				datasets: [
	// 					{
	// 						label: 'Numero de personas por altura',
	// 						data: datos, // datos de la cantidad de personas en cada rango
	// 						backgroundColor: getRandomColor(0.2)
	// 					}
	// 				]
	// 			},
	// 			options: { scales: { y: { beginAtZero: true } } }
	// 		});

	// Genera los colores Ramdon
	function getRandomColor(opacidad: number) {
		const r = Math.floor(Math.random() * 256);
		const g = Math.floor(Math.random() * 256);
		const b = Math.floor(Math.random() * 256);
		return `rgba(${r},${g},${b},${opacidad})`;
	}

	// Descargar pdf
	const descargarPDF = async () => {
		try {
			const res = await fetch('http://127.0.0.1:5000/generarPDF');
			const blob = await res.blob();
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = 'Informe.pdf';
			a.click();
			a.remove();
		} catch (error) {
			console.error('Error al generar el PDF:', error);
		}
	};
</script>

<!--para está entrega-->
<Navbar />
<div class="col-lg-9 col-md-10 col-sm-12 container">
	<!--principal-->
	<div class="row">
		<!--div1-->
		<div class=" col-12 mt-3 rounded">
			<!--div1.1-->
			<div class="text-center">
				<h1 class="text-dark">Estadisticas</h1>
			</div>
			<button onclick={descargarPDF} class="btn btn-primary mb-1"
				><svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					fill="currentColor"
					class="bi bi-newspaper"
					viewBox="0 0 16 16"
				>
					<path
						d="M0 2.5A1.5 1.5 0 0 1 1.5 1h11A1.5 1.5 0 0 1 14 2.5v10.528c0 .3-.05.654-.238.972h.738a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 1 1 0v9a1.5 1.5 0 0 1-1.5 1.5H1.497A1.497 1.497 0 0 1 0 13.5zM12 14c.37 0 .654-.211.853-.441.092-.106.147-.279.147-.531V2.5a.5.5 0 0 0-.5-.5h-11a.5.5 0 0 0-.5.5v11c0 .278.223.5.497.5z"
					/>
					<path
						d="M2 3h10v2H2zm0 3h4v3H2zm0 4h4v1H2zm0 2h4v1H2zm5-6h2v1H7zm3 0h2v1h-2zM7 8h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2z"
					/>
				</svg> Informe
			</button>
		</div>
		<!--div1-->
	</div>
	<!--div1-->
	<div class="row">
		<!--div2-->
		<div class="col-12 d-flex justify-content-between">
			<h5 id="Activos" class="col-lg-4 col-md-6 border-primary my-4 me-4 rounded border p-1">
				Usuarios Activos: {totalUsuarios}
			</h5>
			<h5 id="DiagnosticosTt" class="col-lg-4 col-md-6 border-primary my-4 rounded border p-1">
				Diagnosticos realizados: {diagnosticosTotales}
			</h5>
		</div>
		<div class="col-12 d-flex justify-content-between">
			<h5 id="Ejercicios" class="col-lg-4 col-md-6 border-primary my-4 rounded border p-1">
				Ejercicios registrados: {ejercicios}
			</h5>
			<h5 id="Rutinas" class="col-lg-4 col-md-6 border-primary my-4 rounded border p-1">
				Rutinas creadas:{rutinas}
			</h5>
		</div>
	</div>
	<!--div2-->
	<div class="row mb-5 mt-5">
		<!--div3-->
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica1}></canvas></div>
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica2}></canvas></div>
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica3}></canvas></div>
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica4}></canvas></div>
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica5}></canvas></div>
		<div class="col-lg-4 col-md-6 col-sm-12"><canvas bind:this={grafica6}></canvas></div>
		<!-- <a onclick="GenerarReporte()" class="btn btn-primary">Generar reporte</a>-->
	</div>
	<!--div3-->
</div>
<!--principal-->
