/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

var ws_func = function (url){
    var sock = io(url)
    sock.on('connect', function(){
        sock.send('hi');

        sock.on('message', function(msg){
            console.log(msg);
            sock.send('aha');
        });

    });
}