$(document).ready(function(){

    $("#archivoCartera").on("change", function(){

        const file = this.files[0];

        if(!file){

            $("#archivoInfo").text(
                "Ningún archivo seleccionado"
            );

            return;
        }

        $("#archivoInfo").html(`
            <i class="bi bi-file-earmark"></i>
            ${file.name}
            <br>
            <small>
                ${(file.size / 1024 / 1024).toFixed(2)} MB
            </small>
        `);

    });


    $("#formImportarCartera").on(
        "submit",
        function(e){

            e.preventDefault();

            importarCartera();

        }
    );


    $("#btnCancelarImportacion").click(function(){

        $("#formImportarCartera")[0].reset();

        $("#archivoInfo").text(
            "Ningún archivo seleccionado"
        );

    });

});

function importarCartera(){
    const form = $("#formImportarCartera")[0];
    const formData = new FormData(form);
    const btn = $("#btnImportar");
    btn.prop("disabled", true);
    btn.html(`
        <i class="bi bi-hourglass-split"></i>
        Procesando...
    `);

    $.ajax({
        url: "/configuracion/api/importar",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){
            console.log(response);
            $("#resultadoImportacion").show();
            $("#resultadoImportacionBody").html(`
                <div class="g4">
                    <div class="kpi kc">
                        <div class="kpi-top">
                            <div>
                                <span class="kpi-lbl">
                                    Registros importados
                                </span>
                                <span class="kpi-val">
                                    ${response.insertados}
                                </span>
                            </div>
                            <div class="kpi-ico">
                                <i class="bi bi-database-check"></i>
                            </div>
                        </div>
                    </div>

                    <div class="kpi kg">
                        <div class="kpi-top">
                            <div>
                                <span class="kpi-lbl">
                                    Año
                                </span>
                                <span class="kpi-val">
                                    ${response.anio}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="kpi ko">
                        <div class="kpi-top">
                            <div>
                                <span class="kpi-lbl">
                                    Mes
                                </span>
                                <span class="kpi-val">
                                    ${response.mes.toUpperCase()}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            `);

            $("#formImportarCartera")[0].reset();
            $("#archivoInfo").text("Ningún archivo seleccionado");
        },
        error: function(xhr){
            console.error(xhr);
            let mensaje ="Ocurrió un error durante la importación.";
            if(xhr.responseJSON){
                mensaje = xhr.responseJSON.message || mensaje;
            }
            $("#resultadoImportacion").show();
            $("#resultadoImportacionBody").html(`
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle"></i>
                    ${mensaje}
                </div>
            `);
        },
        complete: function(){
            btn.prop("disabled", false);
            btn.html(`
                <i class="bi bi-upload"></i>
                Importar cartera
            `);
        }
    });
}