The merge grouping initial step returns a list of edges for the top word, and
all top threshold edges for the given word. The result produces two edge lists
(upper,lower, ) through the `weight` threshold.


    Upper:
      word                 weight len   items
    -----------------------------------------
      egg                  -      64    chicken, oval, yolk, white, food, bird, shell, baby ...
      chicken              6.448  87    bird, hen, cross_road, rooster, animal, food, farm, poultry ...
      yolk                 2.455  2     egg, yellow
      white                4.921  3     opposite_of_black, color, colour
      food                 2.0    37    refrigerator, table, kitchen, fridge, oven, supermarket, eaten, cupboard ...
      bird                 4.72   54    animal, flying, sing, wings, tree, flying_animal, nest, sky ...
      shell                2.0    2     ocean, egg
      ...


Clean up references futher by iterating all _top_ of the edge list, find all of high weight
and recursively step through until exausted.

For the initial step, record any primary edges - an edge with a forward reference to the
given word. `egg > shell == 2.0`, and `shell` has `egg` as reference. Same applied for `yolk`.
However `white` does not contain a forward reference to `egg`, therefore it's not a primary.

All primaries: `yolk, shell` etc... are populated in the same method as the original word `egg`.
The same computation is applied to sub-elements, with a reference to the parent graph.

The next step for all values, computing weighted distance through cross-references of primary words.
The `primary->primary` graphs are used as a preliminary weighting bias.
Secondary values such as `chicken`, `bird` etc.. have a reference (`food` and `bird` of `chicken`) are
reweighted whilst populated and checked though the secondary phase.

---



The merging combinator results

+ The root word `egg`
+ edges: The upper/lower initial edge list; `chicken`, `yolk`, `white`, ...
+ Each edge word as a `primary`; any forward reference to the root word: `yolk`, `shell`, etc..
+ Populating the primaries, with their graphs as `primary->primary`
+ Continue populating top X (e.g 50%) weighted of primaries. Until exausted.
+ Test weight of each, walk top edges of these local graphs
+ Compute rolling weights for edges, relative to a root word.

The result produces a tiered set of edges, with primary, lower, dropped etc...
The primary edges apply the best relevence for analysis for the next steps.


## Enrichment

The _naked_ edges only provide best-guess from previously recorded values and does not account for
a 'sentence' of words or session context (other graphs). They should be factored within this.

+ Tokenisation of the sentence
+ Siblings of other words (previous sentences, named graphs, hardcoded training)
+ long-term study

