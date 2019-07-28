
var main = function(){
    let wordView = new WordView()
    wordView.start('mynetwork')
    window.wordView = wordView
}

var colormap = {
    'relatedto': '#dcdcdc'
    , 'isa': 'lightblue'
    // similat
    , 'synonym': '#57f09d'
    // opposite
    , 'antonym': 'purple'

    , '>>': 'red'
    , 'derived': 'pink'
    , atlocation: '#7e92d4'
    , receivesaction: '#76d14d'
    , 'hasproperty': '#d1d14d'
    , usedfor: '#444'
    , 'capableof': '#ffb273'
    , 'hasa': '#2d8baa'
    , 'partof':'#b9b2ff'
    , desires: '#f0c66b'
    //, notdesires: ''
    //, etymologicallyrelatedto: ''
    //, distinctfrom: ''
}


class NetworkEvents {

    hook(network){
        var self = this;

        network.on("click", function (params) {
            if(self.on_click != undefined) {
                self.on_click(params)
            }

            params.event = "[original event]";
            this.lastEvent = ['Click', JSON.stringify(params, null, 4)]
            console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
        });

        network.on("doubleClick", function (params) {

            if(self.on_doubleClick != undefined) {
                self.on_doubleClick(params)
            }

            params.event = "[original event]";
            this.lastEvent = ['doubleClick', JSON.stringify(params, null, 4)]
        });
        network.on("oncontext", function (params) {
            if(self.on_oncontext != undefined) {
                self.on_oncontext(params)
            }

            params.event = "[original event]";
            this.lastEvent = ['oncontext', JSON.stringify(params, null, 4)]
        });
        network.on("dragStart", function (params) {
            if(self.on_dragStart != undefined) {
                self.on_dragStart(params)
            }

            // There's no point in displaying this event on screen, it gets immediately overwritten
            params.event = "[original event]";
            console.log('dragStart Event:', params);
            console.log('dragStart event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
        });
        network.on("dragging", function (params) {
            if(self.on_dragging != undefined) {
                self.on_dragging(params)
            }

            params.event = "[original event]";
            this.lastEvent = ['dragging', JSON.stringify(params, null, 4)]
        });
        network.on("dragEnd", function (params) {
            if(self.on_dragEnd != undefined) {
                self.on_dragEnd(params)
            }

            params.event = "[original event]";
            this.lastEvent = ['dragEnd', JSON.stringify(params, null, 4)]
            console.log('dragEnd Event:', params);
            console.log('dragEnd event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
        });
        network.on("zoom", function (params) {
            if(self.on_zoom != undefined) {
                self.on_zoom(params)
            }

            this.lastEvent = ['zoom', JSON.stringify(params, null, 4)]
        });
        network.on("showPopup", function (params) {
            if(self.on_showPopup != undefined) {
                self.on_showPopup(params)
            }

            this.lastEvent = ['showPopup', JSON.stringify(params, null, 4)]
        });

        network.on("hidePopup", function () {
            if(self.on_hidePopup != undefined) {
                self.on_hidePopup(params)
            }

            console.log('hidePopup Event');
        });

        network.on("select", function (params) {
            if(self.on_select != undefined) {
                self.on_select(params)
            }

            console.log('select Event:', params);
        });

        network.on("selectNode", function (params) {
            if(self.on_selectNode != undefined) {
                self.on_selectNode(params)
            }

            console.log('selectNode Event:', params);
        });
        network.on("selectEdge", function (params) {
            if(self.on_selectEdge != undefined) {
                self.on_selectEdge(params)
            }

            console.log('selectEdge Event:', params);
        });
        network.on("deselectNode", function (params) {
            if(self.on_deselectNode != undefined) {
                self.on_deselectNode(params)
            }

            console.log('deselectNode Event:', params);
        });
        network.on("deselectEdge", function (params) {
            if(self.on_deselectEdge != undefined) {
                self.on_deselectEdge(params)
            }

            console.log('deselectEdge Event:', params);
        });
        network.on("hoverNode", function (params) {
            if(self.on_hoverNode != undefined) {
                self.on_hoverNode(params)
            }

            console.log('hoverNode Event:', params);
        });
        network.on("hoverEdge", function (params) {
            if(self.on_hoverEdge != undefined) {
                self.on_hoverEdge(params)
            }

            console.log('hoverEdge Event:', params);
        });
        network.on("blurNode", function (params) {
            if(self.on_blurNode != undefined) {
                self.on_blurNode(params)
            }

            console.log('blurNode Event:', params);
        });
        network.on("blurEdge", function (params) {
            if(self.on_blurEdge != undefined) {
                self.on_blurEdge(params)
            }

            console.log('blurEdge Event:', params);
        });
    }
}

class WordView extends NetworkEvents{

    create(nodeId) {
        /* create the network view on the given element id*/
        var options = {
            nodes: {
                borderWidth: 0

            }
            , edges: {
                shadow:{
                  enabled: false,
                  color: 'rgba(0,0,0,0.5)',
                  size:0,
                  x:5,
                  y:5
                }

                , font: {
                      color: '#CCC',
                      size: 12, // px
                      face: 'Roboto',
                      background: 'none',
                      strokeWidth: 0, // px
                      strokeColor: 'red',
                  }
            }
        }
        let data = this.getData()
        var container = document.getElementById(nodeId);
        var network = new vis.Network(container, data, options);
        this.hook(network)
        return network;
    }

    on_doubleClick(d) {

        for(let word of d.nodes) {
            getWord(word)
        }
    }

    styles(){
        return {
            word: {
                color: '#444'
            }
        }
    }

    start(name){
        this.network = this.create(name);
        bus.$on('message', this.wsMessage.bind(this))
    }

    wsMessage(data) {

        let sent = []
        let tokens = data.data.tokens || [];

        for(let l of tokens) {
            sent.push(l[0])
        }

        this.addWords(sent);

        if(data.data.ident) {
            //this.presentConceptNetResult(data)
        }

        if(data.data.word) {
            this.presentWord(data)
        }
    }

    presentWord(data) {
        let word = data.data.word;
        //this.addWord(word)
        //this.addWords()
        window.word = word
        let value = word.value;
        if(value == undefined) {
            console.warn(`Old data cache does not contain "value" attribte.
                Please delete dictionary file and update the cache.`)
            return
        }

        let iters = ['synonym', 'antonym']
        for (var j = 0; j < iters.length; j++) {
            if(word[iters[j]] == undefined) {
                console.log(`Word "${value}" does not have "${iters[j]}"`)
                continue
            }

            for (var i = 0; i < word[iters[j]].length; i++) {
                this.addRelate(value, word[iters[j]][i], iters[j])
            };
        }

        window.vpr = this
    }

    presentConceptNetResult(data){

        let metas = data.data.ident.meta;

        for(let meta of metas) {
            let end = meta.end.label.toLowerCase();
            let label = meta.rel.label.toLowerCase();
            let start = meta.start.label.toLowerCase();
            if( meta.end.language != 'en'
                || meta.start.language != 'en' ) {
                continue;
            }

            if(meta.weight < 1.4) {
                continue;
            }

            this.addRelate(start, end, label)
            this.addEdge(start, end, label)
        }

        console.log(data.data.type, Object.keys(data.data))
        console.log(data.data)
    }

    addWords(words, edgeLabel) {
        let last;

        for(let token of words) {
            let c = this.addWord(token.toLowerCase())
            if(last) {
                this.addEdge(last.toLowerCase(), token.toLowerCase(), edgeLabel)
            }
            last = token
        }
    }

    nodes(){
        if(this._nodes == undefined ) {
            this._nodes = new vis.DataSet([])
        };

        return this._nodes;
    }

    edges(){
        if(this._edges == undefined ) {
            this._edges = new vis.DataSet([])
        };

        return this._edges;
    }

    addWord(word, color=undefined){
        word = word.toLowerCase()
        let wordColor = this.styles().word.color
        let fontColor = '#DDD';
        if(color != undefined) {
            wordColor = color
            fontColor = '#000'
        }

        if(word[0] == 'a') {
            let _word = word.split(' ').slice(1).join(' ')

            if(_word != '') {
                word = _word;
            }
        }

        if(word.split(' ').length > 1) {
            return this.addWords(word.split(' '), 'derived')
        }

        let nodes = this.nodes();
        let enode = nodes.get(word);
        if(enode != null) return enode;
        return nodes.add({
            id: word
            , label: word
            , color: wordColor
            , font: {
                color: fontColor
                , face: 'Roboto'
            }
            , shape: 'box'

        })
    }

    addEdge(a, b, related='>>') {
        /*
            connect two existing network elements with a arrow line pointing to 'b'
            ww.addEdge('cake', 'window')
         */
        let edges = this.edges();
        related = related.toLowerCase()
        let eedge = edges.get(`${a}${b}`);
        if(eedge != null) return eedge;

        let cmap = colormap[related];
        let cl = cmap;
        if(typeof(cmap) == 'string') {
            cmap = {}
        } else {
            if(cmap != undefined) {
                cl = cmap.color;
            } else {
                console.log(`No color map for ${related}`)
            }
        }

        this.edges().add(Object.assign({
            id:`${a}${b}`
            , from:a
            , to: b
            , color: cl || '#DDD'
            // , value: .1
            , arrows: {
                to: {
                    scaleFactor: .4
                }
            }
            , label: colormap[related] == undefined? related: undefined
            , related: related
        }, cmap))
    }

    addRelate(word, relate, label='relatedTo', color=undefined) {
        /*
            Add a word related to another word, connecting an edge with an
            arrow pointing to relate (B). This will automatically connect existing
            or new elements.
            this.addEdge('cake', 'window')
            this.addRelate('cake', 'hose')
            this.addRelate('dog', 'hose')
            this.addRelate('dog', 'apples')
            this.addRelate('winner', 'chicken')
            addRelate('word', 'other_word', 'label')
         */
        /* append a 'relateTo', a related to b */
        this.addWord(word.toLowerCase(), color)
        this.addWord(relate.toLowerCase(), color)
        this.addEdge(word.toLowerCase(), relate.toLowerCase(), label)
    }

    getData(){

        // create a network
        var data = {
            nodes: this.nodes()
            , edges: this.edges()
        };

        return data;
    }
}

;main();
