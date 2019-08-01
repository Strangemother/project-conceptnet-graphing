# Long term study of edges

The edge merge splits edge relevence by weight and threshold as they're collected
from db. Edge `primary` edge is scored and kept or dropped for immediate usage and
analysis.
Secondary, lower, and dropped edges for a given word are applied to a background worker -
or rather a FILO queue and analysed in-turn after more-important analysis.
This can be considered as the 'background thoughts' of more expensive graphs. As each
task finished linearly (ignoring the first layer) the same actions occur events. Any
actions or events requiring input are again stored into a forward event planner to act upon
at some point in the future.

This will occur on each edge type independently, referencing all finished information
to a 'named graph'. During `merge::perform>get_edges_words`, apply `lower` and `dropped` to a background queue.
