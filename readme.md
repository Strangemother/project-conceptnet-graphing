# Context View Reader thing

Render word associations and build context with words
Mostly (now) using conceptnet for word DB. the online DB is wrapped into the
ui and engine.

Each request returns a json to read and parse. Caching provides some fallback.


## run

At the momenet it's a bit scratchy. The requirements.txt provides the install
elements required. They're mostly websockets and nltk.

Quick run on windows

```bash
cd C:\Users\jay\Documents\projects
cd context-api
env\Scripts\activate
context\run.bat &
cd context\src
python main.py

```

## Running tests

nose or pytest or anything is fine. Note my python 3 install doesn't catch pytest.
In the 'database/' smaller tests apply:

    > py -m pytest -sv database/



### Websocket server

start the websocket server for communicating to the UI and coms.

    $> python server/ws.py
       info :: Listen on 127.0.0.1 8009

This is a simple server for echoing JSON across clients.
The web interface will connect to the websocket though the address given through
through the CLI. you can connect a websocket client to this address
to received parse data from the engine.

### Client UI (browser)

The client reader `server/index.html` will read and parse the incoming client
data from the engine. open in the browser - you can simply run the file.

    file://path/to/server/index.html

You can serve this from a python app. A simple socket server will also work.

    $ server/ > python -m http.server
    $ server/ > python -m SimpleHTTPServer

Due to cross-origin domain policies, The server should match the client and
the connecting sockets. It's easy enough to serve it all from localhost or 127.0.0.1
The socket server should host the same address as the client file.

Anyhoo - I host another server for the client file:

    $> server/ > python -m http.server
    127.0.0.1:8000

### Python Engine

Next talk to the main app. It's called the 'engine' because I don't care what it is yet. So it runs stuff - that's an engine.

    $> python -i main.py

---

The main CLI is a loop, sending strings to `assess_string`. Each word is cached for saving api questions to the online conceptnet.

### Command line

A few tools are built into the console input. Normally you'll input words as statements for the context to assess. Apply a command paramter at the start of the string can perform python actions on the running context.

The exclaimation mark `!` at the start of a string will run the string as python.

    What? !__file__

It runs `eval` on the statement, printing the output. It's not a primary  tool, so it's not something to rely upon. However in development, you can utilze this to update running modules without restartingt the cli.

Change a python source module whilst in use - in this example we reload the `secondary_functions` module. We proceed through `primary_functions` reference to this module:

    What? cake
    ... assessing "cake"

    // Alter python source, uppercase the assess log.
    What? !reload(primary_functions.secondary_function)
    <module secondar..>

    What? cake
    ... ASSESSING "CAKE"


The hash or _pound_ symbol `#` (Pound: _£_) will run baked commands built into a python API. For example to delete a word from context:

    What? #delete cake

To stop external API fetching use `#fetch off`. or `#fetch on` to reapply.


### MIT ConceptNet

Some elements are build upon the ConceptNet graph. The online api or a docker box
can be connected.

The docker instance needs to be built. Then accessed through the web-interface
on a booted concept_net_5 docker instance:

    http://192.168.99.100:8007/c/en/hello

Or the remote address:

    http://api.conceptnet.io/c/en/hello


## Notes

This is like version... 5? of Sadie's temporal conceptnet. The loss of the old
net was a hard lesson in temporal storage over distributed data.

+ Temporal data record and parse
+ Soft distribution of context
+ Slow conceptual analysis of spread b-tree / merkle.

Noted research completes most of the components to drive. Over the years (from sadie 3) I've studied a lot of the extra parts. And a lot of the hardare is cheaper.

+ Distributed data storage
+ temporal memory records
+ text to speech
+ speech to text
+ Built in python


## Concept

More write-ups exist in the other docs (and backup notes\*) -

Driving a _concept_ of given entities through slow nanny of word driven object records. Allowing a _conceptual_ references  of objects. The association are easy to build.

Building a reference:

    > the cat is blue
    > blue is a colour
    > a cat is an animal
    ? what colour is the cat
    < blue

Through reference this can also be `what color is an animal` - but this is a very high-level concept of the driving engine.


### The Dream

Alike many humans, I'd like a machine to talk to. This _contextnet_ will (hopefully) drive the temporal memory of context for a relative dialog. Consider you environment and its relative attributes. Or to state again - The room and the stuff in it. We simply understand "that chair" or "the other room". but to derive the understanding of "that chair" you know of "a chair", "my chair" or the abstracted "other [item]". If we have a list of all chairs, and understanding the associations of "my" or "other" - we're done! We have a reference point.

This is a tedious example of my enjoyment with this project. Building a layer of context, driven through _words_ alone. The result is a giant tree of associations being updated by new words.

