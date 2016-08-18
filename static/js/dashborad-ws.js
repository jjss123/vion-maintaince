/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

function deviceList(it) {
    $("#device-list li").each(function () {
        $(this).removeClass("hover-list-active")
    });
    $(it).addClass("hover-list-active");
}


$('#device-list').bind('data-refresh', function () {
    $('#device-list').empty();
    dev_lst = JSON.parse(localStorage['device_status'])
    for (var i in dev_lst){

    }
});

if (window.localStorage) {
} else {
    console.log('localStorage NOT supported by your browser!')
}

url = $('#ws').data('url')

var ws = function (url) {
    if ("WebSocket" in window) {
        var sock = new WebSocket(url);
        var date = new Date();

        sock.onopen = function () {
            sock.send(JSON.stringfy({
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
