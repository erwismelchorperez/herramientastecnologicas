const MF={family:"'JetBrains Mono', monospace",size:11};
Chart.defaults.color='#4d6690';
Chart.defaults.font=MF;
Chart.defaults.plugins.legend.display=false;
Chart.defaults.plugins.tooltip.backgroundColor='#0f1729';
Chart.defaults.plugins.tooltip.borderColor='#1e3256';
Chart.defaults.plugins.tooltip.borderWidth=1;
Chart.defaults.plugins.tooltip.titleColor='#00d4ff';
Chart.defaults.plugins.tooltip.bodyColor='#dde6f5';
Chart.defaults.plugins.tooltip.padding=10;
Chart.defaults.scale.grid.color='rgba(30,50,86,.5)';
Chart.defaults.scale.ticks.color='#4d6690';
$(document).ready(function(){
    cargardatos();
});
function cargardatos(){
    $.ajax({
        url: '/api/dashboard/cartera',
        success: function (response) {
            console.log(response.chart_labels);
            console.log(response.chart_series);
            buildAnnualChart(response.chart_series,response.chart_labels);
        },
        error: function (xhr) {
            console.error(xhr);
        }

    });
}
function moneyFormat(value){

    if(value>=1000000){
        return '$'+(value/1000000).toFixed(1)+'M';
    }

    if(value>=1000){
        return '$'+(value/1000).toFixed(1)+'K';
    }

    return '$'+value;
}

/* ── Evolución anual ────────────────────────────────────── */

function buildAnnualChart(carteraData,chartLabels){

    new Chart(
        document.getElementById('carteraChart'),
        {
            type:'line',
            data:{
                labels:chartLabels,
                datasets:[
                    {
                        label:'Cartera',
                        data:carteraData,
                        borderColor:'#00d4ff',
                        backgroundColor:'rgba(0,212,255,.15)',
                        tension:.4,
                        fill:true,
                        borderWidth:3,
                        pointRadius:4
                    }
                ]
            },
            options:{
                responsive:true,
                maintainAspectRatio:false,
                interaction:{
                    mode:'index',
                    intersect:false
                },
                plugins:{
                    legend:{
                        display:true,
                        labels:{
                            font:MF,
                            boxWidth:10,
                            padding:15,
                            color:'#8ca3c8'
                        }
                    },
                    tooltip:{
                        callbacks:{
                            label:function(context){
                                return (
                                    ' '+
                                    context.dataset.label+
                                    ': '+
                                    moneyFormat(context.raw)
                                );
                            }
                        }
                    }
                },
                scales:{
                    x:{
                        grid:{
                            color:'rgba(30,50,86,.4)'
                        }
                    },
                    y:{
                        ticks:{
                            callback:function(value){
                                return moneyFormat(value);
                            }
                        }
                    }
                }
            }
        }
    );
}
