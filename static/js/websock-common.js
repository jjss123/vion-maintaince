/*
* @Author: hylide
* @Date:   2016-08-08 09:58:01
* @Last Modified by:   hylide
* @Last Modified time: 2016-08-08 09:58:59
*/

var ws_func = function (url) {
    ws = new WebSocket(url);

    ws.onopen = function () {
        ws.send({
            "method": "Login",
            "seq": "from client without hash",
            "callback": None,
            "message": {
                "source": "bowers"
            }
        })
    };

    ws.onmessage = function(event){
        console.log(event.data)
        ws.send({
            "method": "KeepAlive",
            "seq": None,
            "callback": None,
            "message":{
                "timestamp": None,
                "source": "bowers",
                "dev_id": None,
                "service": None
            }
        })
    };

    setInterval(5000);


}