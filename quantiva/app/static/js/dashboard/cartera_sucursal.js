sucursales = []
let sucursalVigenteChart;
let sucursalVigenteVencidoChart;
let evolutionProductoChart;
$(document).ready(function(){
    initChart();
    initSucursalVigenteChart();
    initSucursalVigenteVencidoChart();
    initEvolucionProductoChart();
    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    loadSaldos(anio, mes);
    loadSucursalVigenteChart(mes);
    loadSucursalVigenteVencidoChart(anio, mes);
    loadEvolucionProductoChart('all', anio)
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
                loadEvolucionProductoChart('all', anio)
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
        loadSucursalVigenteChart(mes);
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
        url: '/api/cartera/sucursal-vigente-chart',
        method: 'GET',
        data: {
            sucursal: 'all',
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
function loadSucursalVigenteChart(mes){
    $.ajax({
        url: '/api/cartera/sucursal-vigente-anual-chart',
        method: 'GET',
        data: {mes: mes},
        success: function(response){
            //console.log(response);
            //console.log(JSON.stringify(response, null, 2));
            sucursalVigenteChart.destroy();
            sucursalVigenteChart = new ApexCharts(
                document.querySelector(
                    "#ch-suc-anual"
                ),
                getSucursalVigenteAnualChartOptions(
                    response.categories,
                    response.series
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
function loadEvolucionProductoChart(sucursal, anio) {
    $.ajax({
        url: '/api/cartera/get_monto_original_por_producto_mes',
        method: 'GET',
        dataType: 'json',
        data: {
            sucursal: sucursal,
            anio: anio
        },
        success: function(response) {
            const contenedor = document.querySelector('#evolutionProductoChart');

            if (!contenedor) {
                console.error('No existe el contenedor #evolutionProductoChart.');
                return;
            }

            if (evolutionProductoChart) {
                evolutionProductoChart.destroy();
            }

            evolutionProductoChart = new ApexCharts(
                contenedor,
                getEvolucionProductoChartOptions(
                    response.categories,
                    response.series
                )
            );

            evolutionProductoChart.render();
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar evolución por producto:', error);
            console.error(xhr.responseText);
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
function initSucursalVigenteChart(){
    sucursalVigenteChart = new ApexCharts(
        document.querySelector(
            "#ch-suc-anual"
        ),
        getSucursalVigenteAnualChartOptions([],[])
    );
    sucursalVigenteChart.render();
}
function initEvolucionProductoChart(){
    evolutionProductoChart = new ApexCharts(
        document.querySelector(
            "#evolutionProductoChart"
        ),
        getEvolucionProductoChartOptions([],[])
    );
    evolutionProductoChart.render();
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
function getSucursalVigenteAnualChartOptions(categories, series){
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
        colors: [
            '#00d4ff',
            '#00e5a0',
            '#ff8c42',
            '#a78bfa',
            '#ffd93d',
            '#ff4757'
        ],
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
            labels: {
                colors: '#d8e4f5'
            }
        },
        xaxis: {
            categories: categories,
            title: {
                text: 'Año',
                style: {
                    color: '#8ca3c8'
                }
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
                text: 'Capital Vigente',
                style: {
                    color: '#8ca3c8'
                }
            },
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(value){
                    if(value >= 1000000){
                        return '$' +
                            (value / 1000000).toFixed(1) +
                            ' M';
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000).toFixed(1) +
                            ' K';
                    }
                    return '$' + value;
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString(
                            'es-MX',
                            {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            }
                        );
                }
            }
        }
    };
}
function getSucursalVigenteVencidoOptions(categories,series){

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
function getEvolucionProductoChartOptions(categories, series) {
    return {
        chart: {
            type: 'line',
            height: 350,
            background: 'transparent',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            }
        },
        series: series,
        colors: [
            '#00d4ff',
            '#00E5A0',
            '#FFB020',
            '#A78BFA',
            '#FF4757',
            '#F472B6',
            '#38BDF8',
            '#FACC15'
        ],
        stroke: {
            curve: 'smooth',
            width: 3,
            lineCap: 'round'
        },
        markers: {
            size: 4,
            strokeWidth: 2,
            hover: {
                size: 7
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,.05)',
            strokeDashArray: 4,
            padding: {
                left: 10,
                right: 15
            }
        },
        xaxis: {
            categories: categories,
            title: {
                text: 'Mes',
                style: {
                    color: '#8ca3c8'
                }
            },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            },
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            }
        },
        yaxis: {
            title: {
                text: 'Monto original ($)',
                style: {
                    color: '#8ca3c8'
                }
            },
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(val) {
                    if (val >= 1000000) {
                        return (val / 1000000).toFixed(1) + 'M';
                    }
                    if (val >= 1000) {
                        return (val / 1000).toFixed(0) + 'K';
                    }
                    return Number(val).toLocaleString('es-MX');
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(val) {
                    return '$' + Number(val).toLocaleString('es-MX', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                }
            }
        },
        legend: {
            position: 'top',
            labels: {
                colors: '#d8e4f5'
            },
            markers: {
                width: 10,
                height: 10,
                radius: 10
            }
        },
        noData: {
            text: 'No hay datos disponibles',
            align: 'center',
            verticalAlign: 'middle',
            style: {
                color: '#8ca3c8',
                fontSize: '14px'
            }
        }
    };
}
/* Fin GetCharts */