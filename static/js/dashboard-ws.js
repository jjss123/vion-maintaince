/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

function devLst_color_style(s, l) {
    var res = '';
    (l.indexOf(s) >= 0) ? res = "success" : res = "danger";
    return res
}

function devLst_append(status, name, icon) {
    $('#device-list').append(
        '<li onclick="deviceList(this)" data-dev-status="' +
        status + '" data-dev-name="' +
        name + '"><a class="hover-list">' + name +
        '</a><div class="div-pull-right"><span class="label label-' +
        icon + '">' + status + '</span></div>'
    );
}

function deviceList(it) {
    $("#device-list li").each(function () {
        $(this).removeClass("hover-list-active")
    });
    $(it).addClass("hover-list-active");
}

$('#device-search').bind('data-filter', function (evt, data) {
    var filter = data;
    var dev_lst = JSON.parse(localStorage['device_status']);
    var root = $('#device-list li');
    var count = 0;
    var icon = '';

    $('#device-list').empty();
    if (filter) {
        for (var i = 0; i < dev_lst.length; i++) {
            if ((dev_lst[i].name.indexOf(filter)) >= 0 || (dev_lst[i].status.indexOf(filter) >= 0)) {
                icon = devLst_color_style('Online', dev_lst[i].status);
                devLst_append(dev_lst[i].status, dev_lst[i].name, icon);
                count += 1;
            }
        }

        if (!count) {
            console.log('no result after screening ...');
            $('#device-list').append('<p>no result after screening</p>');
        }

    } else {
        for (var i = 0; i < dev_lst.length; i++) {
            icon = devLst_color_style('Online', dev_lst[i].status);
            devLst_append(dev_lst[i].status, dev_lst[i].name, icon);
        }
    }

});

$('#device-list').bind('data-refresh', function (evt) {
    var icon = '';
    var dev_lst = JSON.parse(localStorage['device_status']);
    var nameset = new Array();
    var data = $('device-search').val();

    if (data) {
        var r = $('#device-list li');
        for (var j = 0; j < r.length; j++) {
            nameset[r[j].getAttribute('data-dev-name')] = r[j];
        };
        for (var i = 0; i < dev_lst.length; i++) {
            if ((dev_lst[i].name.indexOf(data) >= 0) && (dev_lst[i].status.indexOf(data) < 0)) {

                icon = devLst_color_style('Online', dev_lst[i].status);
                (dev_lst[i].status.indexOf('Online') >= 0) ? label = "danger" : label = "success";

                if (!(!!nameset[dev_lst[i].name])) {
                    node = nameset[dev_lst[i].name];
                    node.setAttribute('data-dev-status', dev_lst[i].status);
                    spanLabel = $(node).children('span');
                    if (!(spanLabel.attr('class').indexOf(icon))) {
                        spanLabel.removeClass('label-' + label);
                        spanLabel.addClass('label-' + icon);
                    }
                    spanLabel.html(dev_lst[i].status);
                } else {
                    devLst_append(dev_lst[i].status, dev_lst[i].name, icon);
                }
            } else if ((dev_lst[i].name.indexOf(data) < 0) && (dev_lst[i].status.indexOf(data) < 0)) {
                $('#device-list').empty();
            } else {
                console.log('Query by status NOT supported!');
            }
        };
    } else {
        $('#device-list').empty();
        for (var i = 0; i < dev_lst.length; i++) {
            icon = devLst_color_style('Online', dev_lst[i].status);

            devLst_append(dev_lst[i].status, dev_lst[i].name, icon);
        };
    };
});

$(document).ready(function () {

    if (window.localStorage) {
    } else {
        console.log('localStorage NOT supported by your browser!')
    }

    var timeout;

    $('#device-search').trigger('data-filter', ['']);

    $("#device-search").keypress(function () {
        if (timeout != "undefined") {
            clearTimeout(timeout);
        }
    });
    $("#device-search").keyup(function () {
        t = setTimeout(function () {
            var data = $('#device-search').val();
            $('#device-search').trigger('data-filter', [data]);
        }, 1000);
        if (timeout > 2) {
            clearTimeout(timeout);
            t = setTimeout(function () {
                var data = $('#device-search').val();
                $('#device-search').trigger('data-filter', [data]);
            }, 1000);
        }
    });
});

var url = $('#ws').data('url')

var ws = function (url) {
    if ("WebSocket" in window) {
        var sock = new WebSocket(url);
        var date = new Date();

        sock.onopen = function () {
            sock.send(JSON.stringify({
                "method": "Login",
                "timestamp": date.getTime(),
                "message": {
                    "request": "Login"
                }
            }));
            console.log("connect ...");
            sock.send(JSON.stringify({
                "method": "Get",
                "timestamp": date.getTime(),
                "message": {
                    "request": "Device_Status",
                    "localStorage": JSON.parse(localStorage["device_status"])
                }
            }))
        };
        sock.onmessage = function (evt) {
            var recv = JSON.parse(evt.data);
            if (recv.message.command == 'comfirm') {
                // recv message example:
                /*
                {
                    "method": "",
                    "timestamp": "",
                    "message": {
                        "command":"comfirm",
                        "from_request": "Login/... ..."
                    }
                }               
                */
                console.log('recv comfirm from-request: ' + rec.message.from_request + ' ok')

            } else if (recv.message.command == 'refresh') {
                // recv message example:
                /*
                {
                    "method": "",
                    "timestamp": "",
                    "message": {
                        "command":"refresh",
                        "type": %static/%
                        "content":[
                            {dev info 1},
                            {dev info 2},
                            ...
                        ]
                    }
                }
                dev info example:
                {
                    "id": %device id%,
                    "status": %device status:: Online/Offline/Run Without Svr%,
                    "accredit": %device accredit or not:: Yes/No/No Need%,
                    "ip": %device ip%,
                    "name": %device name%,
                    "type": %device type%,
                    "static": %device static info%
                }
                */
                localStorage['device_status'] = recv.message.content;

                $('#device-list').trigger('data-fresh');
            } else {
                console.log("can not execute command: " + recv.message.command)
            }
        };

        sock.onerror = function () {
            console.log()
        }

        sock.onclose = function () {
            console.log('Connection is closed. Logout');
        };

    } else {
        console.log("WebSocket NOT supported by your Browser!");
    }
}
