let topSociosPorSaldoChart = null;
let topSociosPorNumeroCuentasChart = null;
$(document).ready(function(){
    initFilters();

    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    let sucursal = $("#sucursalSelect").val();
    loadTopSociosPorSaldo(sucursal, anio, mes);
    loadTopSociosPorNumeroCuentas(sucursal, anio, mes);

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
    });
}
/* Init charts */
function initChart(){
    topSociosPorSaldoChart = createBarChart({
        element: '#chart_top_socios_por_saldo',
        labels: [],
        series: [{
            name: 'Saldo',
            data: []
        }],
        title: '',
        xAxisTitle: 'Socio',
        yAxisTitle: 'Saldo',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 350,
        legend: false
    });
    topSociosPorNumeroCuentasChart = createBarChart({
        element: '#chart_top_socios_por_numero_cuentas',
        labels: [],
        series: [{
            name: 'Número de cuentas',
            data: []
        }],
        title: '',
        xAxisTitle: 'Socio',
        yAxisTitle: 'Número de cuentas',
        valueType: 'number',
        compact: true,
        decimals: 0,
        height: 350,
        legend: false
    });
}
/* Init charts */
/* Load Chart */
function loadTopSociosPorSaldo(sucursal, anio, mes = 'all') {
    $.ajax({
        url: '/api/captacion/get_top_ahorradores',
        method: 'GET',
        data: { sucursal, anio, mes },
        success: function(response) {
            if (topSociosPorSaldoChart) {
                topSociosPorSaldoChart.destroy();
            }

            topSociosPorSaldoChart = createBarChart({
                element: '#chart_top_socios_por_saldo',
                labels: response.chart_labels || [],
                series: [{
                    name: 'Saldo',
                    data: response.chart_series || []
                }],
                title: '',
                xAxisTitle: 'Socio',
                yAxisTitle: 'Saldo',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 350,
                legend: false
            });
        },
        error: function(xhr) {
            console.error(
                'Error al cargar el ranking de socios por saldo:',
                xhr.responseText
            );
        }
    });
}
function loadTopSociosPorNumeroCuentas(sucursal, anio, mes = 'all') {
    $.ajax({
        url: '/api/captacion/get_top_socios_por_numero_cuentas',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function(response) {
            if (topSociosPorNumeroCuentasChart) {
                topSociosPorNumeroCuentasChart.destroy();
            }

            topSociosPorNumeroCuentasChart = createBarChart({
                element: '#chart_top_socios_por_numero_cuentas',
                labels: response.chart_labels || [],
                series: [{
                    name: 'Número de cuentas',
                    data: response.chart_values || []
                }],
                title: '',
                xAxisTitle: 'Socio',
                yAxisTitle: 'Número de cuentas',
                valueType: 'number',
                compact: true,
                decimals: 0,
                height: 350,
                legend: false
            });
        },
        error: function(xhr) {
            console.error(
                'Error al cargar el ranking de socios con más cuentas:',
                xhr.responseText
            );
        }
    });
}
/* Load Chart */