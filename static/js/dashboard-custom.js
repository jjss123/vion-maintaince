$(document).ready(function () {
    var flot3 = function () {
        var data_00 = [],
            data_01 = [],
            data_02 = [],
            totalPoints = 100;
        function getRandomData_00() {
            if (data_00.length > 0)
                data_00 = data_00.slice(1);

            while (data_00.length < totalPoints) {

                var prev = data_00.length > 0 ? data_00[data_00.length - 1] : 50,
                    y = prev + Math.random() * 10 - 5;

                if (y < 0) {
                    y = 0;
                } else if (y > 100) {
                    y = 100;
                }

                data_00.push(y);

            }

            var res = [];
            for (var i = 0; i < data_00.length; i++) {
                res.push([i, data_00[i]])
            }

            return res;
        }
        function getRandomData_01() {
            if (data_01.length > 0)
                data_01 = data_01.slice(1);

            while (data_01.length < totalPoints) {

                var prev = data_01.length > 0 ? data_01[data_01.length - 1] : 50,
                    y = prev + Math.random() * 10 - 5;

                if (y < 0) {
                    y = 0;
                } else if (y > 100) {
                    y = 100;
                }

                data_01.push(y);

            }

            var res = [];
            for (var i = 0; i < data_01.length; i++) {
                res.push([i, data_01[i]])
            }

            return res;
        }
        function getRandomData_02() {
            if (data_02.length > 0)
                data_02 = data_02.slice(1);

            while (data_02.length < totalPoints) {

                var prev = data_02.length > 0 ? data_02[data_02.length - 1] : 50,
                    y = prev + Math.random() * 10 - 5;

                if (y < 0) {
                    y = 0;
                } else if (y > 100) {
                    y = 100;
                }

                data_02.push(y);

            }

            var res = [];
            for (var i = 0; i < data_02.length; i++) {
                res.push([i, data_02[i]])
            }

            return res;
        }

        var plot3 = $.plot("#flotchart3", [{ label: "mem", data: getRandomData_00(), color: ["#22BAA0"] }, { label: "cpu", data: getRandomData_01(), color: ["#0099FF"] }, { lable: "net", data: getRandomData_02(), color: ["#CC99FF"] }], {
            series: {
                shadowSize: 0
            },
            yaxis: {
                min: 0,
                max: 100
            },
            xaxis: {
                show: false
            },
            legend: {
                show: true,
                position: "sw"
            },
            grid: {
                color: "#AFAFAF",
                hoverable: true,
                borderWidth: 0,
                backgroundColor: '#FFF'
            },
            tooltip: true,
            tooltipOpts: {
                content: "Y: %y",
                defaultTheme: false
            }
        });

        function update() {
            plot3.setData([{ label: "mem", data: getRandomData_00() }, { label: "cpu", data: getRandomData_01() }, { lable: "net", data: getRandomData_02() }]);

            plot3.draw();
            setTimeout(update, 500);
        }

        update();
    }

    flot3();
})