### Progress

This has been in working progress for nearly 7 years now. By now I considered this idea dead - with the incoming technologies such as deep learning and machine learning. However many years on and trying a bunch of methods - I'm still back on this idea.

Mapping the progress of ideas to show functionality why this may work.


#### First Versions

Version 1 defined a mapping of all communicated words and (essentially) built a spell check dictionary - but this had problems with cross referencing words

I quickly discovered the need for distributed computing with the requirement to cross reference massive lists. In addition the _single core_ concept didn't scale, there one word computed per app cycle is pointless.

Versions 2 and 3 hit the same computational blocks. Memory consumption killed any attempts at referencing small words such as 'tree'. The data-feeds were online corpus, but they did not suite the type of training I wanted.

I needed to learn more about databases, threading, lower-level languages, distributed machinery.


Some years missed, included maths class, AI studies and distributed computing - but the classes didn't help - and getting a job in the field helped.


#### Version 4

With slow nanny training over months/years - I had driven a stable version of the cross referencing context. By carefully communicating to an active b-tree, associations were built upon my (long studied) input word by word.

I feel it cheated as I loaded a lot more trained data via text files for word types for machine understanding - such as "if" and "is". Then they ran independent and _hardcoded_ functionality. I found this ugly, but it did help with short-cutting word relationship management:

After every sentence input, any unknown word was input requested:

    > operator
    < machine
    # machine comment
    // example machine work

    ---

    > I like cake
    # Computing input
    # reference "cake" -
    // Machine input Wiki
    // building concepts into data format b-tree: 159 branches.
    < what is cake?
    > cake is food
    < what is food?
    > food is edible
    # found "edible" reference
    # cake is edible

So with slow input over every word, I carefully mapped out reference chains for word association. It was painfully slow - sometimes taking hours for b-tree referencing.

The b-tree referencing was interesting in itself; by inspecting a wiki - such as a corpus of knowledge from wordnet, all words associated were bound to a weighted tree. Every new word reference was checked against the existing trees for a cross reference. If a match exists, such as "tree > leaves > leaf > green" a weighting core denotes its preferred usage.

Once the machine has scored this path (by distance mostly), higher weighted paths are kept. This is recursive until all paths are exhausted and the winning path denotes a 'true' reference path.

A fully populated tree contains a 'context' session for the entity, such as a 'cake' reference. Some properties are required

    + who - who or what owns the cake. Its spacial reference or owner such as a box
    + what - what is the cake. Its categories such as 'food'
    + where - where is the cake relative to the owner. such as "in" the box.

The machine extrapolates questions to populate this session of information about the referenced cake.

As an example from a previous conversation, in reference to music:

    > operator
    < machine
    # machine comment
    // example machine work

    ---

    > music
    < what is music?
    > music is recreational audio
    < what music is recreational audio?
    > this is rap music
    < is rap music funny?

To understand the depth of the machine questions here - it helps to know what words are loaded and how it asks questions. The operator (me) gave the string "music" knowing the machine has never seen it. This will prompt the query phase.

The machine distinctly asks for "music". The _hardwire_ of this function notes anything after _"what is ..."_ as the variable in question. In return a similar context of "music is" helps mat the answer.

Alternatively changing "music is recre..." with "it's recrea..." - may not have worked due to the inflections and relative position of 'it'. However "this is rap music" I applied knowingly - ensuring the machine enact the _local context_ or relative references local the session; "this".

So which the machine asks "what music is recreational audio" - it already had associations of 'audio' and 'recreational' else those questions would have come first. The entire query requested the a distinction of music and recreational music. And that's a win.

Applying 'rap music', in reference to "this" pushed the 'rap music' into a reference of local determiners "this", "I", "here" etc... so the finished path exists in the references kept for _now_. In addition, applying 'rap' and 'music' defined an association if 'music' again. This will affirm the path when the machine discovers two clean paths to 'rap'.

At this point, the machine cross references the new word 'rap' (with some association to 'music'). Previously a scrap or entry defined rap-music as 'rhythmic beats' or 'rhymes' due a  plural to singular translation map using an off-the-shelf library.

Rhymes can be funny, hence the reference `rap > rhymes > humor > funny`. Again some leaps are taken with the tree steps, but when the data is scrapped, more references to another work gains weight. 'humor' is found against 'rhymes' and 'poem' a lot.

---

The machine attempts to fill a gap with the first solid path it found. Previous training sessions build full models of 'poem' and other such words - they have become strongly weighted nodes in the tree of words through these paths. At this point, the machine affirms or concludes a path based upon operator input.

At this point I can answer in the positive or negative, keeping this path or destroying it.

_At the time, being a metal fan, I laughed at the invention of a funny computer and answered "yes"._






