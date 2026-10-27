/* Declaracion de variables */
let carteraEvolutionVigVencChart = null;
let indicemorosidadAnualChart = null;
let colocacionChart = null;
let creditosOtorgadosChart = null;
$(document).ready(function(){
    initChart();

    initFilters();
    let anio = $('#anioSelect').val();
    let sucursal = $('#sucursalSelect').val();
    console.log("document                " + sucursal);
    loadEvolutionVigVencChart(sucursal, anio);
    loadindiceMorosidadAnualChart(sucursal, anio);
    loadColocacionChart(sucursal, anio);
    loadCreditosOtorgadosChart(sucursal, anio);
});
function initFilters(){
    $('#sucursalSelect').on('change', function(){
        let anio = $("#anioSelect").val();
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
                loadEvolutionVigVencChart(sucursal, anio);
                loadindiceMorosidadAnualChart(sucursal, anio);
                loadColocacionChart(sucursal, anio);
                loadCreditosOtorgadosChart(sucursal, anio);
            }
        });
    }
    );
   $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let sucursal = $("#sucursalSelect").val();
        console.log("Año seleccionado:", anio);
        console.log("Sucursal seleccionado:", sucursal);
        loadEvolutionVigVencChart(sucursal, anio);
        loadindiceMorosidadAnualChart(sucursal, anio);
        loadColocacionChart(sucursal, anio);
        loadCreditosOtorgadosChart(sucursal, anio);
    });
}
/* Init charts */
function initChart(){
    carteraEvolutionVigVencChart = createLineChart({
        element: '#carteraEvolutionVigVencChart',
        labels: window.chartLabels,
        series: window.chartSeries,
        title: 'Evolución de la cartera',
        xAxisTitle: 'Mes',
        yAxisTitle: 'Capital ($)',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 200,
        colors: ['#00d4ff', '#ff6384']
    });
    indicemorosidadAnualChart = createLineChart({
        element: '#morosidadEvolutionChart',
        labels: window.chart_labels,
        series: window.chart_series,
        title: 'Evolución de la morosidad',
        xAxisTitle: 'Mes',
        yAxisTitle: 'Morosidad (%)',
        valueType: 'percentage',
        decimals: 2,
        height: 250,
        colors: ['#00d4ff', '#ff6384']
    });
    colocacionChart = createBarChart({
        element: '#colocacionChart',
        labels: window.chart_labels,
        series: window.chart_series,
        title: 'Colocación mensual de créditos',
        xAxisTitle: 'Mes',
        yAxisTitle: 'Monto colocado ($)',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 250,
        colors: ['#00d4ff'],
        legend: false
    });
    creditosOtorgadosChart = createBarChart({
        element: '#creditosOtorgadosChart',
        labels: window.chart_labels,
        series: window.chart_series,
        title: 'Créditos otorgados por mes',
        xAxisTitle: 'Mes',
        yAxisTitle: 'Número de créditos',
        valueType: 'number',
        compact: false,
        height: 250,
        colors: ['#00d4ff'],
        legend: false
    });
}
/* Init charts */
/* Load Chart */
function loadEvolutionVigVencChart(sucursal, anio) {
    $.ajax({
        url: '/api/cartera/evolution-vig-venc-chart',
        method: 'GET',
        data: {sucursal: sucursal, anio: anio},
        success: function(response){
            const labels = response.chart_labels;
            const series = response.chart_series;

            console.log('Etiquetas:', labels);
            console.log('Series:', series);
            if (carteraEvolutionVigVencChart) {
                carteraEvolutionVigVencChart.destroy();
            }

            carteraEvolutionVigVencChart = createLineChart({
                element: '#carteraEvolutionVigVencChart',
                labels: response.chart_labels,
                series: response.chart_series,
                title: 'Evolución de la cartera',
                xAxisTitle: 'Mes',
                yAxisTitle: 'Capital ($)',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 250,
                colors: ['#00d4ff', '#ff6384']
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar la evolución de cartera:', error);
        }
    });
}
function loadindiceMorosidadAnualChart(sucursal, anio) {
    $.ajax({
        url: '/api/cartera/get_morosidad_anual',
        method: 'GET',
        data: { sucursal: sucursal, anio: anio },
        success: function(response) {
            const categories = response.chart_labels;
            const series = [{
                name: 'Índice de morosidad',
                data: response.chart_series.map(Number)
            }];
            console.log("morosidad anual:           ",response)
            if (indicemorosidadAnualChart) {
                indicemorosidadAnualChart.destroy();
            }

            indicemorosidadAnualChart = createLineChart({
                element: '#morosidadEvolutionChart',
                labels: response.chart_labels,
                series: [
                    {
                        name: 'Morosidad',
                        data: response.chart_series
                    }
                ],
                title: 'Evolución de la morosidad',
                xAxisTitle: 'Mes',
                yAxisTitle: 'Morosidad (%)',
                valueType: 'percentage',
                decimals: 2,
                height: 250,
                colors: ['#00d4ff', '#ff6384']
            });
        },
        error: function(xhr, status, error) {
            console.error(
                'Error al cargar el índice de morosidad anual:',
                error
            );
        }
    });
}
function loadColocacionChart(sucursal, anio) {
    $.ajax({
        url: '/api/cartera/get_colocacion_mensual',
        method: 'GET',
        data: { sucursal, anio },
        success: function(response) {
            if (colocacionChart) {
                colocacionChart.destroy();
            }

            colocacionChart = createBarChart({
                element: '#colocacionChart',
                labels: response.chart_labels,
                series: response.chart_series,
                title: 'Colocación mensual de créditos',
                xAxisTitle: 'Mes',
                yAxisTitle: 'Monto colocado ($)',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 250,
                colors: ['#00d4ff'],
                legend: false
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar la colocación:', error);
        }
    });
}
function loadCreditosOtorgadosChart(sucursal, anio) {
    $.ajax({
        url: '/api/cartera/get_creditos_otorgados_mensual',
        method: 'GET',
        data: { sucursal, anio },
        success: function(response) {
            if (creditosOtorgadosChart) {
                creditosOtorgadosChart.destroy();
            }

            creditosOtorgadosChart = createBarChart({
                element: '#creditosOtorgadosChart',
                labels: response.chart_labels,
                series: response.chart_series,
                title: 'Créditos otorgados por mes',
                xAxisTitle: 'Mes',
                yAxisTitle: 'Número de créditos',
                valueType: 'number',
                compact: false,
                height: 250,
                colors: ['#00d4ff'],
                legend: false
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar los créditos otorgados:', error);
        }
    });
}
/* Fin Load Chart */