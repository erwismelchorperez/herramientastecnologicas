let sociosSucursalChart;
let sociosSexoChart;
let sociosEdadChart;
let sociosAntiguedadChart;
let sociosEscolaridadChart;
let sociosCodigoPostalChart;
let sociosLocalidadChart;
let sociosMunicipioChart;
$(document).ready(function(){
    initFilters();
    initSociosSexoChart();
    initSociosSucursalChart();
    initSociosEdadChart();
    initSociosAntiguedadChart();
    initSociosEscolaridadChart();
    initSociosCodigoPostalChart();
    initSociosLocalidadChart();
    initSociosMunicipioChart();

    let anio = $('#anioSelect').val();
    let mes = $('#mesSelect').val();
    loadSaldos(anio, mes);
    loadSociosSexoChart(anio, mes);
    loadSociosSucursalChart(anio, mes);
    loadSociosEdadChart(anio,mes);
    loadSociosAntiguedadChart(anio,mes);
    loadSociosEscolaridadChart(anio,mes);
    loadSociosCodigoPostalChart(anio,mes);
    loadSociosLocalidadChart(anio,mes);
    loadSociosMunicipioChart(anio,mes);
});
/* Bloque de inits */
function initFilters(){
    $('#anioSelect').on('change', function () {
        let anio = $(this).val();
        let mes = $("#mesSelect").val();
        console.log("Año seleccionado:", anio, "  mes:   ", mes);
        $.ajax({
            url: '/api/months_socios',
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
                loadSaldos(anio, mes);
                loadSociosSexoChart(anio, mes);
                loadSociosSucursalChart(anio, mes);
                loadSociosEdadChart(anio,mes);
                loadSociosAntiguedadChart(anio,mes);
                loadSociosEscolaridadChart(anio,mes);
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
        loadSaldos(anio, mes);
        loadSociosSexoChart(anio, mes);
        loadSociosSucursalChart(anio, mes);
        loadSociosEdadChart(anio,mes);
        loadSociosAntiguedadChart(anio,mes);
        loadSociosEscolaridadChart(anio,mes);
    });
}
function initSociosSucursalChart(){
    sociosSucursalChart=new ApexCharts(
        document.querySelector("#sociosSucursalChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(0,212,255,0.85)'
        )
    )
    sociosSucursalChart.render()
}
function initSociosSexoChart(){
    sociosSexoChart=new ApexCharts(
        document.querySelector("#sociosSexoChart"),
        getDonutOptions(
            [],
            []
        )
    )
    sociosSexoChart.render()
}
function initSociosEdadChart(){ 
    sociosEdadChart=new ApexCharts(
        document.querySelector("#sociosEdadChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    sociosEdadChart.render()
}
function initSociosAntiguedadChart(){
    sociosAntiguedadChart = new ApexCharts(
        document.querySelector("#sociosAntiguedadChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(255,217,61,0.85)'
        )
    )
    sociosAntiguedadChart.render()
}
function initSociosEscolaridadChart(){ 
    sociosEscolaridadChart=new ApexCharts(
        document.querySelector("#sociosEscolaridadChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    sociosEscolaridadChart.render()
}
function initSociosCodigoPostalChart(){ 
    sociosCodigoPostalChart=new ApexCharts(
        document.querySelector("#sociosCodigoPostalChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    sociosCodigoPostalChart.render()
}
function initSociosLocalidadChart(){ 
    sociosLocalidadChart=new ApexCharts(
        document.querySelector("#sociosLocalidadChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    sociosLocalidadChart.render()
}
function initSociosMunicipioChart(){ 
    sociosMunicipioChart=new ApexCharts(
        document.querySelector("#sociosMunicipioChart"),
        getHorizontalBarOptions(
            [],
            [],
            'rgba(124,255,155,0.85)'
        )
    )
    sociosMunicipioChart.render()
}
/* Termina bloque de inits */
/* Bloque de load */
function loadSaldos(anio, mes){
    $.ajax({
        url: '/api/socios/kpis',
        method: 'GET',
        data: {
            anio: anio,
            mes: mes
        },
        success: function (response) {
            console.log(response);
            $('#capital_social').html(
                    response.capital_social
                ).attr(
                    'title',
                    '$' + Number(response.capital_social_title).toLocaleString());
            $('#socios_activos').html(
                    response.socios_activos
                ).attr(
                    'title',
                    + Number(response.socios_activos_title).toLocaleString());
            $('#altas_mes').html(
                    response.altas_mes
                ).attr(
                    'title', + Number(response.altas_mes_title).toLocaleString());
            $('#bajas_mes').html(
                    response.bajas_mes
                ).attr(
                    'title', + Number(response.bajas_mes_title).toLocaleString());
        },
        error: function (xhr) {
            console.error(xhr);
        }

    });
}
function loadSociosSucursalChart(anio,mes ){
    $.ajax({
        url: '/api/socios/sucursal-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosSucursalChart.destroy()
            sociosSucursalChart=
                new ApexCharts(
                    document.querySelector("#sociosSucursalChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(0,212,255,0.85)'
                    )
                )
            sociosSucursalChart.render()
        }
    })
}
function loadSociosSexoChart(anio,mes){
    $.ajax({
        url:'/api/socios/sexo-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosSexoChart.destroy()
            sociosSexoChart=
                new ApexCharts(
                    document.querySelector("#sociosSexoChart"),
                    getDonutOptions(
                        response.chart_labels,
                        response.chart_series
                    )
                )
            sociosSexoChart.render()
        }
    })
}
function loadSociosEdadChart(anio,mes){
    $.ajax({
        url: '/api/socios/edad-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosEdadChart.destroy()
            sociosEdadChart=
                new ApexCharts(
                    document.querySelector("#sociosEdadChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            sociosEdadChart.render()
        }
    })
}
function loadSociosAntiguedadChart(anio,mes){
    $.ajax({
        url: '/api/socios/antiguedad-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosAntiguedadChart.destroy()
            sociosAntiguedadChart=
                new ApexCharts(
                    document.querySelector("#sociosAntiguedadChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(255,217,61,0.85)'
                    )
                )
            sociosAntiguedadChart.render()
        }
    })
}
function loadSociosEscolaridadChart(anio,mes){
    $.ajax({
        url: '/api/socios/escolaridad-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosEscolaridadChart.destroy()
            sociosEscolaridadChart=
                new ApexCharts(
                    document.querySelector("#sociosEscolaridadChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            sociosEscolaridadChart.render()
        }
    })
}
function loadSociosCodigoPostalChart(anio,mes){
    $.ajax({
        url: '/api/socios/codigopostal-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosCodigoPostalChart.destroy()
            sociosCodigoPostalChart=
                new ApexCharts(
                    document.querySelector("#sociosCodigoPostalChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            sociosCodigoPostalChart.render()
        }
    })
}
function loadSociosLocalidadChart(anio,mes){
    $.ajax({
        url: '/api/socios/localidad-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosLocalidadChart.destroy()
            sociosLocalidadChart=
                new ApexCharts(
                    document.querySelector("#sociosLocalidadChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            sociosLocalidadChart.render()
        }
    })
}
function loadSociosMunicipioChart(anio,mes){
    $.ajax({
        url: '/api/socios/municipio-chart',
        method: 'GET',
        data:{
            anio: anio,
            mes: mes
        },
        success:function(response){
            sociosMunicipioChart.destroy()
            sociosMunicipioChart=
                new ApexCharts(
                    document.querySelector("#sociosMunicipioChart"),
                    getHorizontalBarOptions(
                        response.chart_labels,
                        response.chart_series,
                        'rgba(124,255,155,0.85)'
                    )
                )
            sociosMunicipioChart.render()
        }
    })
}
/* Termina bloque de load */
/* Bloque de get */
function getHorizontalBarOptions( labels, series, color){
    return {
        chart:{
            type:'bar',
            height:250,
            background:'transparent',
            toolbar:{
                show:false
            }
        },
        theme:{
            mode:'dark'
        },
        series:[{
            name:'Socios',
            data:series
        }],
        colors:[
            color
        ],
        plotOptions:{
            bar:{
                horizontal:true,
                borderRadius:6,
                barHeight:'60%'
            }
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        xaxis:{
            categories: labels,
            labels:{
                style:{
                    colors:'#8ca3c8'
                },
                formatter: function(value){
                    if(value >= 1000000){
                        return ''+ (value / 1000000).toFixed(1) + 'M'
                    }
                    if(value >= 1000){
                        return ''+(value / 1000).toFixed(1) + 'K'
                    }
                    return value
                }
            }
        },
        yaxis:{
            labels:{
                style:{
                    colors:'#8ca3c8'
                }
            }
        },
        dataLabels:{
            enabled:false
        },
        tooltip:{
            theme:'dark',
             y: {
                formatter: function(value){
                    return '' + Number(value).toLocaleString()
                }
            }
        }
    }
}
function getDonutOptions(labels,series){
    return{
        chart:{
            type:'donut',
            height:265,
            background:'transparent'
        },
        theme:{
            mode:'dark'
        },
        labels: labels,
        series: series,
        colors:[
            '#00d4ff',
            '#7cff9b',
            '#ffd93d',
            '#ff4757'
        ],
        legend:{
            position:'bottom',
            labels:{
                colors:'#8ca3c8'
            }
        },
        stroke:{
            width:2,
            colors:['#000000']
        },
        dataLabels:{
            enabled:true
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