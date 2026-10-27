let garantiasChart = null;
let garantiasSucursalChart = null;
let eprcsucursalChart = null;
let eprcClasificacionChart = null;
$(document).ready(function(){
    initChart();

    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    let sucursal = $('#sucursalSelect').val();
    console.log("document                " + sucursal);
    loadGarantiasChart(sucursal, anio, mes);
    loadGarantiasSucursalChart(sucursal, anio, mes);
    loadEprcSucursalChart(sucursal, anio, mes);
    loadEPRCClasificacionChart(sucursal, anio, mes);
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
                        loadGarantiasChart(sucursal, anio, mes);
                        loadGarantiasSucursalChart(sucursal, anio, mes);
                        loadEprcSucursalChart(sucursal, anio, mes);
                        loadEPRCClasificacionChart(sucursal, anio, mes);
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
                loadGarantiasChart(sucursal, anio, mes);
                loadGarantiasSucursalChart(sucursal, anio, mes);
                loadEprcSucursalChart(sucursal, anio, mes);
                loadEPRCClasificacionChart(sucursal, anio, mes);
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
        loadGarantiasChart(sucursal, anio, mes);
        loadGarantiasSucursalChart(sucursal, anio, mes);
        loadEprcSucursalChart(sucursal, anio, mes);
        loadEPRCClasificacionChart(sucursal, anio, mes);
    });
}
/* Init charts */
function initChart() {
    if (garantiasChart) garantiasChart.destroy();
    if (garantiasSucursalChart) garantiasSucursalChart.destroy();
    if (eprcsucursalChart) eprcsucursalChart.destroy();
    if (eprcClasificacionChart) eprcClasificacionChart.destroy();
    console.log("window.chart_labels: ", window.chart_labels);
    console.log("window.chart_series: ", window.chart_series);
    garantiasChart = createDonutChart({
        element: '#chart_garantias',
        labels: window.chart_labels,
        series: window.chart_series,
        title: '',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 300,
        donut: true,
        legend: true,
        showLabels: true,
        showPercentages: true,
        showTotal: true
    }); 
    garantiasSucursalChart = createBarChart({
        element: '#chart_garantias_sucursal',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Sucursal',
        yAxisTitle: 'Monto de las garantías',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 350,
        horizontal: false,
        stacked: false,
        legend: true,
        borderRadius: 4
    });
    eprcSucursalChart = createBarChart({
        element: '#chart_eprc_sucursal',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Sucursal',
        yAxisTitle: 'Monto de EPRC',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 350,
        horizontal: false,
        stacked: false,
        legend: true,
        borderRadius: 4
    });
    eprcClasificacionChart = createBarChart({
        element: '#chart_eprc_clasificacion',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Clasificación de crédito',
        yAxisTitle: 'Monto de EPRC',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 350,
        horizontal: false,
        stacked: false,
        legend: true,
        borderRadius: 4
    });
}
/* Init charts */
/* Load Chart */
function loadGarantiasChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_montos_por_tipo_garantia',
        method: 'GET',
        data: {sucursal: sucursal, anio: anio, mes: mes},
        success: function(response){
            const labels = response.chart_labels;
            const series = response.chart_series;

            console.log('Etiquetas:', labels);
            console.log('Series:', series);
            if (garantiasChart) {
                garantiasChart.destroy();
            }

            chartGarantias = createDonutChart({
                element: '#chart_garantias',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 300,
                donut: true,
                legend: true,
                showLabels: true,
                showPercentages: true,
                showTotal: true
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar la evolución de cartera:', error);
        }
    });
}
function loadGarantiasSucursalChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_garantias_por_sucursal',
        method: 'GET',
        data: {sucursal: sucursal, anio: anio, mes: mes},
        success: function(response){
            const labels = response.chart_labels;
            const series = response.chart_series;

            console.log('Etiquetas:', labels);
            console.log('Series:', series);
            if (garantiasSucursalChart) {
                garantiasSucursalChart.destroy();
            }

            garantiasSucursalChart = createBarChart({
                element: "#chart_garantias_sucursal",
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Sucursal',
                yAxisTitle: 'Monto de las garantías',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 350,
                horizontal: false,
                stacked: false,
                legend: true,
                borderRadius: 4
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar la evolución de cartera:', error);
        }
    });
}
function loadEprcSucursalChart(sucursal, anio, mes) {
    $.ajax({
        url: '/api/cartera/get_eprc_por_sucursal',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function(response) {
            const labels = response.chart_labels;
            const series = response.chart_series;

            console.log('Etiquetas EPRC:', labels);
            console.log('Series EPRC:', series);

            if (eprcSucursalChart) {
                eprcSucursalChart.destroy();
            }

            eprcSucursalChart = createBarChart({
                element: '#chart_eprc_sucursal',
                labels: labels,
                series: series,
                title: '',
                xAxisTitle: 'Sucursal',
                yAxisTitle: 'Monto de EPRC',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 350,
                horizontal: false,
                stacked: false,
                legend: true,
                borderRadius: 4
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el EPRC por sucursal:', error);
        }
    });
}
function loadEPRCClasificacionChart(sucursal, anio, mes) {
    console.log("loadEPRCClasificacionChart: ", sucursal, anio, mes);
    $.ajax({
        url: '/api/cartera/get_eprc_por_clasificacion',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio,
            mes: mes
        },
        success: function(response) {
            console.log("   Response        ",response);
            if (eprcClasificacionChart) {
                eprcClasificacionChart.destroy();
            }

            eprcClasificacionChart = createBarChart({
                element: '#chart_eprc_clasificacion',
                labels: response.chart_labels,
                series: response.chart_series,
                title: '',
                xAxisTitle: 'Clasificación de crédito',
                yAxisTitle: 'Monto de EPRC',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 350,
                horizontal: false,
                stacked: false,
                legend: true,
                borderRadius: 4
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el EPRC por clasificación:', error);
        }
    });
}
/* Load Chart */