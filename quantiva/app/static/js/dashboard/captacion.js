let captacionEvolutionChart;
let captacionProductoChart;
let captacionSucursalChart;
let captacionTipoSocioChart;
$(document).ready(function(){
    initFilters();
    initCaptacionEvolutionChart();
    initCaptacionProductoChart();
    initCaptacionSucursalChart();
    initCaptacionTipoSocioChart();

    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();

    loadSaldos(anio, mes);
    loadCaptacionEvolutionChart();
    loadCaptacionProductoChart();
    loadCaptacionSucursalChart();
    loadCaptacionTipoSocioChart();

});
function initFilters(){
    $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let mes = $("#mesSelect").val();
        console.log("Año seleccionado:", anio, "  mes:   ", mes);
        $.ajax({
            url: '/api/months_captacion',
            method: 'GET',
            data: {
                anio: anio
            },
            success: function (response) {
                loadSaldos(anio,mes)
                loadCaptacionEvolutionChart(anio,mes);
                loadCaptacionProductoChart(anio,mes);
                loadCaptacionSucursalChart(anio,mes);
                loadCaptacionTipoSocioChart(anio,mes);
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
        loadCaptacionEvolutionChart(anio,mes);
        loadCaptacionProductoChart(anio,mes);
        loadCaptacionSucursalChart(anio,mes);
        loadCaptacionTipoSocioChart(anio,mes);
    });
}
function loadSaldos(anio, mes){
    $.ajax({
        url: '/api/captacion/kpis',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function (response) {
            console.log(response);
            $('#captacionTotal').html(
                    response.captacion_total
                ).attr(
                    'title',
                    '$' + Number(response.captacion_total_title).toLocaleString());
            $('#captacioncaptado').html(
                    response.captacion_captado
                ).attr(
                    'title',
                    '$' + Number(response.captacion_captado_title).toLocaleString());
            $('#captaciondeposito').html(
                    response.captacion_deposito
                ).attr(
                    'title',
                    '$' + Number(response.captacion_deposito_title).toLocaleString());
            $('#captacionretiro').html(
                    response.captacion_retiro
                ).attr(
                    'title',
                    '$' + Number(response.captacion_retiro_title).toLocaleString());
        },
        error: function (xhr) {
            console.error(xhr);
        }

    });
}
function initCaptacionEvolutionChart(){

    captacionEvolutionChart = new ApexCharts(
        document.querySelector(
            "#captacionEvolutionChart"
        ),
        getCaptacionEvolutionOptions([],[])
    )
    captacionEvolutionChart.render()
}
function loadCaptacionEvolutionChart(anio){
    $.ajax({
        url: '/api/captacion/evolution-chart',
        method: 'GET',
        data: {anio: anio},
        success: function(response){
            captacionEvolutionChart.destroy()
            captacionEvolutionChart =
                new ApexCharts(
                document.querySelector(
                    "#captacionEvolutionChart"
                ),
                getCaptacionEvolutionOptions(response.chart_labels,response.chart_series)
            )
            captacionEvolutionChart.render()
        }
    })
}
function initCaptacionProductoChart(){

    captacionProductoChart = new ApexCharts(
        document.querySelector(
            "#captacionProductoChart"
        ),
        getCaptacionProductoOptions([],[])
    )
    captacionProductoChart.render()
}
function loadCaptacionProductoChart(anio,mes){
    $.ajax({
        url: '/api/captacion/producto-chart',
        method: 'GET',
        data: {anio: anio,mes: mes},
        success: function(response){
            captacionProductoChart.destroy()
            captacionProductoChart =
                new ApexCharts(
                document.querySelector(
                    "#captacionProductoChart"
                ),
                getCaptacionProductoOptions(response.chart_labels,response.chart_series
                )
            )
            captacionProductoChart.render()
        }
    })
}
function getCaptacionEvolutionOptions(labels,series){
    return {
        chart: {
            type: 'line',
            height: 250,
            toolbar: {
                show: false
            }
        },
        series: [{
            name: 'Captación',
            data: series
        }],
        colors: [
            'rgba(0,212,255,0.95)'
        ],
        stroke: {
            curve: 'smooth',
            width: 3
        },
        fill: {
            type: 'solid',
            opacity: 0.15
        },
        markers: {
            size: 4,
            strokeWidth: 2,
            hover: {
                size: 6
            }
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
                            (value / 1000000)
                            .toFixed(1) + 'M'
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000)
                            .toFixed(1) + 'K'
                    }
                    return '$' + value
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString()
                }
            }
        }
    }
}
function getCaptacionProductoOptions(labels,series){

    return {

        chart: {
            type: 'bar',
            height: 250,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },

        theme: {
            mode: 'dark'
        },

        series: [{
            name: 'Captación',
            data: series
        }],

        colors: [
            'rgba(0,212,255,0.85)'
        ],

        plotOptions: {

            bar: {
                horizontal: true,
                borderRadius: 6,
                barHeight: '60%'
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
                            (value / 1000000)
                            .toFixed(1) + 'M'

                    }

                    if(value >= 1000){

                        return '$' +
                            (value / 1000)
                            .toFixed(1) + 'K'

                    }

                    return '$' + value

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
                        .toLocaleString()

                }
            }
        }
    }

}
function initCaptacionSucursalChart(){
    captacionSucursalChart = new ApexCharts(
        document.querySelector(
            "#captacionSucursalChart"
        ),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(0,212,255,0.85)'
        )
    )
    captacionSucursalChart.render()
}
function initCaptacionTipoSocioChart(){
    captacionTipoSocioChart = new ApexCharts(
        document.querySelector(
            "#captacionTipoSocioChart"
        ),
        getDonutOptions(
            [],
            []
        )
    )
    captacionTipoSocioChart.render()
}
function loadCaptacionSucursalChart(anio,mes){
    $.ajax({
        url: '/api/captacion/sucursal-chart',
        method: 'GET',
        data: {anio: anio,mes: mes},
        success: function(response){
            captacionSucursalChart.destroy()
            captacionSucursalChart =
                new ApexCharts(
                document.querySelector(
                    "#captacionSucursalChart"
                ),
                getHorizontalBarOptions(
                    response.chart_labels,
                    response.chart_series,
                    'rgba(0,212,255,0.85)'
                )
            )
            captacionSucursalChart.render()
        }
    })
}
function loadCaptacionTipoSocioChart(anio,mes){
    $.ajax({
        url: '/api/captacion/tipo-socio-chart',
        method: 'GET',
        data: {anio: anio,mes: mes},
        success: function(response){
            captacionTipoSocioChart.destroy()
            captacionTipoSocioChart =
                new ApexCharts(
                document.querySelector(
                    "#captacionTipoSocioChart"
                ),
                getDonutOptions(
                    response.chart_labels,
                    response.chart_series
                )
            )
            captacionTipoSocioChart.render()
        }
    })
}
function getHorizontalBarOptions(labels,series,color){
    return {
        chart: {
            type: 'bar',
            height: 250,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        series: [{
            name: 'Captación',
            data: series
        }],
        colors: [color],
        plotOptions: {
            bar: {
                horizontal: true,
                borderRadius: 6,
                barHeight: '60%'
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
                            (value / 1000000)
                            .toFixed(1) + 'M'
                    }
                    if(value >= 1000){
                        return '$' +
                            (value / 1000)
                            .toFixed(1) + 'K'
                    }
                    return '$' + value
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
                        .toLocaleString()
                }
            }
        }
    }

}
function getDonutOptions(labels,series){
    return {
        chart: {
            type: 'donut',
            height: 250,
            background: 'transparent'
        },
        theme: {
            mode: 'dark'
        },
        labels: labels,
        series: series,
        colors: [
            '#00d4ff',
            '#7cff9b'
        ],
        legend: {
            position: 'bottom',
            labels: {
                colors: '#8ca3c8'
            }
        },
        stroke: {
            width: 2,
            colors: ['#0f172a']
        },
        dataLabels: {
            enabled: true
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(value){
                    return '$' +
                        Number(value)
                        .toLocaleString()
                }
            }
        }
    }

}