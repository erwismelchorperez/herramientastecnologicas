$(document).ready(function(){
    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();

    loadForecastCards('xgboost')
});
function formatNumberShort(value){
    if(value===null||value===undefined){
        return '-';
    }
    value=Number(value);
    if(Math.abs(value)>=1000000000){
        return '$'+(value/1000000000).toFixed(2)+'B';
    }
    if(Math.abs(value)>=1000000){
        return '$'+(value/1000000).toFixed(2)+'M';
    }
    if(Math.abs(value)>=1000){
        return '$'+(value/1000).toFixed(2)+'K';
    }
    return '$'+value.toLocaleString(
        'es-MX',
        {
            minimumFractionDigits:0,
            maximumFractionDigits:2
        }
    );
}
function initFilters(){
   $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let mes = $("#mesSelect").val();
        console.log("Año seleccionado:", anio);
        $.ajax({
            url: '/api/months',
            method: 'GET',
            data: {
                anio: anio
            },
            success: function (response) {
                let mesSelect = $('#mesSelect');
                mesSelect.empty();
                response.forEach(function (mes) {
                    mesSelect.append(
                        `<option value="${mes}">
                            ${mes.toUpperCase()}
                        </option>`
                    );
                });
            },
            error: function (xhr) {console.error(xhr);}
        });
    });
    $('#mesSelect').on('change', function () {
        let anio = $('#anioSelect').val();
        let mes = $(this).val();
        console.log(anio, mes);
    });  
}
function loadForecastCards(modelo='xgboost'){
    console.log(modelo)
    $.ajax({
        url:'/api/forecast_cartera/cards',
        method:'GET',
        data:{modelo:modelo},
        success:function(response){
            $('#forecast_mes').html(
                formatNumberShort(
                    response.forecast
                )
            ).attr(
                'title',
                '$'+Number(
                    response.forecast
                ).toLocaleString()
            )
            $('#forecast_crecimiento').html(
                Number(
                    response.crecimiento
                ).toFixed(2)
                +'%'
            )
            $('#forecast_error').html(
                Number(
                    response.mape
                ).toFixed(2)
                +'%'
            )
            $('#forecast_precision').html(
                Number(
                    response.precision
                ).toFixed(2)
                +'%'
            )
        },
        error:function(xhr){console.error(xhr)}
    })
}