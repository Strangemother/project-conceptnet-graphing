echo "Running local client"
cd %~dp0/src/server/
py -m http.server --bind 127.0.0.1
