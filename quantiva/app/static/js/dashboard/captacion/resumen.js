let composicionCaptacionProductoChart = null;
let captacionSucursalChart = null;
$(document).ready(function(){
    initFilters();

    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    let sucursal = $("#sucursalSelect").val();

    loadkpiCaptacion(sucursal,anio, mes);
    loadComposicionCaptacionProducto(sucursal, anio, mes);
    loadCaptacionSucursal(sucursal, anio, mes);
});
function initFilters(){
    $('#sucursalSelect').on('change', function(){
        let anio = $("#anioSelect").val();
        let mes = $("#mesSelect").val();
        let sucursal = $(this).val();
        console.log("Sucursal seleccionada:     ", sucursal)
        $.ajax({
            url: '/api/captacion/years',
            method: 'GET',
            data: {sucursal: sucursal},
            success: function(response){
                let anioSelect = $('#anioSelect');
                anioSelect.empty();
                response.forEach(function (anio) {
                    anioSelect.append(
                        `<option value="${anio}">
                            ${anio}
                        </option>`
                    );
                });
                anio = $("#anioSelect").val();
                $.ajax({
                    url: '/api/months_captacion',
                    method: 'GET',
                    data: {sucursal: sucursal, anio: anio},
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
                        loadkpiCaptacion(sucursal,anio, mes);
                        loadComposicionCaptacionProducto(sucursal, anio, mes);
                        loadCaptacionSucursal(sucursal, anio, mes);
                    },
                    error: function (xhr) {
                        console.error(xhr);
                    }
                });
            }
        });
        
        
    });
    $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let sucursal = $("#sucursalSelect").val();
        console.log("Año seleccionado:", anio);
        $.ajax({
            url: '/api/months_captacion',
            method: 'GET',
            data: {
                sucursal: sucursal,
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
                let mes = $("#mesSelect").val();
                loadkpiCaptacion(sucursal,anio, mes);
                loadComposicionCaptacionProducto(sucursal, anio, mes);
                loadCaptacionSucursal(sucursal, anio, mes);
            },
            error: function (xhr) {
                console.error(xhr);
            }
        });
    });
    $('#mesSelect').on('change', function () {
        let anio = $('#anioSelect').val();
        let mes = $(this).val();
        let sucursal = $("#sucursalSelect").val();
        console.log(anio, mes);
        loadkpiCaptacion(sucursal,anio, mes);
        loadComposicionCaptacionProducto(sucursal, anio, mes);
        loadCaptacionSucursal(sucursal, anio, mes);
    });
}
/* Init charts */
function initChart(){
    composicionCaptacionProductoChart = createBarChart({
        element: '#chart_composicion_captacion_producto',
        labels: response.chart_labels || [],
        series: [{
            name: 'Saldo de captación',
            data: response.chart_values || []
        }],
        title: '',
        xAxisTitle: 'Producto',
        yAxisTitle: 'Saldo de captación ($)',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        horizontal: true,
        height: 400,
        legend: false,
        distributed: true, colors: ['#1E90FF']
    });
}
/* Init charts */
/* Load Chart */
function loadkpiCaptacion(sucursal, anio, mes){
    $.ajax({
        url: '/api/captacion/kpis',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function (response) {
            console.log(response);
            $('#captacionTotal').html(
                    response.captacion_total
                ).attr(
                    'title',
                    '$' + Number(response.captacion_total_title).toLocaleString());
            $('#captacioncaptado').html(
                    response.captacion_captado
                ).attr(
                    'title',
                    '$' + Number(response.captacion_captado_title).toLocaleString());
            $('#captaciondeposito').html(
                    response.captacion_deposito
                ).attr(
                    'title',
                    '$' + Number(response.captacion_deposito_title).toLocaleString());
            $('#captacionretiro').html(
                    response.captacion_retiro
                ).attr(
                    'title',
                    '$' + Number(response.captacion_retiro_title).toLocaleString());
            $('#numero_cuentas').html(
                    response.numero_cuentas
                ).attr(
                    'title',
                    '' + Number(response.numero_cuentas_title).toLocaleString());
            $('#intereses_mes').html(
                    response.intereses_mes
                ).attr(
                    'title',
                    '$' + Number(response.intereses_mes_title).toLocaleString());
            $('#socios_captacion').html(
                    response.socios_captacion
                ).attr(
                    'title',
                    '' + Number(response.socios_captacion_title).toLocaleString());
            $('#capital_plazo').html(
                    response.capital_plazo
                ).attr(
                    'title',
                    '$' + Number(response.capital_plazo_title).toLocaleString());
        },
        error: function (xhr) {
            console.error(xhr);
        }

    });
}
function loadComposicionCaptacionProducto(sucursal, anio, mes) {
    $.ajax({
        url: '/api/captacion/get_composicion_producto',
        method: 'GET',
        data: { sucursal, anio, mes },
        success: function(response) {
            if (composicionCaptacionProductoChart) {
                composicionCaptacionProductoChart.destroy();
            }

            composicionCaptacionProductoChart = createBarChart({
                element: '#chart_composicion_captacion_producto',
                labels: response.chart_labels || [],
                series: [{
                    name: 'Saldo de captación',
                    data: response.chart_values || []
                }],
                title: '',
                xAxisTitle: 'Producto',
                yAxisTitle: 'Saldo de captación ($)',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                horizontal: false,
                height: 400,
                legend: false,
                distributed: true, colors: ['#1E90FF']
            });

            composicionCaptacionProductoChart.render();
        },
        error: function(xhr) {
            console.error(
                'Error al cargar la composición de captación:',
                xhr.responseText
            );
        }
    });
}
function loadCaptacionSucursal(sucursal, anio, mes) {
    $.ajax({
        url: '/api/captacion/sucursal-chart',
        method: 'GET',
        data: { sucursal, anio, mes },
        success: function(response) {
            if (captacionSucursalChart) {
                captacionSucursalChart.destroy();
            }

            captacionSucursalChart = createBarChart({
                element: '#chart_sucursal_captacion',
                labels: response.chart_labels || [],
                series: [{
                    name: 'Saldo de captación',
                    data: response.chart_series || []
                }],
                title: '',
                xAxisTitle: 'Sucursal',
                yAxisTitle: 'Saldo de captación ($)',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                horizontal: false,
                height: 400,
                legend: false,
                distributed: true, colors: ['#1E90FF']
            });

            captacionSucursalChart.render();
        },
        error: function(xhr) {
            console.error(
                'Error al cargar la composición de captación:',
                xhr.responseText
            );
        }
    });
}
/* Load Chart */