function createLineChart({
    element,
    labels,
    series,
    title = '',
    xAxisTitle = '',
    yAxisTitle = '',
    valueType = 'number',
    compact = true,
    decimals = 2,
    height = 250,
    colors = ['#00d4ff', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40'],
    legend = true
}) {
    const container = document.querySelector(element);

    if (!container) {
        console.error(`No existe el contenedor: ${element}`);
        return null;
    }

    const formatValue = (value, abbreviated = false) => {
        if (value === null || value === undefined || value === '') return '-';

        const number = Number(value);

        if (!Number.isFinite(number)) return '-';

        // Porcentajes: morosidad, tasas e indicadores similares
        if (valueType === 'percentage') {
            return number.toLocaleString('es-MX', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            }) + '%';
        }

        // Valores monetarios
        if (valueType === 'currency') {
            if (abbreviated && compact) {
                if (Math.abs(number) >= 1000000) {
                    return '$' + (number / 1000000).toFixed(1) + ' M';
                }

                if (Math.abs(number) >= 1000) {
                    return '$' + (number / 1000).toFixed(1) + ' K';
                }
            }

            return '$' + number.toLocaleString('es-MX', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });
        }

        // Valores numéricos
        if (valueType === 'number' && abbreviated && compact) {
            if (Math.abs(number) >= 1000000) {
                return (number / 1000000).toFixed(1) + ' M';
            }

            if (Math.abs(number) >= 1000) {
                return (number / 1000).toFixed(1) + ' K';
            }
        }

        return number.toLocaleString('es-MX', {
            minimumFractionDigits: valueType === 'decimal' ? decimals : 0,
            maximumFractionDigits: decimals
        });
    };

    const options = {
        chart: {
            type: 'line',
            height,
            background: 'transparent',
            toolbar: { show: false },
            zoom: { enabled: false }
        },
        theme: { mode: 'dark' },
        series,
        colors,
        stroke: {
            curve: 'smooth',
            width: 3
        },
        markers: {
            size: 4,
            strokeWidth: 2,
            strokeColors: '#081028',
            hover: { size: 6 }
        },
        dataLabels: { enabled: false },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        title: {
            text: title,
            style: {
                color: '#cbd5e1',
                fontSize: '14px',
                fontWeight: 600
            }
        },
        xaxis: {
            categories: labels,
            title: {
                text: xAxisTitle,
                style: { color: '#8ca3c8' }
            },
            axisBorder: { show: false },
            axisTicks: { show: false },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            title: {
                text: yAxisTitle,
                style: { color: '#8ca3c8' }
            },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                },
                formatter: value => formatValue(value, true)
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: value => formatValue(value, false)
            }
        },
        legend: {
            show: legend,
            labels: { colors: '#cbd5e1' }
        }
    };

    const chart = new ApexCharts(container, options);
    chart.render();

    return chart;
}
function createBarChart({
    element,
    labels,
    series,
    title = '',
    xAxisTitle = '',
    yAxisTitle = '',
    valueType = 'number',
    compact = true,
    decimals = 2,
    height = 250,
    colors = ['#00d4ff', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40'],
    legend = true,
    horizontal = false,
    stacked = false,
    borderRadius = 4,
    distributed = false}) {
    const container = document.querySelector(element);

    if (!container) {
        console.error(`No existe el contenedor: ${element}`);
        return null;
    }

    const formatValue = (value, abbreviated = false) => {
        if (value === null || value === undefined || value === '') return '-';

        const number = Number(value);
        if (!Number.isFinite(number)) return '-';

        // Porcentajes
        if (valueType === 'percentage') {
            return number.toLocaleString('es-MX', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            }) + '%';
        }

        // Moneda
        if (valueType === 'currency') {
            if (abbreviated && compact) {
                if (Math.abs(number) >= 1000000) {
                    return '$' + (number / 1000000).toLocaleString('es-MX', {
                        maximumFractionDigits: 1
                    }) + ' M';
                }

                if (Math.abs(number) >= 1000) {
                    return '$' + (number / 1000).toLocaleString('es-MX', {
                        maximumFractionDigits: 1
                    }) + ' K';
                }
            }

            return '$' + number.toLocaleString('es-MX', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });
        }

        // Números abreviados
        if (valueType === 'number' && abbreviated && compact) {
            if (Math.abs(number) >= 1000000) {
                return (number / 1000000).toLocaleString('es-MX', {
                    maximumFractionDigits: 1
                }) + ' M';
            }

            if (Math.abs(number) >= 1000) {
                return (number / 1000).toLocaleString('es-MX', {
                    maximumFractionDigits: 1
                }) + ' K';
            }
        }

        return number.toLocaleString('es-MX', {
            minimumFractionDigits: valueType === 'decimal' ? decimals : 0,
            maximumFractionDigits: decimals
        });
    };

    const options = {
        chart: {
            type: 'bar',
            height,
            background: 'transparent',
            toolbar: { show: false },
            zoom: { enabled: false },
            stacked
        },
        theme: {
            mode: 'dark'
        },
        series,
        colors,
        plotOptions: {
            bar: {
                horizontal,
                borderRadius,
                columnWidth: '55%',
                barHeight: '65%',
                distributed
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: 'rgba(255,255,255,0.05)',
            strokeDashArray: 4
        },
        title: {
            text: title,
            align: 'left'
            /*style: {
                color: '#cbd5e1',
                fontSize: '14px',
                fontWeight: 600
            }*/
        },
        xaxis: {
            categories: labels,
            title: {
                text: xAxisTitle,
                style: { color: '#8ca3c8' }
            },
            axisBorder: { show: false },
            axisTicks: { show: false },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            title: {
                text: yAxisTitle,
                style: { color: '#8ca3c8' }
            },
            labels: {
                style: {
                    colors: '#8ca3c8',
                    fontSize: '11px'
                },
                formatter: value => formatValue(value, true)
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: value => formatValue(value, false)
            }
        },
        legend: {
            show: legend && series.length > 1,
            labels: {
                colors: '#cbd5e1'
            }
        }
    };

    const chart = new ApexCharts(container, options);
    chart.render();

    return chart;
}
function createDonutChart({
    element,
    labels = [],
    series = [],
    title = '',
    valueType = 'number',
    compact = true,
    decimals = 2,
    height = 300,
    donut = true,
    legend = true,
    showLabels = true,
    showPercentages = true,
    showTotal = true,
    colors = ['#00d4ff', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40']}) {
    const elementNode = typeof element === 'string'
        ? document.querySelector(element)
        : element;

    if (!elementNode) {
        console.error('No se encontró el elemento para la gráfica:', element);
        return null;
    }

    const values = series.length && Array.isArray(series[0].data)
        ? series[0].data.map(value => Number(value) || 0)
        : [];

    const formatValue = value => {
        const number = Number(value) || 0;

        if (valueType === 'currency') {
            return number.toLocaleString('es-MX', {
                style: 'currency',
                currency: 'MXN',
                notation: compact ? 'compact' : 'standard',
                maximumFractionDigits: decimals
            });
        }

        if (valueType === 'percentage') {
            return `${number.toFixed(decimals)}%`;
        }

        return number.toLocaleString('es-MX', {
            notation: compact ? 'compact' : 'standard',
            maximumFractionDigits: decimals
        });
    };

    const total = values.reduce((sum, value) => sum + value, 0);

    const chart = new ApexCharts(elementNode, {
        chart: {
            type: donut ? 'donut' : 'pie',
            height: height,
            toolbar: {
                show: false
            }
        },
        series: values,
        labels: labels,
        title: {
            text: title,
            align: 'left'
        },
        colors: colors,
        legend: {
            show: legend,
            position: 'bottom',
            fontSize: '12px'
        },
        dataLabels: {
            enabled: showLabels,
            formatter: function (percentage) {
                return showPercentages
                    ? `${percentage.toFixed(1)}%`
                    : '';
            }
        },
        tooltip: {
            y: {
                formatter: function (value) {
                    return formatValue(value);
                }
            }
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: donut && showTotal,
                        name: {
                            show: true,
                            offsetY: -8
                        },
                        value: {
                            show: true,
                            formatter: function (value) {
                                return formatValue(value);
                            }
                        },
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: function () {
                                return formatValue(total);
                            }
                        }
                    }
                }
            }
        },
        noData: {
            text: 'No hay datos disponibles'
        },
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    height: 280
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    });

    chart.render();
    return chart;
}

