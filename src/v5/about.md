## Reboot

The date is 21 July 2019 and this is (if even) version 5 of the context net.
Currently version 3 works with version 4 as a conceptual prototype to structure.

The rebuild warrents a year of alternative study and a clearer definition of output.
Fundamentally the old (current) code isn't readable, due to the mixed structure approach.
As such, the new concept should allow an easier learning curve for picking-up the
project.


---

This write-up is a more-formal write-up of the idea, combining the previous data and concepts
with newer study. The fundamental project changes will encompass:

+ Forget the initial 'modular' structure in the persuit of a great "lib"
    I intend to use the cleanest _written_ libs, to make is super easy to pickup.
    For example a db layer in django is extremely readable. And with no need to
    build libraries of stitching code or glue it's easy extend.
+ forgoe speed for clarity
    finding the fastest method is good, but I keep finding a better method. Therefore
    I give up and instead use a clean adapter I'll delete layer when fully functioning.
+ less ML, more data
    through clever data structures I can achieve a lot of the requirements without black box magic.
    Having a fully ML context machine is hard to evaluate and retrain.
    Instead I'm opting for very thing 'glue' layers to formluate edges of the sentence graphs: case: Stattrek-list.


## Primitive layout

The basic premise: Convert sentences to objects, graph objects to provide associative _context_
in relation to a sentence or a session of conversation.
_Working with the data over these years, I see a lot of this can be done with clever data indexing (db)
and lots of async graphery._

### Input Layer

Any sensory input, predominantly textual and intially text and verbal input/output.
The TTS and STT are already done through standard SAPI and web-tech, so this is a arbitrary step.

The context api should handle temporal particles, therefore the input stream shouldn't matter.
For the _doorbell_ project, it's shown any IO is credeble given the correct training.

+ Receive external signals, streams, texct etc..
+ Pass the the next layer as a source to _split_ as particles.

Text format:
```
> CLI: Show me page six and extract my favorite word.
< send to layer "Show me page six and extract my favorite word."
```

### Layer 1: Temporal Particles

Split incoming temporal streams into congizent chunks for the _sentences layer_.
As input is received, the slicing or _selection_ of data is structured for the next layer.

With text this is easy, each temporal particle is just an input word or sentence. With
voice it's slightly tricker however I consider it a complex tokensation problem given to
NLTK to tokensizer. I feel the hard part may be applying (or extracting) grammer from
unstructured streams to single ledgible items.

For now I can focus on simple training sentences, and I hope to pick up a ready-to-use ML
tagging lib...

+ Receive unstructured (but formatted) information from input layers
+ Break down the streams in particles (chunks) of single units to identify (word tags).
+ Send to a 2D graphing layer for contextual abstraction

```
> "Show me page six and extract my favorite word."
< send ["Show" "me" "page" "six" "and" "extract" "my" "favorite" "word", "."]
```

Or maybe even sub particle breakdown

```
< send [ ["Show" "me" "page" "six"] "and" ["extract" "my" "favorite" "word", "."] ]
```

## Layer 1.5: 2D Ledger (Sentence Grouping)

For the first (real) layer, the sentences are a session of lists, defining a group
of messages in context. Consider asking a machine to book a flight, each input sentence
is a single entity within a conversation list.

For each incoming particle-set, apply to the correct context session (the current one)
and study each element (a word token) for cross-reference knowledge.
Given we have the word "in the other room",
the context should define association for "other" and "room". It should consider
the history of a session, contexts from other sessions and generally populate the
words _as much as possible_ to define a solution to _what_ is the "other room".

We should think of it as a flat graph - using a nice and easy example

    [
        > "turn on the TV",
        < ??,
        > "in the other room",
    ]


In the middle `< ??` our output, must quantify more context for the session, we'll
ignore it for now. The "Turn on TV" is the action to perform in the "other room" and
for now, the focus on contextually defining 'other'.

_Note: The leap here defines the pre-trained "room", being a standard object for an
environment, we don't need to build a deeper contextual graph - other than 'where'.
Given this example assumes a standard installation, the room list() is a lookup for
defining the name "other". If the room was "bedroom" - this wouldn't be a challenge :p._

As "other" isn't a named entity it should be "contextually graphed", i.e information
regarding the word "other" should be stored into memory as it's own _thing_ graph.


+ A list of unit entities for session - _lists of sentences, containing 'word' units to reference._
+ A sentence session for each unit of work - _almost like a a log group per conversation_
+ A cross-reference instigator for knowledge gaps - _define previously unscanned elements providing data for all words -
+ A place of reference for _starting_ a graph analysis. - _scanning for previously known words and sentences_


Fundamentally this layer converts unstructured sentences and value data into knowledge chunks, ready to
'contextualise' and cross reference.

## Layer 2: Cross referencing

_The overall goal for the context-api maintains a state of "context" for a word or phrase within an overall session.
Each word may have its own context, assisting the population of other nodes within the graph"_.

Each word in a given sentence has a graph of associations within a boundry of language in addition to local context.
The underyling laguage prodvides relationships for words. For each words we define a starndard knowedge base and an
extended context knowledge base.

    "this is my dog"

The example sentence provides an association to the relative entity "this" and 'dog' with bridges to ownership and identity.
The contextapi will populate the edges and leafs.
