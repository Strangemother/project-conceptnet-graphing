For building memory, there seems to be a few core stages

+ initial sentence graphing
+ immediate contextual cross-referencing
+ best fit sentence weighting
+ abstraction for response.

The entire goal of the api should be 'to attain knowledge', allowing more graphing and stronger context connections.

This should be achieved through a process of elimination for sentences (temporal graphed concepts) for a finished context object.

We can consider a _single complete context reference_ as a dictionary of waiting values. The keys to the _abstract_ dictionary are definined and populated through cross referecing graphing.

When graphing fails for a context - a deeper search for context will being. At some point an entropy number should stop this. In forwarding cases, the contextual filling mechanism should be automated, allowing long exposure to an concept graph - with a governing AI driving corrections (adverserial ML network).

## Initial sentences

Each terporal string - we can define as a sentence - keeps a graph of context for a string of associated string; "I like my cat".
The sub word graphing is kept in memory and used for cross-referencing other sentences.

It's more explicitly a 'temporal string' as the information may not strictly be a single sentence. Potentially it's a fuzzy mix of speech to text/ "I like food but I love my cat lets make fish!" is a simple example of three statements and a command. This could be broken into distinct sentences "I like food. But I love my cat. Let us make pasta." - forgive the crummy grammar but it's easier to understand - this is 3 reference trees and 2 sentences in one temporal string.

+ A single temporal string is stord as a base for a context graph
+ storing many context graphs in a sentence list for contact referencing


## Immediate cross-referencing

As a sentence is given, each change to the temporal string should yield a new graphing within the single context reference. For each new graph the weghting should be asserted against all immediate context graphs within the sentence. The winning graph provides the stored abstract of the temporal string and a sentence.

For example: "do this before that" applies a command at the end of the sentence, yielding a complete change of context for the incoming sentence.

Competing graphs would finalise as "do <that>, then <this>". As this is cross-referenced against the immediate tree, `this` and `that` should have context.

If not - an _abstraction for response_ is required.


## Best fit sentence weighting

Each temporal string has a permanent weight and a transient weight per context (or other temporal string). A Temporal string may be broken down into smaller graphs and sub graphs, noting many context objects within a sentence.

For an incoming temporal string, the transient weighing is applied for all given context objects. All other contexts are weight graphed for their potential fit to the given temporal string.
The general winner will be the context with the greatest weight.

Given a string: "I like my dog" then "But I prefer my cat" - will change the given preference of animal to cat over dog.

The first sentence "I like my dog" is a relatively simple statement of preference. This would graph into a Sentence with one statement of intent and 4 sub-graphs (and and recursive graphs). The weighting for "I" LIKE/PREFER "dog" is high.

The next "But I prefer my cat" should naturally assign a greater weight, given 'prefer' is greater than 'like' in an abstract sense. In addition, as this _Sentence_ is _temporally connected_ to the first statement - an antonym weighting "but" should drive the context circuit enough.

With "But" and "prefer" massing a greater weight over "like", "dog" the two distinct sentences (in this case two temporal strings) - the second sentence will change the overall transient state of all graphs, applying the preference as a permanency into the next major context graph.


## Abstraction for Response

Probably the most challenging aspect of the overall design and automated _filling_ of context data. The general goal to 'object' the enviroment context defines some simple requirements per 'object'

A Cup:

* Who owns
* What is
* When was
* Where is
* Why a cup

This WWWWW concept is the initial idea to drive _completion_ of context for a given unit. The naming here helps for readability but to quantify; For a given _thing_ we need to know if it's apart of our environment. We can keep the object in context to our associated _other things_ - mandated _knowledge_ should be "where is it" and "who owns it"

Once operational, we can walk the graph, back-referencing other context objects to infer transient knowledge or request new knowledge.

Requesting new knowledge or **Abstracting** some context from the outbound API and expecting a temporal response relative to this context.


#### Full graph

With full graphing, offering information after a statement yielding an already existing graph of [dog]:

    OP: "I cannot find my dog"
    CTX: "Your dog is in the kitchen"


As the location (Where is) of the dog is loaded into the most recent "dog" context. The 'my dog' yields a subset (of one) dogs to define.


#### Empty Graph


Graphing of a brand new object for reference requires population of sub categories or "context associations" before a "full graph" goal is complete.

With a given temporal input, an immediate dialog persists the Sentence with contextual information about the market. Again simply persisting the WWWWW concept should fill enough graph for contextual referencing

    OP: I went to the market
    CTX: When did you go to the market
    OP: Yesterday
    CTX: Which market
    OP: The local one
    CTX: To buy [produce] fruit


The machine needs a time of 'went' (When), a location (Where) and a reason (Why).

The log displays a fault with the training - where 'fruit' was the top weight for a market. The context graph should refer to any market 'produce' - In later work this should be inferred from a recursive inspection of relative products from an _immediate historic graph_

#### Infer Completion

Through temporal monitoring of an incoming stream, inference of the _next_ expected word - a lot like an AI phone keyboard.

    OP: "My car is" ...
    CTX: a color blue
    CTX: In the car-park

In this case, "My car" has no context, therefore a previous knowledge of a finishing result doesn't exist. Instead from the already cached evaluations of 'car' with context to 'my' - 'is' yields example queries previously used reference strings.

This allows prediction of future conversations and caching potential values for response. With persona referencing "I" and "my" a graph of the OPerator provides a personal attribution.
