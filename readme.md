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

Andhoo - I host another server for the client file:

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

+ Distrubuted data storage
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

Through reference this can also be `what color is an animal`.


