<!--contenedor de todo-->
    <div class="container">
        <div class="row my-4">
            <div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">
                <div id="Rutina" class="card mb-5">
                    <h4 class="card-header">Diagnostico</h4>
                    <div class="card-body ">
                        <div id="RutinaUser" class="my-4 mx-1 border border-info rounded p-1" >
                            <!--DIAGNOSTICO-->
                        </div>
                        <!--NOTA-->
                        <!--<div class="form-floating">
                            <textarea id="txtnota" class="form-control"></textarea>
                            <label for="txtnota">Queja u opinion:</label>
                        </div>-->
                    </div>
                </div>
            </div>
            <div class="col-lg-7 col-md-7 col-sm-12 col-xs-12 ">
                <div class="card">
                    <div class="card-header bg-success">
                        <div class="row">
                            <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                                <h4 id="nombrerutina" class="text-center text-white"><!--nombre de la rutina--></h4>
                            </div>
                            <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                                <h4 id="nivelR" class="text-center text-white">Nivel: <!--nivel de la rutina--></h4>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <label for="descripR" class="form-label"><b>Descripción</b></label>
                            <!--descripción de la rutina-->
                            <textarea name="" readonly id="descripR" class="form-control"></textarea required>                               
                        </div>
                        <div class="table-responsive">
                            <table id="tablaRtUser" class=" table table-striped " style="width:100%">
                                <thead>
                                    <tr>
                                        <th>id</th>
                                        <th><b>Ejercicios</b> </th>
                                        <th><b>Duración</b></th>
                                        <th><b>Series</b></th>
                                        <th><b>Repeticiones</b></th>
                                    </tr>
                                </thead>
                                <tbody>
                                </tbody>
                           </table>
                       </div>
                    </div>
                </div>
            </div>
        </div>
    </div>