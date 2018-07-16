# Large Graphs Representing an Entire Field

Starting in ab abstract thought - When working with the _context_ of one word - such as "apple" we can derive more than one concept. Building a graph upon a single context
will require temporal knowledge of previous context and the general input (a sentence).

If a person said "I work for Apple I build shopping carts" we can deduce they are a  developer in a _(arguably sort-after)_ programming role building product puchase interfaces. On the contrary "I work with apples making carts" would denote an apple cart maker or some sort of carpenter/joiner.

The two sentences are dependant upon context of the environment - and previously aquired knowledge of a programmers role and the Apple company. Denoting the correct context to continuation is complex through a single graphing space. Dividing graphing knowledge by parental association - such as a field of industry - it's easier to perform weighted reasoning and discover _which context_ is the relevent graph.

In process, a `Graph('developer')` and a `Graph('carpenter')` maintain individual previously trained associations. 'developer' has 'programmer' and 'computing' etc... and 'carpenter' maintains more 'wood-work', 'hand work' etc...

The two graphs bridge through _cart_ or "shopping cart" / "... carts". Simply being the same word is enough to assume an edge connection. During a read procedure 'carpenter' will have a lesser association to 'apple', 'shopping'.

    + 'Apple' _has_ employees
    + 'carpenter' _performs_ ("making") with wood
    + a card _madeof_ wood.

The weights from the above assumed connections defines higher priority for the relevant graph through seperated context graphs. A sentence is weighted by both graphs. Our example graphs `developer` and `carpenter` provide a weighted result for a given sentence to the 'weighting and reasoning module'.

The reasoning module should assess all graphs (in our case 2 of them) for a single string "I work for Apple I build shopping carts". It assess the overall given result value (a overall weight) - the distance to calulcation (still to be done) and some soft of API for its evidence.

The reasoning graph will assess a thinner graph for a goal such as a 'win' value and driven by an ML for semantic reasoning. It will also re-assess parts of a result graph it sees as incomplete; Providing additional _questions_ for a greater graph response. This will include firing requests to modules the result graph does not have access to - such as a sentiment module, a external-sources module etc...

Once the reasoning has applied any additional results to a graph and finalised a weight against all other graphs in this overall context (our two strings). The result is given to the translate, long-term and recursive analysis modules.





