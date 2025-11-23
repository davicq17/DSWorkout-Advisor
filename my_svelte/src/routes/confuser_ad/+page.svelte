<script lang="ts">
	// para esta entrega
	import Navbar from '$lib/components/Navbar.svelte';
	import axios from 'axios';
	import { onMount } from 'svelte';
	// almacen de datos
	let usuarios: any[] = $state([]);
	let userEdit: any = $state(null);
	let userEliminar: any = $state(null);

	onMount(() => {
		Init_Data();
	});
	// pedir datos de la bd
	const Init_Data = async () => {
		try {
			const response = await axios.get('http://127.0.0.1:8000/Usuarios/TableUser');
			usuarios = response.data.map((u: any) => ({
				...u,
				// convertidor del rol en texto
				rolTxt: u.rol === 1 ? 'Administrador' : u.rol === 2 ? 'Usuario' : 'Profesional'
			}));
			console.log('usuarios cargados:', usuarios);
		} catch (err) {
			console.error('Error al cargar usuarios:', err);
		}
	};
	// actualizar usuarios
	const preEditar = (user: any) => {
		// Excluir rolTxt ya que no existe en el backend
		const { rolTxt, ...userData } = user;
		userEdit = userData;
	};

	const Actualizar = async () => {
		console.log('Actualizando usuario:', userEdit);
		try {
			await axios.put(`http://127.0.0.1:8000/Usuarios/editUser/${userEdit.id}`, {
				username: userEdit.username,
				name: userEdit.name,
				surname: userEdit.surname,
				email: userEdit.email,
				password: userEdit.password,
				cell: userEdit.cell,
				rol: userEdit.rol
			});
			alert('usuario actualizado correctamente');
			userEdit = null;
			await Init_Data();
		} catch (err) {
			console.error('Error:', err);
		}
	};

	// Función para eliminar usuario
	const Eliminar = async () => {
		try {
			await axios.put(`http://127.0.0.1:8000/Usuarios/delete/${userEliminar.id}`);
			alert('Usuario eliminado correctamente');
			userEliminar = null;
			await Init_Data();
		} catch (err) {
			console.error('Error al eliminar:', err);
		}
	};
</script>

<!--para está entrega-->
<Navbar rol={1} />
<div class="container my-5">
	<!--principal-->
	<div class="col-12 d-flex justify-content-center">
		<!--div1-->
		<h1 class="h1">Información de Usuarios logueados</h1>
	</div>
	<!--div1-->
	<table
		id="tablaa"
		class="table-bordered table-striped table-hover table-responsive table-responsive-sm table-responsive-lg table-responsive-md table-responsive-xl table"
	>
		<thead class="table-dark">
			<tr>
				<th scope="col">ID</th>
				<th scope="col">Usuario</th>
				<th scope="col">Nombre</th>
				<th scope="col">Apellidos</th>
				<th scope="col">Correo</th>
				<th scope="col">Contraseña</th>
				<th scope="col">Celular</th>
				<th scope="col">Rol</th>
				<th scope="col">Acciones</th>
			</tr>
		</thead>
		<tbody>
			{#each usuarios as user}
				<tr>
					<td>{user.id}</td>
					<td>{user.username}</td>
					<td>{user.name}</td>
					<td>{user.surname}</td>
					<td>{user.email}</td>
					<td>{user.password}</td>
					<td>{user.cell}</td>
					<td>{user.rolTxt}</td>
					<td>
						<button
							onclick={() => preEditar(user)}
							class="btn btn-warning btn-sm ms-3"
							data-bs-toggle="modal"
							data-bs-target="#Editar"
							aria-label="Editar usuario">Editar</button
						>
						<button
							onclick={() => {
								userEliminar = user;
							}}
							class="btn btn-danger btn-sm ms-3"
							data-bs-toggle="modal"
							data-bs-target="#Eliminar"
							aria-label="Eliminar usuario">Eliminar</button
						>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
	<!--Modal para confirmar la eliminacion de un usuario-->
	<div class="modal fade" tabindex="-1" id="Eliminar">
		<!--div2-->
		<div class="modal-dialog">
			<!--div2.1-->
			<div class="modal-content">
				<!--div2.2-->
				<div class="modal-header">
					<!--div2.2.1-->
					<h1 class="my-3 ms-4 text-center">Eliminar Usuario</h1>
				</div>
				<!--div2.2.1-->
				<div class="modal-body">
					<!--div2.2.2-->
					<p class="ms-4 text-start">
						¿Seguro que deseas eliminar al usuario <b>{userEliminar?.username}</b>?
					</p>
				</div>
				<!--div2.2.2-->
				<div class="modal-footer d-flex justify-content-around">
					<!--div2.2.3-->
					<button
						onclick={Eliminar}
						class="btn btn-danger ms-5"
						data-bs-dismiss="modal"
						aria-label="eliminar usuario">Eliminar</button
					>
					<button class="btn btn-primary" data-bs-dismiss="modal">Cancelar</button>
				</div>
				<!--div2.2.3-->
			</div>
			<!--div2.2-->
		</div>
		<!--div2.1-->
	</div>
	<!--div2-->
	<!--Modal para la edicion de datos del usuario-->
	<div class="modal fade" tabindex="-1" id="Editar">
		<!--div3-->
		<div class="modal-dialog">
			<!--div4-->
			<div class="modal-content">
				<!--div5-->
				<div class="modal-header">
					<h1 class="my-3 ms-4 text-center">Editar Usuario</h1>
				</div>
				<div class="modal-body">
					{#if userEdit}
						<div class="row">
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-username" class="form-label">Usuario</label>
									<input
										id="edit-username"
										type="text"
										class="form-control"
										bind:value={userEdit.username}
										placeholder="Nombre de usuario"
									/>
								</div>
							</div>
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-name" class="form-label">Nombre</label>
									<input
										id="edit-name"
										type="text"
										class="form-control"
										bind:value={userEdit.name}
										placeholder="Nombre"
									/>
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-surname" class="form-label">Apellidos</label>
									<input
										id="edit-surname"
										type="text"
										class="form-control"
										bind:value={userEdit.surname}
										placeholder="Apellidos"
									/>
								</div>
							</div>
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-email" class="form-label">Correo</label>
									<input
										id="edit-email"
										type="email"
										class="form-control"
										bind:value={userEdit.email}
										placeholder="correo@ejemplo.com"
									/>
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-password" class="form-label">Contraseña</label>
									<input
										id="edit-password"
										type="password"
										class="form-control"
										bind:value={userEdit.password}
										placeholder="Contraseña"
									/>
								</div>
							</div>
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-cell" class="form-label">Celular</label>
									<input
										id="edit-cell"
										type="text"
										class="form-control"
										bind:value={userEdit.cell}
										placeholder="Número de celular"
									/>
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-6">
								<div class="mb-3">
									<label for="edit-rol" class="form-label">Rol</label>
									<select id="edit-rol" class="form-select" bind:value={userEdit.rol}>
										<option value={1}>Administrador</option>
										<option value={2}>Usuario</option>
										<option value={3}>Profesional</option>
									</select>
								</div>
							</div>
						</div>
					{/if}
				</div>
				<div class="modal-footer d-flex justify-content-around">
					<button
						onclick={Actualizar}
						class="btn btn-success"
						data-bs-dismiss="modal"
						aria-label="Guardar cambios">Guardar</button
					>
					<button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
				</div>
			</div>
			<!--div5-->
		</div>
		<!--div4-->
	</div>
	<!--div3-->
</div>
<!--principal-->
