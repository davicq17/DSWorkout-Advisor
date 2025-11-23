<script lang="ts">
	import { onMount } from 'svelte';
	import axios from 'axios';

	// variables reactivas
	let ageI: any = $state(0);
	let genderI = $state('');
	let weightI: any = $state(0);
	let heightI: any = $state(0);
	let Fr_trainI = $state('');
	let goalI = $state('');
	let restrictionsI = $state('');
	// arreglo reactivo para resivr usuarios
	let user: any = $state(null);
	// estado de carga
	let isLoading = $state(false);
	let token: string = $state('');

	onMount(() => {
		token = localStorage.getItem('token') || '';
	});
	const RegistroFisicState = async () => {
		if (
			!ageI ||
			ageI < 0 ||
			genderI === '0' ||
			!weightI ||
			weightI < 0 ||
			!heightI ||
			heightI < 0 ||
			!Fr_trainI ||
			!goalI ||
			!restrictionsI
		) {
			return alert('VERIFICAR CAMPOS VACIOS');
		}
		isLoading = true;
		try {
			const response = await axios.get(`http://127.0.0.1:8000/Login/verify_token/${token}`);
			user = response.data;
			if (response.data.rol !== 2) {
				alert('No tienes permiso para acceder a esta página');
				window.location.href = '/';
			}

			console.log(user);
			const res = await axios.post('http://127.0.0.1:8000/Diagnosticos/regisFisicState', {
				id: user.id,
				age: ageI,
				gender: genderI,
				height: heightI,
				weight: weightI,
				fr_train: Fr_trainI,
				goal: goalI,
				restrictions: restrictionsI
			});
			alert(res.data.informacion);
			window.location.href = '/fisicestate_cli';
		} catch (err) {
			console.log('Error: ', err);
		} finally {
			isLoading = false;
		}
	};
</script>

<!--contenedor de todo-->
<div class="col-lg-7 col-sm-10 container my-5">
	<div class="justify-content-center">
		<h3 class="h3 fw-bold mb-5 text-center">Estado Fisico</h3>
	</div>
	<form class="row g-3">
		<div class="col-sm-12 col-md-6">
			<label for="inputAge" class="form-label">Edad</label>
			<input
				bind:value={ageI}
				type="number"
				class="form-control"
				id="inputAge"
				placeholder="Edad"
			/>
		</div>
		<div class="col-sm-12 col-md-6">
			<label for="inputGender" class="form-label">Género</label>
			<select bind:value={genderI} class="form-select" id="inputGender">
				<option value="0" selected></option>
				<option value="M">Masculino</option>
				<option value="F">Femenino</option>
			</select>
		</div>

		<div class="col-md-6">
			<label for="inputWeight" class="form-label">Peso (kg)</label>
			<input
				bind:value={weightI}
				type="number"
				class="form-control"
				id="inputWeight"
				placeholder="Peso(kg)"
			/>
		</div>
		<div class="col-sm-12 col-md-6">
			<label for="inputHeight" class="form-label">Altura (m)</label>
			<input
				bind:value={heightI}
				type="number"
				class="form-control"
				id="inputHeight"
				placeholder="Altura(m)"
			/>
		</div>
		<div class="col-md-12">
			<label for="inputfr_train" class="form-label"
				>¿Con que fecuencia realiza actividad fisica?</label
			>
			<select bind:value={Fr_trainI} id="inputfr_train" class="form-select">
				<option value="Nunca" selected>Nunca</option>
				<option value="ocacional">Ocasional (1-2 veces a la semana)</option>
				<option value="Regular">Regular(3-4 veces a la semana)</option>
				<option value="Frecuentemente">Frecuentemente(5 o mas veces a la semana)</option>
			</select>
		</div>
		<div class="col-md-12">
			<label for="inputObjetivo" class="form-label">Objetivo</label>
			<select bind:value={goalI} id="inputObjetivo" class="form-select">
				<option value="" selected></option>
				<option value="Mantener salud">Mantener salud</option>
				<option value="Perder peso">Perder peso</option>
				<option value="Ganar musculo">Ganar musculo</option>
			</select>
		</div>
		<div class="col-md-12">
			<label for="inputRestricción_alimenticia" class="form-label">Restricciones alimenticias</label
			>
			<input
				bind:value={restrictionsI}
				type="text"
				class="form-control"
				id="inputRestricción_alimenticia"
			/>
		</div>
		<div class=" col-6 d-flex container mt-3">
			<div class="col-3 me-5">
				<button onclick={RegistroFisicState} class="btn btn-primary" disabled={isLoading}
					>{isLoading ? 'Enviando...' : 'Enviar'}</button
				>
			</div>
			<div class="col-3">
				<a class="btn btn-danger" href="/intuser_cli">cancelar</a>
			</div>
		</div>
	</form>
</div>
