var cleanData = []

var bus = new Vue({

})

var questionInput = new Vue({
   el: '#question_input'
    , data: {
        question: 'hello'
        , lastQuestion: ''
        , messages: []
    }
    , mounted(){
        bus.$on('message', this.wsMessage.bind(this))
    }

    , methods: {

        wsMessage(data) {
            //console.log('input from socket', data)
            let tokens = data.data.tokens
            if(tokens == undefined) { tokens = []}
            if(data.data.action) {
                this.messages.unshift({
                    action: data.data.action
                    , tokens: [].slice.call(tokens, 0)
                })
            }

           // bus.$emit('message', data)
        }

        , getWord(word) {
            getWord(word)
        }

        , clear(){
            wordView.nodes().clear()
        }

        , inputString(event) {
            console.log('Enter Key', this.question)
            getWord(this.question)
            this.lastQuestion = this.question
            this.messages.push(this.question)
            this.question = ''
        }
    }
})


var tableView = new Vue({
    el: '#table_view'
    , data: {
        words: ['cake']
    }
    , mounted(){
        bus.$on('word', this.wordEvent.bind(this))
    }

    , methods: {
        wordEvent(data) {
            console.log('word event')
            for(let item of data.edges) {
                this.addLine('edges', item, data.word)
            }

            for(let item of data.rev) {
                this.addLine('rev', item, data.word)
            }
        }

        , addLine(group, entity, word) {
            let line = {
                group, from: word
            }
            line.rel = entity[0]
            line.word = entity[1]
            line.weight = entity[2]
            this.words.push(line)
        }
    }

})

var words = {}

var getWord = function(word, limit=-1){

    var enterWord = function(data) {
        bus.$emit('word', data)
    }

    if( words[word] != undefined
        && words[word].limit >= limit ) {
        enterWord(words[word].data)
    }

    let path = `/word/${word}/`
    if(limit != -1){
        path = `/word/${word}/${limit}`
    }

    $.get(path, function(data){
        words[word] = { limit, data }
        enterWord(data)
    })
}

//$(function(){
//  if ('speechSynthesis' in window) {
//    speechSynthesis.onvoiceschanged = function() {
//      var $voicelist = $('#voices');
//
//      if($voicelist.find('option').length == 0) {
//        speechSynthesis.getVoices().forEach(function(voice, index) {
//          console.log(voice);
//          var $option = $('<option>')
//          .val(index)
//          .html(voice.name + (voice.default ? ' (default)' :''));
//
//          $voicelist.append($option);
//        });
//
//        $voicelist.material_select();
//      }
//    }
//
//    $('#speak').click(function(){
//      var text = $('#message').val();
//      var msg = new SpeechSynthesisUtterance();
//      var voices = window.speechSynthesis.getVoices();
//      msg.voice = voices[$('#voices').val()];
//      msg.rate = $('#rate').val() / 10;
//      msg.pitch = $('#pitch').val();
//      msg.text = text;
//
//      msg.onend = function(e) {
//        console.log('Finished in ' + event.elapsedTime + ' seconds.');
//      };
//
//      console.log(speechSynthesis);
//
//      speechSynthesis.speak(msg);
//    })
//  } else {
//    $('#modal1').openModal();
//  }
//});
