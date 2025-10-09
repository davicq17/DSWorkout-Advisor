<!--inicio de sesion-->
    <div class="container ">
        <div class="card  mx-auto mt-5" style="max-width:50rem;">
            <div class="card-header text-white ">
                <center class="fw-bold">INICIAR SESION</center>
            </div>
            <div class="card-body text-dark">
                <div class="card-text">
                    <div class="row">
                        <div class="col-xl6 col-lg-6 col-md-6 col-sm12 col-12 d-flex justify-content-center">
                            <img src="../img/e-trainer.ico" alt="icono">
                        </div>
                        <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12 col-12">
                            <br>
                            <label for="usertxt">USUARIO</label>
                            <input type="text" class="form-control" placeholder="digite el usuario" id="usertxt"><br>
                            <label for="passwordtxt">CONTRASEÑA</label>
                            <input type="password" class="form-control" placeholder="ingrese la contraseña" id="passwordtxt">
                            <label for="rol">ROL</label>
                            <select  id="rol" class="form-control">
                                <option selected="true" value="0"></option>
                                <option value="3">Profesional</option>
                                <option value="2">Fit</option>
                                <option value="1">Administrador</option>
                            </select><br>
                            <button class="btn btn-primary">
                                <a  class="text-decoration-none text-white" href="#">INICIAR</a>
                                <!--onclick="verificar()"-->
                            </button>
                            <button class="btn btn-primary">
                                <a href="/registro" class="text-decoration-none text-white">REGISTRARSE</a>
                            </button>
                            <button class="btn btn-success">
                                <a href="/" class="text-decoration-none text-white ">VOLVER</a>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>