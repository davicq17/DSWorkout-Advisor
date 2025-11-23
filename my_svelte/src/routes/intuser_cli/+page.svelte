<script lang="ts">
	import DataTable from 'datatables.net-dt';
	import 'datatables.net-dt/css/dataTables.dataTables.css';
	import axios from 'axios';
	import { onMount } from 'svelte';
	import { cerrarSesion, getToken,verifyToken } from '$lib/utils/AuthClient';
	import { type UserData } from '$lib/utils/AuthClient';
	// variables reactivas
	let user: UserData | null = $state(null);
	let RutinaUser = $state('');
	let nameRutin = $state('');
	let nivelR = $state('');
	let descripR = $state('');
	let IdRutina = $state();
	// arreglo que rescibe los datos
	let dataA: any[] = $state([]);
	const GetRutina = async () => {
		try {
			let response = await verifyToken();
			user = response?.user;
			const respon = await axios.get(
				`http://127.0.0.1:8000/Diagnosticos/GetDiagnostico/${user?.id}`
			);

			if (respon.data.informacion == null) {
				RutinaUser = respon.data.diagnostico;
				nameRutin = respon.data.nombreR;
				nivelR = respon.data.nivelR;
				descripR = respon.data.descripcion;
				IdRutina = respon.data.idR;

				const res = await axios.get(`http://127.0.0.1:8000/EjerciciosUser/${IdRutina}`);
				let ejercicios = res.data;
				// se limpia el arreglo antes de mapear para evitar duplicados
				dataA = [];
				for (let i = 0; i < res.data.length; i++) {
					dataA.push([
						ejercicios[i].id,
						ejercicios[i].nombre,
						ejercicios[i].duracion,
						ejercicios[i].repeticiones,
						ejercicios[i].series
					]);
				}

				setTimeout(() => {
					new DataTable('#tablaRtUser', {
						columnDefs: [{ target: 0, visible: false }],
						paging: false,
						searching: false,
						scrollY: '300px',
						data: dataA
					});
				}, 0);
			} else {
				//VERIFICAR SI EL USUARIO YA HA REALIZADO EL FORMULARIO DE ESTADO FISICO
				const res = await axios.get(`http://127.0.0.1:8000/Diagnosticos/GetFisicState/${user?.id}`);
				if (!res.data) {
					alert('Debes realizar el formulario de estado fisico para recibir un diagnostico');
					cerrarSesion();
				} else {
					RutinaUser = 'Aun no se te ha asignado una rutina';
					alert(
						'Ya realizaste el formulario de estado fisico, espera a que un instructor te asigne una rutina'
					);
					cerrarSesion();
				}
			}
		} catch (err) {
			console.log('Error: ', err);
		}
	};
	// carga la funcón antes de que se carge la pagina
	onMount(() => {
		GetRutina();
		verifyToken();
	});
</script>

<!--contenedor de todo-->
<div class="container">
	<div class="row my-4">
		<div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">
			<div id="Rutina" class="card mb-5">
				<h4 class="card-header">Diagnostico</h4>
				<div class="card-body">
					<div id="RutinaUser" class="border-info mx-1 my-4 rounded border p-1">
						<!--DIAGNOSTICO-->
						{#if RutinaUser}
							{RutinaUser}
						{/if}
					</div>
					<!--NOTA-->
					<!--<div class="form-floating">
                            <textarea id="txtnota" class="form-control"></textarea>
                            <label for="txtnota">Queja u opinion:</label>
                        </div>-->
				</div>
			</div>
		</div>
		<div class="col-lg-7 col-md-7 col-sm-12 col-xs-12">
			<div class="card">
				<div class="card-header bg-success">
					<div class="row">
						<div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
							<!--nombre de la rutina-->
							<h4 id="nombrerutina" class="text-center text-white">{nameRutin}</h4>
						</div>
						<div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
							<!--nivel de la rutina-->
							<h4 id="nivelR" class="text-center text-white">Nivel: {nivelR}</h4>
						</div>
					</div>
				</div>
				<div class="card-body">
					<div class="mb-2">
						<label for="descripR" class="form-label"><b>Descripción</b></label>
						<!--descripción de la rutina-->
						<textarea readonly id="descripR" class="form-control"> {descripR}</textarea>
					</div>
					<div class="table-responsive">
						<table id="tablaRtUser" class=" table-striped table" style="width:100%">
							<thead>
								<tr>
									<th>id</th>
									<th><b>Ejercicios</b> </th>
									<th><b>Duración</b></th>
									<th><b>Series</b></th>
									<th><b>Repeticiones</b></th>
								</tr>
							</thead>
							<tbody> </tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
