document.addEventListener("DOMContentLoaded", function () {
    console.log(window.chartData);
    var options = {
        series: window.chartData.counts,
        chart: {
            type: 'donut',
            height: '100%',
            width: '100%',
        },
        labels: window.chartData.topics,
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    height: '70%',
                    width: '100%',
                },
                legend: {
                    position: 'bottom',
                }
            }
        }, {
            breakpoint: 768,
            options: {
                chart: {
                    height: '80%',
                    width: '100%',
                },
                legend: {
                    position: 'bottom',
                }
            }
        }],
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        name: {
                            fontSize: '16px',
                        },
                        value: {
                            fontSize: '20px',
                            formatter: function (val) {
                                return parseFloat(val).toLocaleString('en-US', {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                });
                            }
                        }
                    }
                }
            }
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return parseFloat(val).toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                }
            }
        }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
});

document.addEventListener("DOMContentLoaded", function () {
    fetch('/monthly-data')
        .then(response => response.json())
        .then(data => {
            const monthNames = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", 
                                "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."];

            const categories = data.map(item => monthNames[item.month - 1]);
            const seriesData = data.map(item => parseFloat(item.total_asset_value));
            const totalValue = seriesData.reduce((acc, val) => acc + val, 0);
            const percentageData = seriesData.map(value => (value / totalValue) * 100);

            var options = {
                series: [{
                    name: 'Total Asset Value',
                    data: percentageData
                }],
                chart: {
                    width: '100%',
                    height: 360,
                    type: 'bar',
                },
                plotOptions: {
                    bar: {
                        borderRadius: 10,
                        dataLabels: {
                            position: 'top',
                        },
                    }
                },
                dataLabels: {
                    enabled: true,
                    formatter: function (val) {
                        return `${val.toFixed(2)}%`;
                    },
                    offsetY: -20,
                    style: {
                        fontSize: '12px',
                        colors: ["#304758"]
                    }
                },
                xaxis: {
                    categories: categories,
                    position: 'bottom',
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    tooltip: {
                        enabled: true,
                        formatter: function (val, { seriesIndex, dataPointIndex }) {
                            return `${categories[dataPointIndex]}: ฿${seriesData[dataPointIndex].toLocaleString()}`;
                        }
                    }
                },
                yaxis: {
                    labels: {
                        formatter: function (val) {
                            return val.toLocaleString('en-US', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            });
                        }
                    }
                },
                responsive: [{
                    breakpoint: 768,
                    options: {
                        chart: {
                            height: 300,
                        },
                        dataLabels: {
                            offsetY: -15, 
                        }
                    }
                }, {
                    breakpoint: 480,
                    options: {
                        chart: {
                            height: 250,
                        },
                        dataLabels: {
                            offsetY: -10,
                        }
                    }
                }]
            };

            var chart = new ApexCharts(document.querySelector("#chart2"), options);
            chart.render();
        })
        .catch(error => console.error("Error fetching monthly data:", error));
});

