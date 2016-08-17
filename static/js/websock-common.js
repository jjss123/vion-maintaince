/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

var ws = function (url) {
    if ("WebSocket" in window) {
        var sock = new WebSocket(url);

        sock.onopen = function () {
            sock.send("Login");
            console.log("connect ...");
        };
        sock.onmessage = function (evt) {
            var recv = evt.data;
            while (True) {
                console.log(recv);
                sock.send("KeepAlive");
                setInterval(5000);
            }
        };
        sock.onclose = function () {
            console.log('Connection is closed. Logout');
        };
    } else {
        console.log("WebSocket NOT supported by your Browser!");
    }
}