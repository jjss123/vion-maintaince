$(document).ready(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
});
function thumbnail(selector) {

    selector.highcharts({
        chart: {
            type: 'area',
            animation: Highcharts.svg,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.random() * 100;
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            },
            plotBackgroundColor: '#FFFFFF',
            plotBorderColor: '#D9EAF4',
            plotBorderWidth: 1,
            reflow: true,
            showAxes: true,
            spacingLeft:5,
            spacingRight:5,
            spacingTop:5,
            spacingBottom:5, 
            width: 70,
            height: 50
        },
        credits: {
            enabled: false,
        },
        title: {
            text: null,
        },
        xAxis: [{
            type: 'datetime',
            gridLineColor: '#FFFFFF',
            gridLineWidth: 1,
            showFirstLabel: true,
            showLastLabel: true,
            tickPixelInterval: 250,
            tickPosition: 'inside',
            labels: {
                enabled: false
            }
        }, {
                type: 'datetime',
                gridLineColor: '#FFFFFF',
                gridLineWidth: 1,
                opposite: true,
                labels: {
                    enabled: false
                }
            }],
        yAxis: {
            opposite: true,
            max: 100,
            min: 0,
            tickInterval: 10,
            title: {
                text: null,
            },
            labels:{
                enabled: false
            },
            gridLineColor: '#FFFFFF',
            gridLineWidth: 1,
        },
        plotOptions: {
            series: {
                lineWidth: 0.7,
                lineColor: '#117DBB',
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: false
                        }
                    }
                }
            },
            area: {
                states: {
                    hover: {
                        enabled: false
                    }
                }
            }
        },
        tooltip: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -59; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.random() * 100
                    });
                }
                return data;
            } ()),
            color: '#F1F6FA'
        }]

    })
}

function draw() {
    $('#highchart-cpu').highcharts({
        chart: {
            type: 'area',
            animation: Highcharts.svg, // don't animate in old IE                
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.random() * 100;
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            },
            plotBackgroundColor: '#FFFFFF',
            plotBorderColor: '#D9EAF4',
            plotBorderWidth: 1,
            reflow: true,
            showAxes: true,
        },
        credits: {
            enabled: false,
        },
        title: {
            align: 'left',
            text: 'CPU',
            style: {
                fontFamily: 'Microsoft YaHei',
                color: '#000000',
                fontSize: '18px',
            },
            floating: true,
        },
        subtitle: {
            align: 'right',
            text: 'Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz'
        },
        xAxis: [{
            type: 'datetime',
            gridLineColor: '#D9EAF4',
            gridLineWidth: 1,
            showFirstLabel: true,
            showLastLabel: true,
            tickPixelInterval: 250,
            tickPosition: 'inside'
        }, {
                type: 'datetime',
                gridLineColor: '#D9EAF4',
                gridLineWidth: 1,
                opposite: true,

            }],
        yAxis: {
            opposite: true,
            max: 100,
            min: 0,
            tickInterval: 10,
            title: {
                text: null,
            },
            gridLineColor: '#D9EAF4',
            gridLineWidth: 1,

        },
        plotOptions: {
            series: {
                lineWidth: 0.7,
                lineColor: '#117DBB',
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: false
                        }
                    }
                }
            },
            area: {
                states: {
                    hover: {
                        enabled: false
                    }
                }
            }
        },
        tooltip: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -59; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.random() * 100
                    });
                }
                return data;
            } ()),
            color: '#F1F6FA'
        }]
    });
};

