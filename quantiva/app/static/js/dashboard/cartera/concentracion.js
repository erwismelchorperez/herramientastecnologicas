let topAcreditadosChart = null;
let topAcreditadosVencidoChart = null;
let top20AcreditadosCreditosChart = null;
let rankingAntiguedadPagoChart = null;
$(document).ready(function(){
    initChart();

    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    let sucursal = $('#sucursalSelect').val();
    console.log("document                " + sucursal);
    loadTopAcreditadosChart(sucursal, anio, mes);
    loadTopAcreditadosVencidoChart(sucursal, anio, mes);
    loadTop20AcreditadosCreditosChart(sucursal, anio, mes);
    loadRankingAntiguedadPagoChart(sucursal, anio, mes);
});
function initFilters(){
    $('#sucursalSelect').on('change', function(){
        let anio = $("#anioSelect").val();
        let mes = $('#mesSelect').val();
        let sucursal = $(this).val();
        console.log("Sucursal seleccionada:     ", sucursal)
        $.ajax({
            url: '/api/years',
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
                        mes = $("#mesSelect").val();
                        loadTopAcreditadosChart(sucursal, anio, mes);
                        loadTopAcreditadosVencidoChart(sucursal, anio, mes);
                        loadTop20AcreditadosCreditosChart(sucursal, anio, mes);
                    },
                    error: function (xhr) {
                        console.error(xhr);
                    }
                });
            }
        });
    }
    );
   $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let sucursal = $("#sucursalSelect").val();
        let mes = $('#mesSelect').val();
        console.log("Año seleccionado:", anio);
        console.log("Sucursal seleccionado:", sucursal);
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
                mes = $("#mesSelect").val();
                loadTopAcreditadosChart(sucursal, anio, mes);
                loadTopAcreditadosVencidoChart(sucursal, anio, mes);
                loadTop20AcreditadosCreditosChart(sucursal, anio, mes);
            },
            error: function (xhr) {
                console.error(xhr);
            }
        });
    });
    $('#mesSelect').on('change', function () {
        let anio = $('#anioSelect').val();
        let mes = $(this).val();
        let sucursal = $('#sucursalSelect').val();
        console.log(anio, mes);
        loadTopAcreditadosChart(sucursal, anio, mes);
        loadTopAcreditadosVencidoChart(sucursal, anio, mes);
        loadTop20AcreditadosCreditosChart(sucursal, anio, mes);
    });
}
function initChart() {
    topAcreditadosChart = createBarChart({
        element: '#chart_top_acreditados',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Acreditado',
        yAxisTitle: 'Capital total',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 400,
        horizontal: true,
        stacked: false,
        legend: false,
        borderRadius: 4
    });
    topAcreditadosVencidoChart = createBarChart({
        element: '#chart_top_acreditados_vencido',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Acreditado',
        yAxisTitle: 'Capital Vencido',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 400,
        horizontal: true,
        stacked: false,
        legend: false,
        borderRadius: 4, colors: ['#ff6384']
    });
    top20AcreditadosCreditosChart = createBarChart({
        element: '#chart_top20_acreditados_creditos',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Número de créditos',
        yAxisTitle: 'Número de socio',
        valueType: 'number',
        compact: true,
        decimals: 2,
        height: 400,
        horizontal: false,
        stacked: false,
        legend: false,
        borderRadius: 4, colors: ['#4bc0c0']
    });
    rankingAntiguedadPagoChart = createBarChart({
        element: '#chart_ranking_antiguedad_pago',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Días de mora',
        yAxisTitle: 'Número de crédito',
        compact: true,
        decimals: 2,
        height: 400,
        horizontal: false,
        stacked: false,
        legend: false,
        borderRadius: 4, colors: ['#4bc0c0']
    });

}
function loadTopAcreditadosChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_top_10_acreditados_capital',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function(response) {
            if (topAcreditadosChart) {
                topAcreditadosChart.destroy();
            }

            topAcreditadosChart = createBarChart({
                element: '#chart_top_acreditados',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Acreditado',
                yAxisTitle: 'Capital total',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 400,
                horizontal: false,
                stacked: false,
                legend: false,
                borderRadius: 4
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el ranking de acreditados:', error);
        }
    });
}
function loadTopAcreditadosVencidoChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_top_10_acreditados_capital_vencido',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function(response) {
            if (topAcreditadosVencidoChart) {
                topAcreditadosVencidoChart.destroy();
            }

            topAcreditadosVencidoChart = createBarChart({
                element: '#chart_top_acreditados_vencido',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Acreditado',
                yAxisTitle: 'Capital Vencido',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 400,
                horizontal: false,
                stacked: false,
                legend: false,
                borderRadius: 4, colors: ['#ff6384']
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el ranking de acreditados:', error);
        }
    });
}
function loadTop20AcreditadosCreditosChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_top_20_acreditados_numero_creditos',
        method: 'GET',
        data: { sucursal, anio, mes },
        success: function(response) {
            if (top20AcreditadosCreditosChart) {
                top20AcreditadosCreditosChart.destroy();
            }

            top20AcreditadosCreditosChart = createBarChart({
                element: '#chart_top20_acreditados_creditos',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Número de créditos',
                yAxisTitle: 'Número de socio',
                valueType: 'number',
                compact: true,
                decimals: 2,
                height: 400,
                horizontal: false,
                stacked: false,
                legend: false,
                borderRadius: 4, colors: ['#4bc0c0']
            });
        },
        error: function(xhr) {
            console.error('Error al cargar créditos por acreditado:', xhr.responseText);
        }
    });
}
function loadRankingAntiguedadPagoChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_ranking_creditos_mayor_antiguedad_pago',
        method: 'GET',
        data: { sucursal, anio, mes, limite: 20 },
        success: function(response) {
            if (rankingAntiguedadPagoChart) {
                rankingAntiguedadPagoChart.destroy();
            }

            rankingAntiguedadPagoChart = createBarChart({
                element: '#chart_ranking_antiguedad_pago',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Días de mora',
                yAxisTitle: 'Número de crédito',
                valueType: 'number',
                compact: true,
                decimals: 2,
                height: 400,
                horizontal: false,
                stacked: false,
                legend: false,
                borderRadius: 4, colors: ['#4bc0c0']
            });
        },
        error: function(xhr) {
            console.error(
                'Error al cargar el ranking de antigüedad de pago:',
                xhr.responseText
            );
        }
    });
}