function createScatterChart({
    element,
    series,
    title,
    xAxisTitle,
    yAxisTitle,
    height = 450
}) {
    const node = document.querySelector(element);
    if (!node) return null;

    const options = {
        chart: {
            type: 'scatter',
            height: height,
            toolbar: { show: true },
            zoom: { enabled: true }
        },
        series: series,
        title: {
            text: title,
            align: 'left'
        },
        xaxis: {
            title: { text: xAxisTitle },
            labels: {
                formatter: value => Number(value).toLocaleString('es-MX', {
                    maximumFractionDigits: 0
                })
            }
        },
        yaxis: {
            title: { text: yAxisTitle },
            labels: {
                formatter: value => Number(value).toLocaleString('es-MX', {
                    maximumFractionDigits: 0
                })
            }
        },
        tooltip: {
            custom: function({ seriesIndex, dataPointIndex, w }) {
                const p = w.config.series[seriesIndex].data[dataPointIndex];
                const moneda = value => Number(value).toLocaleString('es-MX', {
                    style: 'currency',
                    currency: 'MXN',
                    maximumFractionDigits: 2
                });

                return `
                    <div class="p-2">
                        <strong>Socio: ${p.acreditado}</strong><br>
                        Capital total: ${moneda(p.capital_total)}<br>
                        Capital vencido: ${moneda(p.capital_vencido)}<br>
                        Porcentaje vencido: ${p.porcentaje_vencido}%
                    </div>`;
            }
        },
        markers: {
            size: 5
        },
        dataLabels: {
            enabled: false
        }
    };

    return new ApexCharts(node, options);
}