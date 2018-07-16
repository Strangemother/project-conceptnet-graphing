var cleanData = []

var formOutput = new Vue({
    el: '#form_output'
    , data: {
        socketMessages: []
    }

    , methods: {
        messageComponent(message) {
            let name = `${message.data.type}`
            if(Vue.options.components[name] != undefined) {
                return name;
            }

            return 'default'
        }
         , clearMessages(){
            formOutput.socketMessages = []
        }
    }
})

var jsonFetchApp = new Vue({
    el: '#websockets'
    , data: {
        address: 'ws://82.27.16.166:8009'
        , basePath: ''
        , requests: []
        , selected: {}
        , message: undefined
        , connected: false
        , indexItem: -1
    }

    , mounted() {
        this.connect()
    }

    , methods: {

        connect() {
            let p = this.address
            let ws = new WebSocket(p);
            ws.onmessage = this.socketMessage;
            ws.onopen = this.socketOpen;
            this.webSocket = ws;
        }

        , socketMessage(d){

            let m = {
                type: 'in'
                , data: JSON.parse(d.data)
            };

            formOutput.socketMessages.push(m)
            bus.$emit('message', m)
        }

        , socketOpen(d){
            console.log('open', d);
            this.connected = true
        }

        , sendMessage(){
            this.webSocket.send(this.message)
            formOutput.socketMessages.push({
                type: 'out'
                , data: this.message
            })

            this.message = ''
        }


        , fetch(event, partial){
            let path = partial == undefined ? this.$refs.address.value: partial;
            console.log('path', path)
            let fullpath = `${this.basePath}${path}`
            $.get(fullpath, function(data){
                this.renderPath(path, data)
            }.bind(this))
        }

        , renderPath(path, data) {
            console.log('got', data)
            cleanData.push({path, data})
            let dataCopy = JSON.parse(JSON.stringify(data))
            this.requests.push({ path, dataCopy })

        }

    }
})
