sucursales = []
let sucursalVigenteChart;
let sucursalVigenteVencidoChart;
$(document).ready(function(){
    initChart();
    initIndiceMorosidadSucursalChart();
    initSucursalVigenteVencidoChart();
    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    loadSaldos(anio, mes);
    loadIndiceMorosidadSucursalChart(anio, mes);
    loadSucursalVigenteVencidoChart(anio, mes);
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
                loadSaldos(anio,mes)
                loadSucursalVigenteVencidoChart(anio, mes);
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
        loadSaldos(anio,mes);
        loadIndiceMorosidadSucursalChart(anio, mes);
        loadSucursalVigenteVencidoChart(anio, mes);
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
/* Inicio Load Chart */
function loadSaldos(anio, mes){
    $.ajax({
        url: '/api/cartera/kpis',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function (response) {
            console.log(response);
            // =========================
            // ACTUALIZAR KPIs
            // =========================
            subcapitalvencido = (response.capital_vencido_title/response.cartera_total_title)*100
            subcapitalvigente = (response.capital_vigente_title/response.cartera_total_title)*100
            $('#carteraTotal').html(
                    response.cartera_total
                ).attr(
                    'title',
                    '$' + Number(response.cartera_total_title).toLocaleString());
            $('#capitalvencido').html(
                    response.capital_vencido
                ).attr(
                    'title',
                    '$' + Number(response.capital_vencido_title).toLocaleString());
            $('#subcapitalvencido').html(
                   Number(subcapitalvencido).toFixed(2) + "%" + " de la cartera total"
                );
            $('#capitalvigente').html(
                    response.capital_vigente
                ).attr(
                    'title',
                    '$' + Number(response.capital_vigente_title).toLocaleString());
            $('#subcapitalvigente').html(
                   Number(subcapitalvigente).toFixed(2) + "%" + " de la cartera total"
                );
            $('#morosidad').html(
                Number(
                    response.morosidad
                ).toFixed(2)
                + '%'
            );

            $('#creditos_vencidos').html(Number(response.creditos_vencidos).toLocaleString());
            $('#creditos_vigentes').html(Number(response.creditos_vigentes).toLocaleString());
            $('#reestructurado').html(Number(response.creditos_reestructurados).toLocaleString());
            $('#credito_promedio').html(
                    response.credito_promedio
                ).attr(
                    'title',
                    '$' + Number(response.credito_promedio_title).toLocaleString());
        },
        error: function (xhr) {
            console.error(xhr);
        }

    });
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
                                <i class="bi bi-shield-check"></i>
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
function loadIndiceMorosidadSucursalChart(anio, mes){
    console.log("Indice de morosidad sucursal       ",anio, mes)
    $.ajax({
        url: '/api/cartera/get_morosidad_por_sucursal',
        method: 'GET',
        data: {anio: anio, mes: mes},
        success: function(response){
            console.log("Indice Morosidad Sucursal:   ", response);
            //console.log(JSON.stringify(response, null, 2));
            // ==========================
            // CATEGORÍAS
            // ==========================

            const categories = response.data.map(
                item => item.sucursal
            );
            // ==========================
            // SERIES
            // ==========================
            const series = [{
                    name: 'Morosidad',
                    data: response.data.map(
                        item => item.morosidad
                    )
                }];

            sucursalVigenteChart.destroy();
            sucursalVigenteChart = new ApexCharts(
                document.querySelector(
                    "#ch-suc-anual"
                ),
                getIndiceMorosidadSucursalChartOptions(
                    categories,
                    series
                )
            );
            sucursalVigenteChart.render();
        }
    });
}
function loadSucursalVigenteVencidoChart(anio, mes){
    $.ajax({
        url:'/api/cartera/sucursal-vigente-vencido-chart',
        method:'GET',
        data:{
            anio:anio,
            mes:mes
        },
        success:function(response){
            sucursalVigenteVencidoChart.destroy();

            sucursalVigenteVencidoChart =
                new ApexCharts(
                    document.querySelector(
                        "#ch-suc-stack"
                    ),
                    getSucursalVigenteVencidoOptions(
                        response.categories,
                        response.series
                    )
                );
            sucursalVigenteVencidoChart.render();
        }
    });
}
/* Fin Load Chart */
/* Init charts */
function initSucursalVigenteVencidoChart(){
    sucursalVigenteVencidoChart = new ApexCharts(
        document.querySelector(
            "#ch-suc-stack"
        ),
        getSucursalVigenteVencidoOptions([],[])
    );
    sucursalVigenteVencidoChart.render();
}
function initIndiceMorosidadSucursalChart(){
    sucursalVigenteChart = new ApexCharts(
        document.querySelector(
            "#ch-suc-anual"
        ),
        getIndiceMorosidadSucursalChartOptions([],[])
    );
    sucursalVigenteChart.render();
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
/* Fin charts */
/* Init GetCharts */
function getIndiceMorosidadSucursalChartOptions(categories, series) {
    return {
        chart: {
            type: 'bar',
            height: 350,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        series: series,
        colors: ['#00d4ff'],
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 6,
                columnWidth: '65%'
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        legend: {
            position: 'top',
            labels: {colors: '#d8e4f5'}
        },
        xaxis: {
            categories: categories,
            title: {
                text: 'Sucursal',
                style: {color: '#8ca3c8'}
            },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Índice de morosidad (%)',
                style: {
                    color: '#8ca3c8'
                }
            },
            labels: {
                style: {colors: '#8ca3c8'},
                formatter: function(value) {
                    return Number(value).toFixed(2) + '%';
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value) {
                    return Number(value).toLocaleString(
                        'es-MX',
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    ) + '%';
                }
            }
        }
    };

}function getSucursalVigenteVencidoOptions(categories,series){

    return {

        chart:{
            type:'bar',
            height:350,
            stacked:false,
            toolbar:{
                show:false
            }
        },

        series:series,

        colors:[
            '#00E5A0',
            '#FF4757'
        ],

        plotOptions:{
            bar:{
                horizontal:false,
                columnWidth:'50%',
                borderRadius:4
            }
        },

        dataLabels:{
            enabled:false
        },

        stroke:{
            width:0
        },

        grid:{
            borderColor:'rgba(255,255,255,.05)'
        },

        xaxis:{
            categories:categories,
            labels:{
                style:{
                    colors:'#8ca3c8'
                }
            }
        },

        yaxis:{
            labels:{
                style:{
                    colors:'#8ca3c8'
                },
                formatter:function(val){

                    if(val >= 1000000){
                        return (
                            val / 1000000
                        ).toFixed(1) + 'M';
                    }

                    return val.toLocaleString();
                }
            }
        },

        tooltip:{
            theme:'dark',
            y:{
                formatter:function(val){
                    return '$' +
                        Number(val)
                        .toLocaleString(
                            'es-MX',
                            {
                                minimumFractionDigits:2
                            }
                        );
                }
            }
        },

        legend:{
            position:'top',
            labels:{
                colors:'#d8e4f5'
            }
        }
    };
}
/* Fin GetCharts */