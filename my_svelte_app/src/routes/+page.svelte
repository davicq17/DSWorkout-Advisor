<script>
  import "bootstrap/dist/css/bootstrap.min.css";
  import "../css/Fijos.css";
</script>

<!-- Barra de navegación -->
<nav class="navbar navbar-expand-sm">
  <div class="container-fluid">
    <!-- Logo -->
    <img class="navbar-brand" src="/img/e-trainer.ico" alt="DS LOGO" width="60" height="60" />

    <!-- Botón para abrir el menú -->
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#menu-navbar"
      aria-controls="menu-navbar"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <!-- Menú -->
    <div class="collapse navbar-collapse justify-content-end" id="menu-navbar">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active fw-bold" href="/">INICIO</a>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-bold" href="/howstart">COMO EMPEZAR</a>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-bold" href="/login">INICIAR SESIÓN</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<!-- Contenido principal -->
<div class="container d-flex-column">
  <div class="justify-content-center p-2">
    <div class="row">
      <h4 class="h4">DS Workout Advisor</h4>

      <div class="text-justify col-12 col-md-6">
        <p>
          Es una herramienta Web que lo ayudará en la asesoría de sus ejercicios, con ayuda de un asesor virtual
          llamado E-Trainer, el cual de acuerdo a su estado físico y objetivos propuestos podrá sugerir una rutina
          de ejercicio y un plan de alimentación para complementar y potenciar la actividad física, además cuenta con
          una guía de ejecución para cada ejercicio en caso de que se desconozca la forma correcta de realizarlo.
        </p>
        <p>
          Tenemos un amplio repertorio de ejercicios para asegurarnos de que cualquier tipo de persona pueda mejorar su
          estado físico de manera segura. Cada una de nuestras rutinas es verificada y aprobada por un instructor real,
          al igual que los planes de alimentación.
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
      width="400" height="400" style="border:0;" loading="lazy" 
      referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</div>

<!-- Pie de página -->
<footer class="container-fluid bg-dark text-white mt-4">
  <div class="row p-5 pb-1">
    <div class="col-md-4">
      <p class="h5 mb-3">Autores</p>
      <p class="text-secondary">David José Carrillo Quevedo</p>
      <p class="text-secondary">Stiven Alexander Chico Pelaez</p>
    </div>

    <div class="col-md-4">
      <p class="h5 mb-3">Contactos</p>
      <p class="text-secondary">Teléfono +57 ******</p>
      <p class="text-secondary">WhatsApp +57 ******</p>
    </div>

    <div class="col-md-4">
      <p class="h5 mb-3">Síguenos</p>
      <a href="#"><img src="/img/facebook.ico" alt="Facebook" /></a>
      <a href="#"><img src="/img/instagram.ico" alt="Instagram" /></a>
      <a href="#"><img src="/img/Twiter.ico" alt="Twitter" /></a>
      <a href="#"><img src="/img/tik-tok.ico" alt="TikTok" /></a>
    </div>

    <div class="col-12 pt-3">
      <p class="text-center">Copyright © 2023 DS Workout Advisor. Todos los derechos reservados.</p>
      <p class="text-center">
        <a class="text-decoration-none text-white" href="#">Términos y condiciones</a>
      </p>
    </div>
  </div>
</footer>

<!-- Bootstrap JS <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>-->
