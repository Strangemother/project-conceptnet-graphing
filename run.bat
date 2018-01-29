start %~dp0\run_websocket.bat
start %~dp0\run_client.bat
start "" http://127.0.0.1:8000/
%~dp0\..\env\Scripts\activate.bat
