var sentenceApp = new Vue({
    el: '#sentence'
    , data: {
        sentences: ['foo']
        , words: []
    }

    , mounted(){
        bus.$on('message', this.recvMessage)
    }

    , methods: {
        recvMessage(data) {
            console.log(data.data.type, data.data.action)

            if(data.data.sentence != undefined) {
                if(data.data.type == 'start') {

                    this.sentences.unshift(data.data.sentence)
                }
            }

            let av = data.data.action

            let m = `${data.data.type}_${av}`;
            if(this[m] != undefined) {
                this[m](data)
            }
        }

        , clearMessages(){
            this.words = []
            this.sentences = []
        }

        , sentence_end(d){
            this.words.push({
                word: 'Divide'
                , type: d.data.type
                , classes: `divider ${d.data.action} ${d.data.type}`
            })
        }

        , sentence_start(d){
            this.words.push({
                    word: 'Divide'
                    , type: d.data.type
                    , classes: `divider ${d.data.action} ${d.data.type}`
                })
        }

        , assess_start(d) {
            console.log('assess start', d)
             let words = []
            for (var i = 0; i < d.data.tokens.length; i++) {
                let e = d.data.tokens[i]
                this.words.push({word: e[0], classes: [], type: e[1]})
            }


        }
        , assess_complete(d) {
            console.log('assess complete', d)

            let words = []
            for (var i = 0; i < d.data.result.length; i++) {
                let e = d.data.result[i]
                words.push({word: e[0], classes: [], type: e[2]})
            }

            //this.words = words
        }


        , assess_word(d) {

            let word = d.data.word.value
            console.log('assess word', d)
            let className = 'assessing'
            for (var i = 0; i < this.words.length; i++) {
                if(this.words[i].word == word) {
                    console.log('found one')
                    this.words[i].classes.push(className)
                } else {
                    let r = this.words[i].classes
                    if(r != undefined && r.splice != undefined) {
                        r.splice(r.indexOf(className), 1)    
                    }
                    
                }
            }
        }
    }
})
