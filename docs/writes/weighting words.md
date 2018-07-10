 Weighting words

Due to the nature of a contextnet single words provide no weighted context within a graph without context. Take the word “food” as an input value. It provides no relevance to a situation or cnext. Without previous input, this statement is considered a _shout in the street_. However when used in context: “What do you need?”, “food.” - it contains a sense of urgency.

To apply this to weighting, a single word defines knowledge without weighting. Given some context, a word can be weighted. Given any context the system should weight the word against all viable context objects.

The weight value does not have defined limits as its final value will depend upon the complexity of the context and the maturity of an existing dataset. Any weights defined through context chaining will provide a numerical value to store against a given sequence of words. A sentence: such as “I need food” contains more contextual weight than “I like food”, furthermore the context “give food” contains less context to weight (devoid of “I”) but should yield a heavier weight as there is a machine action to perform.

If we relied on knowledge weighting alone, we’d see a lesser weight for the sentence “give food” because of its lack of input nodes to weight.
