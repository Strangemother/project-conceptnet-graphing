Vue.component('tokenize', {
    template: $('.templates [data-for="tokenize"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
    , methods: {

        actionName(message) {
            let name = `action-${message.data.action}`
            if(Vue.options.components[name] != undefined) {
                return name;
            }
            return 'action-default'
        }
    }
});

Vue.component('assess', {
    template: $('.templates [data-for="assess"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }

    , methods: {

        actionName(message) {
            let name = `action-${message.data.action}`
            if(Vue.options.components[name] != undefined) {
                return name;
            }
            return 'action-default'
        }

        , word(data) {
            /* return the word from the data */

            if(data.word) {
                return data.word.value
            }
            if(data.value) {
                return data.value
            }
        }
    }
})

Vue.component('action-complete', {
    template: $('.templates [data-for="action-complete"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('default', {
    template: $('.templates [data-for="default"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('tokens-list', {
    template: $('.templates [data-for="tokens-list"]').remove()[0]
    , props: ['tokens', 'message']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-default', {
    template: $('.templates [data-for="action-default"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-start', {
    template: $('.templates [data-for="action-start"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-word', {
    template: $('.templates [data-for="action-word"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
    , methods: {

        renderNodeKey(nkey, node){

            if(node && node.label != undefined) {
                return node.label
            }

            if(nkey == 'weight') {
                return parseFloat(node).toFixed(3)
            }


            return node
        }

        , renderNodeClasses(nkey, node){
            let ignores = ['rel', 'id']
            let nones = [null, undefined, '']
            let word = this.message.data.ident.words[0];

            if(node == undefined) {
                return 'empty'
            }


            if(ignores.indexOf(nkey) > -1){
                return 'hidden'
            }

            if(nkey == 'weight') {
                return nkey
            }


            if(nkey == 'surfaceText'
                && nones.indexOf(node[nkey]) > -1) {
                return 'surface'
            }

            if( (nkey == 'start' || nkey =='end')
                && node.label.toLowerCase() == word.toLowerCase()) {
                return 'match'
            }

            if(node && node.label != undefined) {
                return "type-" + nkey + " label-" + node.label
            }

            return node
        }
    }
})
