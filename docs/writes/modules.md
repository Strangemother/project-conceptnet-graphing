# A Module

A Module (which is an awful term) defines a subsection of the main context api to manage and maintain IO from all other graphs and modules. Given a graph input a module will _result_ a weight and more graphing; given back to the reference (or parent) graph or calling module.

At the moment the concept of a module has no real definition aside from API properties. A module integration should consist of

+ Isolated work from the main graph
+ Maintain personal graphs with a data reference
+ Can call to and wait for other modules
+ May be async or sync.

Some ideas for modules:

## Reasoning module

A module receiving incomplete or finished graphs from a temporal input or other modules and return the best fit result for all other given results.

Consider a sentence "I own a cat". It's broken into graph constituents and a context of the sentence is applied to memory. The reasoning module accepts the initial phase of the sentence. This is potentially the primary data graphs and meta data such as tokenization or another form of _initial_.

Applying another sentence "I don't like cats" will instigate a weight reasoning and abstraction from the second set of graphs. With the competing sentences the reasoning module calls upon other modules for additional weighting.

A final evaluation of the two sentences produces a vector graph to compute as a response. The evaluation of this response result is also _reasoned_ for validity.


## Personal Reference

For references in the first and third person I feel the best method to resolve the counter-intuitive aspect of 'you' and 'I' is define a single module performing a self-referencing flip on all incoming and outgoing graph results.

The sentence "You are a machine. I am a human" provides two clear statements for graphing however at some point the code should infer 'you' as _my personal context_. This is more complicated for other references such as third person referencing; "I said to him I want you to stay". Without grammar this is a tricky for the system. In our sentence 'you' refers to 'him', the abstract other person.

Therefore the personal reference module will depend upon the nltk tokenizer for non deterministic references. Any discoveries to 'self' are maintained in a Graph dedicated to the systems self identification. In turn using the 'self' graph as an antonym graph for the 'operator' graph


## Operator Reference

The operator is the user/inputer/developer/_you_.

## personal preference

The self referencing persona will maintain a context of preferences. This will consist of a heavily weighted graph answering the reasoning module when questions for _which graph_ arises during word weighting.

In a conceptual question "Do you like cats". I response may be yes, no or some other weighted factor. This overall preference resides within a bank of previously graphed knowledge of _things_ and sentences for experiences.

In a more down-to-earth example, a star-trek door has a preference for being closed, opening if someone says "enter after a bell". This same door should be _automatic_ during selected periods. The personal preference to a query "open or closed" will yield closed unless the environment (another graph) provides a heavier weight for the 'open' graph.

This of course leans towards general learning of previous graphs and heavy recursive analysis of 'hard' training and temporal sentences.

## sequences and preference output

A graph will contain meta data of a final result during a weighting session. The result should be re-graphed and _normalised_ to a graph output for translation. In an example case we tell the system a sequence

    "doors have handles"
    "some handles are round"
    "some handles are straight"
    "most handles in Boston are round"

After this, we can query for a graph weight of "How many handles are round?". The context should denote 'most' and 'some' for a count of handles. A question of _which is greater 'most' or 'some'_. Humans easily apply 'most' and it's more than 'some'. But if Boston is the size of Russia, that sequence is opposite.

The preference of output for which entity in an abstract sequence should be applied. In this case we train _most is more than some_ but the same can be equated through a longer timed graph session.


## queries / questions

Most problematic of all inputs; especially temporal without grammar - is a query the _question_. Applying a query to the context should resolve to a translatable answer. In this study case that would be a preferred graph word:

    "how many legs does a dog have"

will need the pseudo code:

    dog.countof(legs)

The assertions already assign `dog hasa four_legs`. Through a split graph of graph "four legs" yields a `count legs` of four.

This is naturally performed through the context graphing. The reasoning module should store this into an environment sentence list and proceed to recurse for stronger graphs.
Translation of the smaller graph is dependent upon the 'how many.. ?' query - something not picked up by a tokenizer without prompt.

As such an individual module for 'question response' detects a temporal query and will monitor the resolution of the sentence graphs until enough information exists for a successful answer.

The answer consists of an event from the module for any other waiting modules - such as the reasoning module.

To quantify a _complete_ answer ready for output the module performs its own detection of a query type - chunking the string and potentially creating a new tokenization.

The sentence graph (main graph) containing a master context is peppered with some meta data for _this is a query_. Each word is contextualized and re-graphed through any additional contexts chosen by the query graph.

A single context object of 'dog' with an empty slot for _legs, count_ stresses the graph to yield an answer until the slot is filled with a true statement.

Through a bridge to the 'self asserting' module the slot is _asserted_ as the answer for the the waiting question. An 'instant answer' event of some kind should prompt the translation module to convert:

    "how many legs does a dog have"
    dog.countof(legs)
    legs_graph = Graph(dog).has_property_four_legs

    legs_graph['four', 'legs'] > count == 4
    four == number
    dog run legs
    dog.has_property.legs
    dog.has_property.four_legs == legs_graph
    ... so on.

The circular graphing for this is pretty strong - Some work to the sequence module can yield:

    legs > perform > run > feet ...


## self asserting queries

In a set of cases we need the graph to _volunteer_ information:

+ Asserting importance; heavy graphs
+ quantify background knowledge (resolved a heavy graph)
+ Response to queries
+ hard-coded graph responses to tasks


## Hard coded actions

Terming as 'self assembly vocal functions' - at times you require an action to be taken upon the resolution of a graph. the example sentence "open the door" should run a function called `bedroom.door_open()`. This same functionality should be ran through any temporal direction:

    Let me in
    open now
    I want in the house!

Each yielding a weighting towards the bias of 'open' in context to a local graph of an operations house.


# Translation Module

To ground the knowledge further, the internal code simply performs indesing of pre-trained and session trained word values. Given enough relationships - and a bunch of number weighting an object of result is stored into 'current context'.  Usually a object full of tree words is a Graph, but it could be any pythonic object with reference data to the tree.

The result object is a graph with computational results from graphs and module in the session. Once an object is flagged with enough knowledge to quantify a permanency in memory - the translation module can convert it to a real-world output.

In this case a 'translation module' receives or captures input from other modules and converts to an audio response. _Translation_ may be misinterpreted as conversion to another language EN to ES for example but here, the module interprets a graph response or module output to another form such as sentences of words or a servo motor.

In a more down-to-earth scenario when walking through a Startrek door you may say "open the door". This graphs to a result of hard-coded context 'open door'. The translation module will accept the finished result object of 'open door' context and convert it to [Startrek door sound] and physically pulling the door open.

On another case we tell the context-api "Ooh no that's bad". The graph will result in a _negative_ and the translation module converts this to R2D2 style whirling beeps.

----

For our normal example we convert the final result object to a simple stated sentence

    "can I eat eggs"

infers the question is it possible to 'eat', 'egg'. A simple test of the current version shows this is graphed through 'food' and a top result for that is 'eating' and 'eat'.

Therefore the context of this sentence is wholly positive and should be asserted through the translation module by the query module as a positive. The translation module should convert this to a `Graph('positive')` and audio assert the top result.

This value should be graphed through the 'personal preference' in accordance to 'sequential order' of the word 'positive'.

