let carteraChart;
let clasificacionChart;
let clasificacion_statusChart;
let sucursalCountChart;
let branchChart;
let sucursalVigenteChart;
let sucursalVencidoChart;
let carteraDonutChart;
let topProductosVigenteChart;
let currentProductosPage=1;
$(document).ready(function(){
    initChart();
    //initClasificacionChart()
    //initBranchChart();
    initClasificacionStatusChart();
    initSucursalCountChart();
    initSucursalVigenteChart()
    initSucursalVencidoChart();
    initCarteraDonutChart();
    initTopProductosVigenteChart();

    initFilters();
    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();

    loadChart(anio);
    loadSaldos(anio, mes);
    //loadClasificacionChart(anio,mes);
    //loadBranchChart(anio,mes);
    loadClasificacionStatusChart(anio,mes);
    loadSucursalCountChart(anio,mes);
    loadSucursalVigenteChart(anio,mes)
    loadSucursalVencidoChart(anio,mes);
    loadCarteraDonutChart(anio,mes);
    loadTopProductosVigenteChart(anio,mes);
    loadProductosTable(anio,mes);
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
                //loadClasificacionChart(anio,mes);
                loadClasificacionStatusChart(anio, mes)
                loadSucursalCountChart(anio, mes)
                loadClasificacionStatusChart(anio, mes)
                loadSucursalVencidoChart(anio,mes);
                loadCarteraDonutChart(anio,mes);
                loadTopProductosVigenteChart(anio,mes);
                loadProductosTable(anio,mes);
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
        loadSaldos(anio,mes)
        //loadClasificacionChart(anio,mes);
        loadClasificacionStatusChart(anio, mes)
        loadSucursalCountChart(anio, mes)
        loadClasificacionStatusChart(anio, mes)
        loadSucursalVencidoChart(anio,mes);
        loadCarteraDonutChart(anio,mes);
        loadTopProductosVigenteChart(anio,mes);
        loadProductosTable(anio,mes);
    });  
}
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
}
function initChart(){
    carteraChart = new ApexCharts(
        document.querySelector(
            "#carteraEvolutionChart"
        ),
        getChartOptions(
                window.chartLabels,
                window.chartSeries
            )
    );
    carteraChart.render();
}
function loadChart(anio) {
    $.ajax({

        url: '/api/cartera/chart',

        method: 'GET',

        data: {
            anio: anio
        },
        success: function(response){
            carteraChart.destroy();
            carteraChart = new ApexCharts(
                document.querySelector(
                    "#carteraEvolutionChart"
                ),
                getChartOptions(
                    response.chart_labels,
                    response.chart_series
                )
            );
            carteraChart.render();
        }
    });
}
function getChartOptions(labels,series){

    return {

        chart: {
            type: 'line',
            height: 200,
            background: 'transparent',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            }
        },

        theme: {
            mode: 'dark'
        },

        series: [{
            name: 'Cartera',
            data: series
        }],

        colors: [
            'rgba(0,212,255,0.95)'
        ],

        stroke: {
            curve: 'smooth',
            width: 3
        },

        markers: {
            size: 4,
            colors: ['#00d4ff'],
            strokeColors: '#081028',
            strokeWidth: 2,
            hover: {
                size: 6
            }
        },

        fill: {
            type: 'gradient',
            gradient: {
                shade: 'dark',
                type: 'vertical',
                shadeIntensity: 0.2,
                gradientToColors: ['rgba(0,212,255,0.05)'],
                inverseColors: false,
                opacityFrom: 0.35,
                opacityTo: 0.02,
                stops: [0,100]
            }
        },

        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },

        dataLabels: {
            enabled: false
        },

        xaxis: {

            categories: labels,

            axisBorder: {
                show: false
            },

            axisTicks: {
                show: false
            },

            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },

        yaxis: {

            labels: {

                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                },

                formatter: function(value){

                    if(value >= 1000000){

                        return '$' +
                            (value / 1000000)
                            .toFixed(1) + 'M';

                    }

                    if(value >= 1000){

                        return '$' +
                            (value / 1000)
                            .toFixed(1) + 'K';

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
                        .toLocaleString();

                }
            }
        },

        legend: {

            labels: {
                colors: '#cbd5e1'
            }
        }
    };

}
function initClasificacionChart(){
    clasificacionChart = new ApexCharts(
        document.querySelector(
            "#clasificacionChart"
        ),
        {
            chart: {
                type: 'bar',
                height: 250,
                toolbar: {
                    show: false
                },
                background: 'transparent'
            },
            colors: [
                'rgba(0,212,255,0.75)',
                'rgba(255,71,87,0.75)'
            ],
            plotOptions: {
                bar: {
                    horizontal: true,
                    columnWidth: '55%',
                    barHeight: '60%',
                    borderRadius: 6
                }
            },
            stroke: {
                show: true,
                width: 1,
                colors: [
                    '#00d4ff',
                    '#ff4757'
                ]
            },
            grid: {
                borderColor: 'rgba(255,255,255,0.05)'
            },
            dataLabels: {
                enabled: true,
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString();
                }
            },
            series: [],
            xaxis: {
                labels: {
                    formatter: function(value){
                        return '$' +
                            Number(value)
                            .toLocaleString();
                    },
                    style: {
                        colors: '#94a3b8'
                    }
                }
            },
            yaxis: {
                categories: [],
                style: {
                    colors: '#94a3b8'
                }
            },
            legend: {
                labels: {
                    colors: '#cbd5e1'
                }
            },
            tooltip: {
                y: {
                    formatter: function(value){
                        return '$' +
                            Number(value)
                            .toLocaleString();
                    }
                }
            }
        }
    );
    clasificacionChart.render();

}
function loadClasificacionChart(anio, mes){
    $.ajax({
        url: '/api/cartera/clasificacion-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            clasificacionChart.updateOptions({
                xaxis: {
                    categories: response.labels
                },
                series: [
                    {
                        name: 'Capital Vigente',
                        data: response.vigente
                    },
                    {
                        name: 'Capital Vencido',
                        data: response.vencido
                    }
                ]
            });
        }
    });
}
function initBranchChart(){
    branchChart = new ApexCharts(
        document.querySelector(
            "#branchChart"
        ),
        {
            chart: {
                type: 'bar',
                height: 400
            },
            colors: [
                '#198754',
                '#dc3545',
                '#0d6efd',
                '#fd7e14',
                '#6f42c1'
            ],
            plotOptions: {
                bar: {
                    horizontal: true,
                    columnWidth: '55%',
                    barHeight: '60%'
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString();
                }
            },
            series: [],
            xaxis: {
                labels: {
                    formatter: function(value){
                        return '$' +
                            Number(value)
                            .toLocaleString();
                    }
                }
            },
            yaxis: {
                categories: []
            },
            tooltip: {
                y: {
                    formatter: function(value){
                        return '$' +
                            Number(value)
                            .toLocaleString();
                    }
                }
            }
        }
    );
    branchChart.render();
}
function loadBranchChart(anio, mes){
    $.ajax({
        url: '/api/cartera/branch-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            branchChart.updateOptions({
                xaxis: {
                    categories: response.labels
                },
                series: [
                    {
                        name: 'Capital Vigente',
                        data: response.vigente
                    },
                    {
                        name: 'Capital Vencido',
                        data: response.vencido
                    }
                ]
            });
        }
    });
}
function initClasificacionStatusChart(){
    clasificacion_statusChart = new ApexCharts(
        document.querySelector(
            "#clasificacion_statusChart"
        ),
        {
            chart: {
                type: 'pie',
                height: 250
            },
            labels: [],
            series: [],
            colors: [
                '#198754',
                '#0d6efd',
                '#ffc107',
                '#dc3545',
                '#6f42c1'
            ],
            legend: {
                position: 'bottom'
            },
            dataLabels: {
                enabled: true,
                formatter: function(value, opts){
                    let total = opts.w.globals.seriesTotals.reduce(
                        (a, b) => a + b,
                        0
                    );
                    let val = opts.w.globals.series[
                        opts.seriesIndex
                    ];
                    return value.toFixed(1) +
                        '% (' +
                        val.toLocaleString()
                        + ')';
                }
            },
            tooltip: {
                y: {
                    formatter: function(value){
                        return Number(value)
                            .toLocaleString();
                    }
                }
            }
        }
    );
    clasificacion_statusChart.render();
}
function loadClasificacionStatusChart(anio, mes){
    $.ajax({
        url: '/api/cartera/clasificacion-status-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            clasificacion_statusChart.updateOptions({
                labels: response.labels
            });
            clasificacion_statusChart.updateSeries(
                response.series
            );
        }
    });
}
function initSucursalCountChart(){
    sucursalCountChart = new ApexCharts(
        document.querySelector(
            "#sucursalCountChart"
        ),
        {
            chart: {
                type: 'pie',
                height: 250
            },
            labels: [],
            series: [],
            colors: [
                '#0d6efd',
                '#198754',
                '#ffc107'
            ],
            legend: {
                position: 'bottom'
            },
            dataLabels: {
                enabled: true,
                formatter: function(value){
                    return value.toFixed(1) + '%';
                }
            },
            tooltip: {
                y: {
                    formatter: function(value){
                        return Number(value)
                            .toLocaleString();
                    }
                }
            }
        }

    );

    sucursalCountChart.render();

}
function loadSucursalCountChart(anio, mes){
    $.ajax({
        url: '/api/cartera/sucursal-count-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            sucursalCountChart.updateOptions({
                labels: response.labels
            });
            sucursalCountChart.updateSeries(
                response.series
            );
        }
    });
}
function initSucursalVigenteChart(){
    sucursalVigenteChart = new ApexCharts(
        document.querySelector(
            "#sucursalVigenteChart"
        ),
        getSucursalVigenteChartOptions([],[])
    );
    sucursalVigenteChart.render();
}
function loadSucursalVigenteChart(anio,mes){
    $.ajax({
        url: '/api/cartera/sucursal-vigente-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            sucursalVigenteChart.destroy();
            sucursalVigenteChart = new ApexCharts(
                document.querySelector(
                    "#sucursalVigenteChart"
                ),
                getSucursalVigenteChartOptions(
                    response.chart_labels,
                    response.chart_series
                )
            );
            sucursalVigenteChart.render();
        }
    });
}
function getSucursalVigenteChartOptions(labels,series){
    return {
        chart: {
            type: 'bar',
            height: 300,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        series: [{
            name: 'Capital Vigente',
            data: series
        }],
        colors: [
            'rgba(124,255,155,0.85)'
        ],
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 6,
                columnWidth: '45%'
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        xaxis: {
            categories: labels,
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(value){
                    if(value >= 1000000){
                        return '$' +
                            (value / 1000000).toFixed(1) + 'M';
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000).toFixed(1) + 'K';
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
                        .toLocaleString();

                }
            }
        }
    };
}
function initSucursalVencidoChart(){
    sucursalVencidoChart = new ApexCharts(
        document.querySelector(
            "#sucursalVencidoChart"
        ),
        getSucursalVencidoChartOptions([],[])
    );
    sucursalVencidoChart.render();
}
function getSucursalVencidoChartOptions(labels,series){
    return {
        chart: {
            type: 'bar',
            height: 300,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        series: [{
            name: 'Capital Vencido',
            data: series
        }],
        colors: [
            'rgba(255,71,87,0.85)'
        ],
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 6,
                columnWidth: '45%'
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        xaxis: {
            categories: labels,
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(value){
                    if(value >= 1000000){
                        return '$' +
                            (value / 1000000).toFixed(1) + 'M';
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000).toFixed(1) + 'K';
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
                        .toLocaleString();
                }
            }
        }
    };
}
function loadSucursalVencidoChart(anio,mes){
    $.ajax({
        url: '/api/cartera/sucursal-vencido-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            sucursalVencidoChart.destroy();
            sucursalVencidoChart = new ApexCharts(
                document.querySelector(
                    "#sucursalVencidoChart"
                ),
                getSucursalVencidoChartOptions(
                    response.chart_labels,
                    response.chart_series
                )
            );
            sucursalVencidoChart.render();
        }
    });
}
function initCarteraDonutChart(){
    carteraDonutChart = new ApexCharts(
        document.querySelector("#carteraDonutChart"),
        getCarteraDonutOptions([0,0])
    );
    carteraDonutChart.render();
}
function getCarteraDonutOptions(series){
    return {
        chart: {
            type: 'pie',
            height: 250,
            background: 'transparent'
        },
        series: series,
        labels: [
            'Capital Vigente',
            'Capital Vencido'
        ],
        colors: [
            'rgba(124,255,155,0.9)',
            'rgba(255,71,87,0.9)'
        ],
        stroke: {
            width: 2,
            colors: ['#0f172a']
        },
        legend: {
            position: 'bottom',
            labels: {
                colors: '#8ca3c8'
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: '12px'
            }
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '68%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Cartera',
                            color: '#8ca3c8',
                            formatter: function(w){
                                let total = w.globals.seriesTotals.reduce(
                                    (a,b) => a + b,
                                    0
                                );
                                if(total >= 1000000){
                                    return '$' +
                                        (total / 1000000)
                                        .toFixed(1) + 'M';
                                }
                                if(total >= 1000){
                                    return '$' +
                                        (total / 1000)
                                        .toFixed(1) + 'K';
                                }
                                return '$' + total;
                            }
                        }
                    }
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString();
                }
            }
        }
    };
}
function loadCarteraDonutChart(anio,mes){
    $.ajax({
        url: '/api/cartera/kpis',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            carteraDonutChart.destroy();
            carteraDonutChart = new ApexCharts(
                document.querySelector("#carteraDonutChart"),
                getCarteraDonutOptions([
                    response.capital_vigente_title,
                    response.capital_vencido_title
                ])
            );
            carteraDonutChart.render();
        }
    });
}
function initTopProductosVigenteChart(){
    topProductosVigenteChart = new ApexCharts(
        document.querySelector(
            "#topProductosVigenteChart"
        ),
        getTopProductosVigenteChartOptions([],[])
    );
    topProductosVigenteChart.render();
}
function getTopProductosVigenteChartOptions(labels,series){
    return {
        chart: {
            type: 'bar',
            height: 400,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        theme: {
            mode: 'dark'
        },
        series: [{
            name: 'Capital Vigente',
            data: series
        }],
        colors: [
            'rgba(0,212,255,0.85)'
        ],
        plotOptions: {
            bar: {
                horizontal: true,
                borderRadius: 6,
                barHeight: '65%'
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        xaxis: {
            categories: labels,
            labels: {
                style: {
                    colors: '#8ca3c8'
                },
                formatter: function(value){
                    if(value >= 1000000){
                        return '$' +
                            (value / 1000000).toFixed(1) + 'M';
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000).toFixed(1) + 'K';
                    }
                    return '$' + value;
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString();
                }
            }
        }
    };
}
function loadTopProductosVigenteChart(anio,mes){
    $.ajax({
        url: '/api/cartera/top-productos-vigente-chart',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function(response){
            topProductosVigenteChart.destroy();
            topProductosVigenteChart = new ApexCharts(
                document.querySelector(
                    "#topProductosVigenteChart"
                ),
                getTopProductosVigenteChartOptions(
                    response.chart_labels,
                    response.chart_series
                )
            );
            topProductosVigenteChart.render();
        }
    });
}
function loadProductosTable(anio,mes,page=1){
    $.ajax({
        url: '/api/cartera/productos-table',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes,
            page:page
        },
        success: function(response){
            let html='';

            response.data.forEach(item=>{

                html+=`
                <tr>
                    <td>${item.producto}</td>
                    <td class="text-end">
                        ${formatCurrencyShort(item.capital_vigente)}
                    </td>
                    <td class="text-end">
                        ${formatCurrencyShort(item.capital_vencido)}
                    </td>
                    <td class="text-end">
                        ${item.numero_creditos.toLocaleString()}
                    </td>
                </tr>
                `;
            });

            $('#productosTableBody').html(html);

            renderProductosPagination(
                response.page,
                response.total_pages
            );
            /*
            let tbody = $('#productosTableBody');
            tbody.empty();
            response.forEach(function(item){
                tbody.append(`
                    <tr>
                        <td>
                            ${item.producto}
                        </td>
                        <td class="text-end text-success">
                            ${formatCurrencyShort(item.capital_vigente)}
                        </td>
                        <td class="text-end text-danger">
                            ${formatCurrencyShort(item.capital_vencido)}
                        </td>
                        <td class="text-end text-info">
                            ${Number(
                                item.numero_creditos
                            ).toLocaleString()}
                        </td>
                    </tr>
                `);
            });
            $('#productosTableBody').html(
                html
            );
            renderProductosPagination(
                response.page,
                response.total_pages,
                anio,
                mes
            );*/
        },
        error:function(xhr){
            console.error(xhr);
        }
    });
}
/*
function renderProductosPagination(page,totalPages){
    let html='';
    html+=`
        <ul class="pagination pagination-sm justify-content-end mb-0">
    `;
    for(let i=1;i<=totalPages;i++){
        html+=`
            <li class="page-item ${i===page?'active':''}">
                <button
                    class="page-link"
                    onclick="changeProductosPage(${i})"
                >
                    ${i}
                </button>
            </li>
            `;
    }
    html+='</ul>';
    $('#productosPagination').html(html);
}*/
function renderProductosPagination(page,totalPages){

    let html='';

    for(let i=1;i<=totalPages;i++){

        html += `
            <button
                class="page-btn ${i===page?'active':''}"
                onclick="changeProductosPage(${i})"
            >
                ${i}
            </button>
        `;
    }

    $('#productosPagination').html(html);
}
function changeProductosPage(page){
    currentProductosPage=page;
    loadProductosTable(
        $('#anioSelect').val(),
        $('#mesSelect').val(),
        page
    );
}
function formatCurrencyShort(value){
    value = Number(value);
    if(value >= 1000000000){
        return '$' +
            (value / 1000000000)
            .toFixed(1) + 'B';
    }
    if(value >= 1000000){
        return '$' +
            (value / 1000000)
            .toFixed(1) + 'M';
    }
    if(value >= 1000){
        return '$' +
            (value / 1000)
            .toFixed(1) + 'K';
    }
    return '$' + value.toLocaleString();
}