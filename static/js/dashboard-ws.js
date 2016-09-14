/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

// context menu objects

var contextMenuArray = new Array();
var contextMenuArrayCount = 0;

function ret_context_obj() {
    var context_obj = [
        { header: "Operation" },
        {
            text: "View",
            custom_data: "1",
            action: function (e) {
                var dev_obj;
                var devList = JSON.parse(localStorage['device_status']);
                var dId, lId, id; 
                e.preventDefault();
                dId = $(this).parent().parent()[0].getAttribute("id").split('-')[1]
                console.log(this);
                for (var j in relation){
                    if (relation[j] == dId){
                        lId = j;
                        break;
                    }
                }
                if (lId){
                    id = $('#' + lId).data().devSerialnum;
                } else {
                    console.log('can not find this id.');
                    return false;
                }

                for (var i = 0; i < devList.length; i++) {
                    if (devList[i].id == id) {
                        dev_obj = devList[i];
                        break;
                    }
                }
                if (dev_obj) {
                    $('#devDetailModalContent').empty();
                    for (var p in dev_obj) {
                        if (p) {
                            $('#devDetailModalContent').append(
                                '<span>' + p + ':</span><p>' + dev_obj[p] + '</p>'
                            );
                        }
                    };
                    $('#devDetailModal').modal('show');
                } else {
                    console.log('can not find this device.');
                }
            }
        }
    ];
    return context_obj;
}


function devLst_color_style(s, l) {
    var res = '';
    (l.indexOf(s) >= 0) ? res = "success" : res = "danger";
    return res
}

function devLst_append(serialNum, status, name, icon) {
    $('#device-list').append(
        '<li onclick="deviceList(this)" id="' + serialNum.replace(":","").replace(":","").replace(":","").replace(":","").replace(":","") + '" data-dev-serialnum="' + serialNum + '" data-dev-status="' +
        status + '" data-dev-name="' +
        name + '"><a class="hover-list">' + name +
        '</a><div class="div-pull-right"><span class="label label-' +
        icon + '">' + status + '</span></div>'
    );
    contextMenuArray[contextMenuArrayCount] = new Context();
    console.log(contextMenuArray.length);
    contextMenuArray[contextMenuArrayCount].init(
        {
            fadeSpeed: 50,
            above: 'auto',
            preventDoubleContext: false,
            compress: false
        }
    )
    contextMenuArray[contextMenuArrayCount].attach(serialNum.replace(":","").replace(":","").replace(":","").replace(":","").replace(":",""), ret_context_obj());
    contextMenuArrayCount ++;
}

function deviceList(it) {
    $("#device-list li").each(function () {
        $(this).removeClass("hover-list-active")
    });
    $(it).addClass("hover-list-active");
}

$(document).ready(function () {

    if (window.localStorage) {
    } else {
        console.log('localStorage NOT supported by your browser!')
    }

    // context menu initial


    // device list filter
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
                    devLst_append(dev_lst[i].id, dev_lst[i].status, dev_lst[i].name, icon);
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
                devLst_append(dev_lst[i].id, dev_lst[i].status, dev_lst[i].name, icon);
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
                        devLst_append(dev_lst[i].id, dev_lst[i].status, dev_lst[i].name, icon);
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

                devLst_append(dev_lst[i].id, dev_lst[i].status, dev_lst[i].name, icon);
            };
        };
    });

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
        }, 500);
        if (timeout > 2) {
            clearTimeout(timeout);
            t = setTimeout(function () {
                var data = $('#device-search').val();
                $('#device-search').trigger('data-filter', [data]);
            }, 500);
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
            if (recv.method == 'Comfirm') {
                // recv message example:
                /*
                {
                    "method": "Comfirm",
                    "timestamp": "",
                    "message": {                        
                        "from_request": "Login/... ..."
                    }
                }               
                */
                console.log('recv comfirm from-request: ' + rec.message.from_request + ' ok')

            } else if (recv.method == 'Refresh') {
                // recv message example:
                /*
                {
                    "method": "Refresh",
                    "timestamp": "",
                    "message": {                        
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
                localStorage['device_status'] = JSON.stringify(recv.message.content);

                $('#device-list').trigger('data-refresh');
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
