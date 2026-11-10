/* Declaracion de variables */
let chartCarteraHistorica = null;
$(document).ready(function(){
    initChart();
    loadCarteraHistoricaChart('all', 2026);
});
/* Init charts */
function initChart(){
    chartCarteraHistorica = createLineChart({
        element: '#chartCarteraHistorica',
        labels: [],
        series: [],
        title: '',
        xAxisTitle: 'Mes',
        yAxisTitle: 'Capital ($)',
        valueType: 'currency',
        compact: true,
        decimals: 2,
        height: 200,
        colors: ['#00d4ff', '#ff6384']
    });
}
/* Init charts */
/* Load Chart */
function loadCarteraHistoricaChart(sucursal, anio) {

    $.ajax({
        url: '/api/cartera/chart',
        method: 'GET',
        data: {
            sucursal: sucursal,
            anio: anio
        },

        success: function(response) {

            const labels = response.chart_labels;
            const values = response.chart_series;

            console.log('Etiquetas:', labels);
            console.log('Series:', values);

            if (chartCarteraHistorica) {
                chartCarteraHistorica.destroy();
                chartCarteraHistorica = null;
            }

            chartCarteraHistorica = createLineChart({
                element: '#chartCarteraHistorica',
                labels: labels,
                series: [{
                    name: 'Capital vigente',
                    data: values
                }],
                title: '',
                xAxisTitle: 'Mes',
                yAxisTitle: 'Capital ($)',
                valueType: 'currency',
                compact: true,
                decimals: 2,
                height: 300,
                colors: ['#00d4ff'],
                legend: false
            });
        },

        error: function(xhr, status, error) {
            console.error(
                'Error al cargar la evolución de cartera:',
                error
            );
        }
    });
}
/* Load Chart */