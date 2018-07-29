The word graph provides concepts of entities and dictionary definitions for each word given. The weighted relationships factor a solution to a best choice for object association.

Not included within the online dataset is an order of sequence for elements:

    one > two > three > four
    country > state > city > town
    okay > good > great > best > fanstastic > awesome

Some are factored through language such as cardinal numbers but most cases require heavy weighting sessions.


At the moment I haven't a solution. Inspecting the current graph we see country, location, city, place and state are all distinct relations. Therefore categorizing these may be performed through relationships up to 3 deep.

I feel utilizing the 'atlocation' for most aspects of decendency will perform the best. Using the standard graph and a reverse standard graph - for every word we produce a graph with a preference to 'atlocation' edges in both directions.

Given the root word 'town' - each edge is inferred 'atlocation' or a top weighted selection for a word.


   village - small_town - town/n - [town] - country - world - solar-system - universe,

At that point the universe is self referencing. With each word a reference to size helps. The 'village' 'hasproperty', 'tiny'. The 'universe' has relations to 'infinite' amongst other _large_ terms.

Graphing numerical order to the indeterminate values such as 'tiny' and 'large' will rely upon graphing each work and discovering antyonms and synonms.

Testing the api I see 'medium' is self-referencing with 'large' as a 'property' to 'big', 'much', and also 'medium. Notably 'few' related to a caridinal value 'three'
