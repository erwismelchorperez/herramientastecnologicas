sucursales = []
$(document).ready(function(){
    initChart();
    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    loadSaldos(anio, mes);
});
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
                loadChart(anio);
                loadSaldos(anio,mes)
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
    });
    $('#mesSelect').on('change', function () {
        let anio = $('#anioSelect').val();
        let mes = $(this).val();
        console.log(anio, mes);
        //loadSaldos(anio,mes)
    });  
}
function formatMoney(value){
    return '$' + new Intl.NumberFormat(
        'es-MX',
        {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }
    ).format(value);
}

function loadSaldos(anio, mes){

    $.ajax({
        url: '/api/cartera/sucursal-vigente-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){

            let html = '';

            const colors = [
                'kc',
                'kg',
                'ko',
                'kr',
                'ky',
                'kp',
                'kpk'
            ];

            response.chart_labels.forEach((sucursal, index) => {

                const color = colors[index % colors.length];

                html += `
                    <div class="kpi ${color}">
                        <div class="kpi-top">

                            <div>
                                <span class="kpi-lbl">
                                    ${sucursal}
                                </span>

                                <span class="kpi-val">
                                    ${formatMoney(response.chart_series[index])}
                                </span>

                                <span class="kpi-sub">
                                    Capital Vigente
                                </span>
                            </div>

                            <div class="kpi-ico">
                                <i class="bi bi-geo-alt"></i>
                            </div>

                        </div>
                    </div>
                `;
            });

            $('#sucursalesKpi').html(html);
        },
        error: function(xhr){
            console.error(xhr);
        }
    });
}
function initChart(){
    /*carteraChart = new ApexCharts(
        document.querySelector(
            "#carteraEvolutionChart"
        ),
        getChartOptions(
                window.chartLabels,
                window.chartSeries
            )
    );
    carteraChart.render();*/
}