@echo off
echo service list:
echo    web service
echo    websocket service
echo    tcp service
echo external app list:
echo    auto_test
echo ========================================================
echo service starting ...

if "%1" == "python" (

start "vmts_web_service" python ./web_service.py
echo web service starting ...
start "vmts_websocket_service" python ./ws_service.py
echo websocket service starting ...
start "vmts_tcp_service" python ./tcp_service.py
echo tcp service starting ...
echo all powered by python

) else (
if "%1" == "pypy" (

start "vmts_web_service" pypy ./web_service.py
echo web service starting ...
start "vmts_websocket_service" pypy ./ws_service.py
echo websocket service starting ...
start "vmts_tcp_service" pypy ./tcp_service.py
echo tcp service starting ...
echo all powered by pypy

) else (
echo Error: no specific interpreter
echo usage:
echo    launcher.bat [interpreter name]
)
)

