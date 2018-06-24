var cleanData = []


var jsonFetchApp = new Vue({
    el: '#main'
    , data: {
        address: '/c/en/hello'
        , basePath: 'http://api.conceptnet.io'
        , requests: []
        , selected: {}
        , relations: []
        , indexItem: -1
    }

    , methods: {
        fetch(event, partial){
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
            if(this.indexItem == -1) {
                this.selected = dataCopy
                let _d = {};
                for(let item of data.edges) {
                    _d[item.rel.label] = 1
                };

                this.relations = Object.keys(_d);
            }

        }

    }
})


var bus = new Vue({

})
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
