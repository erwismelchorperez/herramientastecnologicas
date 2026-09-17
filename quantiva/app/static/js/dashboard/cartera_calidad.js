sucursales = []
let sucursalVigenteChart;
let indiceMorosidadProductoChart;
let distribucionDiasMoraChart = null;
let cantidadCreditosDiasMoraChart = null;
$(document).ready(function(){
    initChart();
    initIndiceMorosidadSucursalChart();
    initIndiceMorosidadProductoChart();
    initDistribucionDiasMoraChart()
    initCantidadCreditosDiasMoraChartOptions()
    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    loadSaldos(anio, mes);
    loadIndiceMorosidadSucursalChart(anio, mes);
    loadIndiceMorosidadProductoChart(anio, mes);
    loadDistribucionDiasMoraChart(anio, mes)
    loadCantidadCreditosDiasMoraChart(anio, mes)
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
                loadIndiceMorosidadProductoChart(anio, mes);
                loadIndiceMorosidadSucursalChart(anio, mes);
                loadDistribucionDiasMoraChart(anio, mes);
                loadCantidadCreditosDiasMoraChart(anio, mes);
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
        loadIndiceMorosidadProductoChart(anio, mes);
        loadDistribucionDiasMoraChart(anio, mes);
        loadCantidadCreditosDiasMoraChart(anio, mes);
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
function loadIndiceMorosidadProductoChart(anio, mes) {
    $.ajax({
        url: '/api/cartera/get_morosidad_por_producto',
        method: 'GET',
        data: {
            anio:anio,
            mes: mes
        },
        success: function(response) {
            console.log(response);
            // ==========================
            // CATEGORÍAS
            // ==========================
            const categories = response.data.map(
                item => item.producto
            );
            // ==========================
            // SERIES
            // ==========================
            const series = [
                {
                    name: 'Morosidad',
                    data: response.data.map(
                        item => item.morosidad
                    )
                }
            ];
            // ==========================
            // DESTRUIR GRÁFICA ANTERIOR
            // ==========================
            indiceMorosidadProductoChart.destroy();
            // ==========================
            // CREAR GRÁFICA
            // ==========================
            indiceMorosidadProductoChart = new ApexCharts(
                document.querySelector("#ch-prod-morosidad"),
                getIndiceMorosidadProductoChartOptions(categories,series)
            );
            indiceMorosidadProductoChart.render();
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar índice de morosidad por producto:',error);
        }
    });
}
function loadDistribucionDiasMoraChart(anio, mes) {
    $.ajax({
        url: '/api/cartera/get_distribucion_dias_mora',
        method: 'GET',
        data: {anio:anio, mes: mes},
        success: function(response) {
            console.log('Distribución por días de mora:',response);
            const categories = response.data.map(
                item => item.rango
            );
            const series = [
                {
                    name: 'Capital vencido',
                    data: response.data.map(
                        item => Number(item.capital_vencido)
                    )
                }
            ];
            if (!distribucionDiasMoraChart) {
                distribucionDiasMoraChart = new ApexCharts(
                    document.querySelector('#ch-dias-mora'),
                    getDistribucionDiasMoraChartOptions(categories,series)
                );
                distribucionDiasMoraChart.render();
            } else {
                distribucionDiasMoraChart.updateOptions({
                    xaxis: {categories: categories}
                });
                distribucionDiasMoraChart.updateSeries(series);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar distribución por días de mora:',error);
        }
    });
}
function loadCantidadCreditosDiasMoraChart(mes) {
    $.ajax({
        url: '/api/cartera/get_cantidad_creditos_por_dias_mora',
        method: 'GET',
        data: { mes: mes },
        success: function(response) {
            const categories = response.data.map(item => item.rango);
            const series = [{
                name: 'Créditos',
                data: response.data.map(item => Number(item.cantidad_creditos))
            }];

            if (!cantidadCreditosDiasMoraChart) {
                cantidadCreditosDiasMoraChart = new ApexCharts(
                    document.querySelector('#ch-cantidad-dias-mora'),
                    getCantidadCreditosDiasMoraChartOptions(categories, series)
                );
                cantidadCreditosDiasMoraChart.render();
            } else {
                cantidadCreditosDiasMoraChart.updateOptions({
                    xaxis: { categories: categories }
                });
                cantidadCreditosDiasMoraChart.updateSeries(series);
            }
        },
        error: function(xhr, status, error) {
            console.error(
                'Error al cargar cantidad de créditos por días de mora:',
                error
            );
        }
    });
}
/* Fin Load Chart */
/* Init charts */
function initIndiceMorosidadProductoChart(){
    indiceMorosidadProductoChart = new ApexCharts(
        document.querySelector(
            "#ch-prod-morosidad"
        ),
        getIndiceMorosidadProductoChartOptions([],[])
    );
    indiceMorosidadProductoChart.render();
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
function initDistribucionDiasMoraChart(){
    distribucionDiasMoraChart = new ApexCharts(
        document.querySelector(
            "#ch-dias-mora"
        ),
        getDistribucionDiasMoraChartOptions([],[])
    );
    distribucionDiasMoraChart.render();
}
function initCantidadCreditosDiasMoraChartOptions(){
    cantidadCreditosDiasMoraChart = new ApexCharts(
        document.querySelector(
            "#ch-cantidad-dias-mora"
        ),
        getCantidadCreditosDiasMoraChartOptions([],[])
    );
    cantidadCreditosDiasMoraChart.render();
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

}
function getIndiceMorosidadProductoChartOptions(categories,series) {
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
            '#00d4ff'
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

                text: 'Producto',

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

                text: 'Índice de morosidad (%)',

                style: {
                    color: '#8ca3c8'
                }

            },

            labels: {

                style: {
                    colors: '#8ca3c8'
                },

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

}
function getDistribucionDiasMoraChartOptions(categories, series) {
    return {
        chart: {
            type: 'bar',
            height: 350,
            background: 'transparent',
            toolbar: {show: false}
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
        dataLabels: {enabled: false},
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
                text: 'Días de mora',
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
                text: 'Capital vencido',
                style: {color: '#8ca3c8'}
            },
            labels: {
                style: {colors: '#8ca3c8'},
                formatter: function(value) {
                    return Number(value).toLocaleString(
                        'es-MX',
                        {
                            notation: 'compact',
                            maximumFractionDigits: 1
                        }
                    );
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
                            style: 'currency',
                            currency: 'MXN',
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );
                }
            }
        }
    };
}
function getCantidadCreditosDiasMoraChartOptions(categories, series) {
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
            '#00d4ff'
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
                text: 'Días de mora',
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
                text: 'Número de créditos',
                style: {
                    color: '#8ca3c8'
                }
            },
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(value) {
                    return Number(value).toLocaleString('es-MX');
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value) {
                    return Number(value).toLocaleString('es-MX') + ' créditos';
                }
            }
        }
    };
}
/* Fin GetCharts */