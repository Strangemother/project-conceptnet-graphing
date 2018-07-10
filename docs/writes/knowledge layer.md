# Knowledge layer

The input of string as data input should be split into a contextual layer of connections, and a knowledge connection set in parallel.

The context layer contains the associations and weights of words within the graph. Connections through words will raise and lower a weighting on the context chain. Better context chain weights yield a list of viable sentence structures. Each sentence structure is future weighted and contualized until a resolution yields a winning context.

This occurs asynchronously to output and temporal input, therefore a dynamic tree of viable contexts should be constantly validated.

The knowledge layer is the ‘under’ layer of graphing words, defined as strongly weighted statements to validate against. The knowledge layer is built through three distinct inputs.

Initially hardcoded or operator written instructions define the base of ‘trueims’. These sentences are valid, albeit require a layer of input to justify. A simple sentence ‘operator is human’ is 100% accurate but the sentence requires a binding to ‘is’, another hardcoded statement. Although mandatory, the goal is little to zero hard coded parameters, opting for a _metal layer_ definitions like a seperate api or microcontroller.

This is expanded for deeper contexts with a tighter focus on a context. Semantic weighting is applied as a seperate layer providing assumptions on ‘no’ and other heavy sentiments.

A sentence is broken in small components defining elements to populate the floating context. An immediate net will handle input weighting on full sentences, “the cat sat on the mat”. We [a human] can easily understand the context of this statement. Logically we can break this down to its constituents we’d require for context.

Firstly we see in this case ‘the’ is an identification. I'm assuming a basic tokenizer would define it as a determiner or logical placeholder. In out case it’s in reference to ‘a’ cat. We need to make a leap here and state we can hardcode ‘the == a’, or one item. ‘The door’ ,’the person’ - with a relative context: “a door” _near hear_.
Again conceptually, we have a reference to ‘here’. The knowledge graph connects this to ‘location’, ‘local’... and the first or second layer defines a location being ‘room’, ‘house’ or even less definitively, a context of the local environment.
This model design starts to take shape when given a greater contextual reference. Over time the interconnected graph of associated contexts (through words as objects)  build a tree of agreeable associations, regardless of the context word.’the stuff in my room’ has visible evidence of object continuity given the context of:

The stuff
I’ve concatenated this point, as we can infer ‘a stuff’. This alone makes no sense - however one amount of the context referencing ‘stuff’ can be abstracted.
In
Parameterization of a given entity (in our case ‘stuff’) nearly always requires a location. Nltk tokensation does a great job of detection locatity with reference. Here we can see one ‘stuff’ exists in the incoming location
My
Out of order sequence is expected and is apart of the context api through the graphing. Reference ‘my’ is ownership to the operator. We can infer a hard coded path of ‘my == operator’ for now. Defining ‘operator room’.
Room
A location definition for the entity in context. The ‘room’ is another contextual reference. Which room, whos room - more importantly, what a room is.
This context relys more upon previously conceptualized entities. Building to this requires a slow growth of _room be owned by_ or _can have an operator_

Okay, so the definition of how these words are initially abstracted gives us another - seemly uglier sentence: “one stuff [atlocation] operator [?location]”. Earlier we hardcoded the ‘operator’. The location parameter is hard to define. I don’t believe i've trained ‘room’ yet. However the context connection does have house, location, place - stuff like that. Driving the connection would require a context chain of ‘operator => at => room’ and ‘room => hasa => location’.
These chains are easily defined through graphing. Given the appropriate sentence weight and existing context object _operator_, we’ve got a tenuous link to a location context. Later we remove the ambiguity through a graph weight comparison.

From here we’ll define a context object as CO. Defining a word reference ‘toast’ or ‘door’ or ‘stuff’ with parameters and graph connections to other CO objects. The attributes for a CO are fluid through soft training, but commonly we’d need a location, owner, name… elements we define for a real world object.

Now we can draw the CO required to store the sentence ‘one stuff [atlocation] operator location’. The tokenizer provides a tree [one stuff] atlocation [operator location]. Ignoring recurring tokenization to simplify this further, we can see how this chain evolves  some context objects.
‘Stuff’ is nothing, it has no reference - the graph reveals thin connections needing stripped.essentially it could be an anything… but here our entity is named purely ‘stuff’. As this is a new context there will be no existing ‘stuff’ CO. we can make a new one and name it CO1, giving it an graph name ‘word’. Populating further with reference of ‘count’, a previous branch to ‘one’ is given a largest weight.
Stepping through layered COs for

We’ve focused mostly on very small examples and cheap sentences. This is mostly due to the computational requirements of larger nets. Sentences greater than four words of arbitrary commands tends to graph more than 1000 word references. Converting all this to a CO net is not probable. Instead small contexts kept in local reference, with layered COs dedicated to a reference. To shortcut expensive sentences we can utilize the temporal nature of a CO net by solidifying certain patterns through AI training and hard coding graph chains. Using the following example:

“Turn the light on before I enter”, or perhaps to a child “open the window, but clean up first”. Both sentences are prone to disambiguation

