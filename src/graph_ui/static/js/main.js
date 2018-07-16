var cleanData = []

var bus = new Vue({

})


var words = {}

var getWord = function(word, limit=50){

    var enterWord = function(data) {
        wordView.addWord(data.word, {
            style: 'root-word'
        })
        
        for(let [type, word, weight] of data.edges) {
            wordView.addRelate(data.word, word, type)
        }
    }

    if( words[word] != undefined
        && words[word].limit >= limit ) {
        enterWord(words[word].data)
    }

    $.get(`/word/${word}/${limit}`, function(data){
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
