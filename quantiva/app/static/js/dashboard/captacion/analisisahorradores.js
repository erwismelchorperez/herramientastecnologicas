let captacionEvolutionChart;
let captacionProductoChart;
let captacionSucursalChart;
let captacionTipoSocioChart;
sucursales = [];
let topAhorradoresChart;
let ahorradoresSucursalChart;
let numeroCuentasPorSucursalChart = null;
$(document).ready(function(){
    initFilters();
    initCaptacionEvolutionChart();
    initCaptacionProductoChart();
    initCaptacionSucursalChart();
    initCaptacionTipoSocioChart();
    initAhorradoresSucursalChart();

    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    let sucursal = $("#sucursalSelect").val();

    loadCaptacionEvolutionChart(sucursal,anio,mes);
    loadCaptacionProductoChart(sucursal,anio,mes);
    loadCaptacionSucursalChart(sucursal,anio,mes);
    loadCaptacionTipoSocioChart(sucursal,anio,mes);
    loadAhorradoresSucursalChart(sucursal,anio,mes);
    loadNumeroCuentasPorSucursal(sucursal, anio, mes);

});
/* Bloque de inits */
function initCharts(){
    numeroCuentasPorSucursalChart = createBarChart({
        element: '#chart_numero_cuentas_por_sucursal',
        labels: [],
        series: [{
            name: 'Número de cuentas',
            data: []
        }],
        title: '',
        xAxisTitle: 'Sucursal',
        yAxisTitle: 'Número de cuentas',
        valueType: 'number',
        compact: true,
        decimals: 0,
        height: 350,
        legend: false
    });
}
function initFilters(){
    $('#sucursalSelect').on('change', function(){
        let anio = $("#anioSelect").val();
        let mes = $("#mesSelect").val();
        let sucursal = $(this).val();
        console.log("Sucursal seleccionada:     ", sucursal)
        $.ajax({
            url: '/api/captacion/years',
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
                loadSaldos(sucursal,anio,mes)
                loadCaptacionEvolutionChart(sucursal,anio,mes);
                loadCaptacionProductoChart(sucursal,anio,mes);
                loadCaptacionSucursalChart(sucursal,anio,mes);
                loadCaptacionTipoSocioChart(sucursal,anio,mes);
                loadNumeroCuentasPorSucursal(sucursal, anio, mes);
            }
        });
        
        $.ajax({
            url: '/api/months_captacion',
            method: 'GET',
            data: {sucursal: sucursal, anio: anio},
            success: function (response) {
                loadSaldos(sucursal,anio,mes)
                loadCaptacionEvolutionChart(sucursal,anio,mes);
                loadCaptacionProductoChart(sucursal,anio,mes);
                loadCaptacionSucursalChart(sucursal,anio,mes);
                loadCaptacionTipoSocioChart(sucursal,anio,mes);
                loadNumeroCuentasPorSucursal(sucursal, anio, mes);
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
    $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let mes = $("#mesSelect").val();
        let sucursal = $("#sucursalSelect").val();
        console.log("Año seleccionado:", anio, "  mes:   ", mes);
        $.ajax({
            url: '/api/months_captacion',
            method: 'GET',
            data: {
                sucursal: sucursal,
                anio: anio
            },
            success: function (response) {
                loadCaptacionEvolutionChart(sucursal, anio,mes);
                loadCaptacionProductoChart(sucursal,anio,mes);
                loadCaptacionSucursalChart(sucursal,anio,mes);
                loadCaptacionTipoSocioChart(sucursal,anio,mes);
                //loadTopAhorradores(sucursal,anio,mes);
                loadNumeroCuentasPorSucursal(sucursal, anio, mes);
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
        let sucursal = $("#sucursalSelect").val();
        console.log(anio, mes);
        loadCaptacionEvolutionChart(sucursal,anio,mes);
        loadCaptacionProductoChart(sucursal,anio,mes);
        loadCaptacionSucursalChart(sucursal,anio,mes);
        loadCaptacionTipoSocioChart(sucursal,anio,mes);
        loadTopAhorradores(sucursal,anio,mes);
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
function initCaptacionProductoChart(){

    captacionProductoChart = new ApexCharts(
        document.querySelector(
            "#captacionProductoChart"
        ),
        getCaptacionProductoOptions([],[])
    )
    captacionProductoChart.render()
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
function initAhorradoresSucursalChart(){ 
    ahorradoresSucursalChart=new ApexCharts(
        document.querySelector("#ahorradoresSucursalChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    ahorradoresSucursalChart.render()
}
/* Termina bloque de inits */
/* Bloque de load */
function loadCaptacionEvolutionChart(sucursal, anio){
    $.ajax({
        url: '/api/captacion/evolution-chart',
        method: 'GET',
        data: {sucursal: sucursal, anio: anio},
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
function loadCaptacionProductoChart(sucursal, anio,mes){
    $.ajax({
        url: '/api/captacion/producto-chart',
        method: 'GET',
        data: {sucursal:sucursal,anio: anio,mes: mes},
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
function loadCaptacionSucursalChart(sucursal, anio,mes){
    $.ajax({
        url: '/api/captacion/sucursal-chart',
        method: 'GET',
        data: {sucursal: sucursal, anio: anio,mes: mes},
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
function loadCaptacionTipoSocioChart(sucursal,anio,mes){
    $.ajax({
        url: '/api/captacion/tipo-socio-chart',
        method: 'GET',
        data: {sucursal:sucursal, anio: anio,mes: mes},
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
function loadAhorradoresSucursalChart(sucursal,anio,mes){
    $.ajax({
        url: '/api/captacion/get_ahorradores_por_sucursal_chart',
        method: 'GET',
        data:{
            sucursal:sucursal,
            anio: anio,
            mes: mes
        },
        success:function(response){
            ahorradoresSucursalChart.destroy()
            ahorradoresSucursalChart=
                new ApexCharts(
                    document.querySelector("#ahorradoresSucursalChart"),
                    getVerticalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            ahorradoresSucursalChart.render()
        }
    })
}
function loadNumeroCuentasPorSucursal(sucursal, anio, mes = 'all') {
    $.ajax({
        url: '/api/captacion/get_numero_cuentas_por_sucursal',
        method: 'GET',
        data: { sucursal, anio, mes },
        success: function(response) {
            if (numeroCuentasPorSucursalChart) {
                numeroCuentasPorSucursalChart.destroy();
            }

            numeroCuentasPorSucursalChart = createBarChart({
                element: '#chart_numero_cuentas_por_sucursal',
                labels: response.chart_labels || [],
                series: [{
                    name: 'Número de cuentas',
                    data: response.chart_values || []
                }],
                title: '',
                xAxisTitle: 'Sucursal',
                yAxisTitle: 'Número de cuentas',
                valueType: 'number',
                compact: true,
                decimals: 0,
                height: 350,
                legend: false
            });
        },
        error: function(xhr) {
            console.error(
                'Error al cargar el número de cuentas por sucursal:',
                xhr.responseText
            );
        }
    });
}
/* Termina bloque de load */
/* Bloque de get */
function getVerticalBarOptions(labels,series,color){
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
                vertical: true,
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
                        return '' +
                            (value / 1000000)
                            .toFixed(1) + 'M'
                    }
                    if(value >= 1000){
                        return '' +
                            (value / 1000)
                            .toFixed(1) + 'K'
                    }
                    return '' + value
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
                    return '' +
                        Number(value)
                        .toLocaleString()
                }
            }
        }
    }

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
/* Termna bloque de get */