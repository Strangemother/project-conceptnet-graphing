import re
import operator
from collections import Counter

from .db import AppendableDB, GRow


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def to_snake_case(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def to_title_case(snake_str):
    res = to_camel_case(snake_str)
    return "{}{}".format(res[0].upper(), res[1:])


class Remap(object):
    """Provide a literal translation of a value to a another prepared value
    for neater internal association of database values:

        # remap CapableOf to ability without DB manipulation
        seeds > CapableOf > grow_flowers
        # to
        seeds > ability > growSeeds
    """
    # Provide a literal key value for word mapping
    # values = ( (MyWord, my_word,), ...)
    values = None

    translator_expose = staticmethod(to_snake_case)
    translator_digest = staticmethod(to_title_case)

    def mapval(self, value, safe=True):
        """Covert a value through the literal translation to another mapped
        value. If safe if true [default] and the value is missing from the
        map, the orignal value is returned.
        """
        dict_values = self._translate_dict_cache()
        res = dict_values.get(value, None)

        if res is None:
            if self.translator_expose is not None:
                return self.translator_expose(value)
            if safe is False:
                raise Exception("Cannot translate string '{}'".format(value))

        if res is None:
            return value

        return res

    def valmap(self, value):
        dict_values = self._translate_dict_cache()
        rev_dict = {y:x for x,y in dict_values.items()}
        res = rev_dict.get(value, None)

        if res is None:
            return self.translator_digest(value)

        return res

    def _translate_dict_cache(self):

        if self.values is None:
            return {}

        if hasattr(self, '_values_dict_cache') is False:
            self._values_dict_cache = dict(self.values)

        if self._values_dict_cache is None:
            return {}
        return self._values_dict_cache

    def _clear_translate_cache(self):
        del self._values_dict_cache
        return True


class EdgeValues(object):
    """Maintain a reference to a key as a hint to the Edge for sorting and value
    extraction.

        db.pick('horse').is_a.weight()
        (1,1,1,1,.4, ...)

    Compatibility for enumeration for sorted and general inspection

        edges = handle.egg.antonym.chicken.capable_of
        ev = edges.weight # edge_values
        # Just the weights:
        ev()
        (1,1,1,1,.4, ...)

        # the edge_node key and weight value
        ev(True)
        (('become_food', 1.0), ('cross_road', 7.746), ('crossing_road', 1.0), (

        # Return the edge, not the key
        ev(True, True)
        (('become_food', <EdgeNode(CapableOf) "become_food":1.0>),

        # value_key=False stops the return of the 'value' attribute from an edgenode.
        # Instead using the _internal key_ 'weight'
        ev(True, True, False)
        ((1.0, <EdgeNode(CapableOf) "become_food":1.0>),
            (7.746, <EdgeNode(CapableOf) "cross_road":7.746>),

    """
    def __init__(self, edges, key):
        self.key = key
        self.edges = edges

    def __call__(self, with_key=False, as_node=False, value_key=True):
        """return a tuple of values of the internal key from every item
        in the associated Edges.

            ev = EdgeValues('weight', edges)
            ev()
            (1,1,1,1)

            ev(with_key=True)
            ('become_food', 1.0), ('cross_road', 7.746), ('crossing_road', 1.0),

            ev()
        """
        res = ()
        items = self.edges._items
        key = self.key
        for x in items:
            attr = getattr(x, key)
            attr_val = attr if as_node is False else x
            if with_key:
                attr_val = (x.value if value_key else attr, attr_val, )
            res += (attr_val, )
        return res

    def sort(self, *keys, **kwargs):
        """Sort and return the edges items using the given one or more key to sort upon.
        If no key is provided, the internal self.key is used.
        If multiple keys are given, multi-sort starting from the left.
        Any additional keyword arguments are given to the sorted() function

            top_5 = handle.egg.antonym.chicken.capable_of.weight.sort(reverse=True)[:5]
            Edges(items=top_5)

        """
        # getter = operator.attrgetter(key or self.key)
        getter_keys = keys if len(keys) > 0 else [self.key]
        getter = operator.itemgetter(*getter_keys)
        return sorted(self.edges._items, key=getter, **kwargs)

    def __repr__(self):
        return "<EdgeValues {} of {}>".format(self.key, len(self.edges))

    def __getitem__(self, index):
        return getattr(self.edges[index], self.key)


class Edges(object):
    """

        sorted(handle.my.related_to, reverse=True)[:5]
        [<EdgeNode(RelatedTo) "he_she":0.469>, <EdgeNode(RelatedTo) "term":0.402>, ...]
        >>> sorted(sorted(handle.my.related_to, reverse=True)[0].graph.related_to, reverse=True)[:4]
        Assuming key search
        [<EdgeNode(RelatedTo) "he_she":0.469>, <EdgeNode(RelatedTo) "term":0.402>, ...]
        >>> sorted(sorted(handle.my.related_to, reverse=True)[0].related_to, reverse=True)[:4]
        Assuming key search
        [<EdgeNode(RelatedTo) "he_she":0.469>, <EdgeNode(RelatedTo) "term":0.402>, ...]
        >>>
    """

    def __init__(self, name=None, items=None):
        self._name = name
        self._items = items or ()
        self._index = {}

    def add(self, edge_node):
        self._index[edge_node.value] = len(self._items)
        self._items += (edge_node,)


    def _text_list(self, weight=False):
        """return a tuple of tuples for text readout of edge_list.

            Edges(items=sorted(gp.edge_list(), reverse=True)[:4])._text_list(True)
        """
        edges = self._items
        if weight:
            return tuple((x.edge_type, x.value, x.weight,) for x in edges)

        return tuple((x.edge_type, x.value,) for x in edges)

    def __getitem__(self, key):
        return self._items[key]

    def __getattr__(self, word_key):
        try:
            return self._items[self._index[word_key]]
        except KeyError:
            """The element does not exist in the index.
            If the key is on the first node item, return an index utility
            for value iteration and sort keys
            """
            if hasattr(self._items[0], word_key):
                return EdgeValues(self, word_key)

    def __repr__(self):
        keys = tuple(str(x) for x in self._items)
        s = '<Edges {} "{}" {}>'.format(len(self._items), self._name or 'NO NAME', keys)
        return s

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):

        if id(self) == id(other):
            return True

        if (self.index == other.index) is not True:
            return False

        if (self.name == other.name) is not True:
            return False

        return True


class EdgeNode(object):
    """An Edgenode has Edge values (type of and weight) with an associated
    end value, such as a word or another entity.
    All calls to the graph proceed from the 'value' end_node. And method
    calls to the edge node pare given to the graph.

        e = EdgeNode('apples', 1, db)
        e.graph
        # > continuation to 'apples' Graph.
    """
    def __init__(self, end_node, weight, graph_db=None, root_graph=None,
                 parent_graph=None, edge_type=None, parent_edgenode=None,
                 additional=None):
        self.value = end_node
        self.weight = weight
        self.graph_db = graph_db
        self._graph = None
        # The originating Graph instance, not strictly the parent.
        self.root_graph = root_graph
        # The graph this edge spawned from
        self.parent_graph = parent_graph
        self.edge_type = edge_type
        self.parent_edgenode = parent_edgenode
        self.additional = additional

    def get_graph(self, value=None):
        if self._graph is None:
            return self.pick(value, root_graph=self.root_graph)

    graph = property(get_graph)

    def pick(self, value=None, root_graph=None, parent_graph=None):
        """Select the given value from the internal graph_db using pick()
        Return a new graph as a child of this edgenode parent_graph.

        If the internal graph_db does not exist, raise an Exception raise
        """
        root_graph = root_graph or self.root_graph
        parent_graph = parent_graph or self.parent_graph
        value = value or self.value
        if self.graph_db:
            graph = self.graph_db.pick(value,
                                       root_graph=root_graph,
                                       parent_graph=parent_graph,
                                       edgenode=self,
                                       )
            return graph
        else:
            raise Exception('No graph_db Database assigned to EdgeNode {}'.format(self.value))

    def graph_chain(self, include_self=False, from_edgenode=None):
        """reutn a list of graph objects to the originating graph using walk_back
        collecting every parent_graph.
        """
        return self.walk_back('parent_graph', include_self, from_edgenode)

    def edgenode_chain(self, include_self=False, from_edgenode=None):
        """Return a list of edgenode instances to the original graph using walk_back
        collecting every parent_edgenode.
        """
        return self.walk_back('parent_edgenode', include_self, from_edgenode, self_item=self)

    def walk_back(self, method, include_self=False, from_edgenode=None, self_item=None):
        """Iterate backward to the instigating graph in memory, calling the given `method`
        for ever back step from this edgenode.
        """
        edge = getattr((from_edgenode or self), method)
        items = ( (self_item or getattr(self, method) ), ) if include_self else ()
        while edge is not None:
            items += (edge, )
            edge = getattr(edge, method)
        return items

    def pair_chain(self, include_self=False, from_edgenode=None):
        """Return a list of paire edgenode and associated graph for every step
        backward to the intrigating graph.
        """
        chain_pair = zip(
            self.edgenode_chain(include_self, from_edgenode),
            self.graph_chain(include_self, from_edgenode)
        )
        return tuple(chain_pair)

    def text_chain(self, include_self=False, from_edgenode=None):
        """Return a list of text tuples for every (word, key, weight) walking
        backward to the instigating graph. This uses pair_chain returning values
        from each discovered edgenode and graph.
        """
        chain = self.pair_chain(include_self, from_edgenode)
        result = ()
        for edge, graph in chain:
            if edge.parent_edgenode is not None:
                nv = edge.parent_edgenode.value
            else:
                nv = edge.parent_graph.key

            result +=( ( nv, edge.edge_type, graph.key, edge.weight),)
        return result

    def match_graph(self, other):
        """
            handle.my.related_to
            >>> a,b=handle.my.related_to[:2]
            Assuming key search
            >>> a.match_graph(b)
            True
        """
        res = False
        if hasattr(other, 'parent_graph') and self.parent_graph is not None:
            res = (self.parent_graph == other.parent_graph
                  and (self.parent_edgenode == other.parent_edgenode) )
        return res

    def match_thin(self, other):
        return (self.value == other.value
                and self.weight == other.weight
                and self.edge_type == other.edge_type )

    def __lt__(self, other):
        if self.match_graph(other):
            other = other.weight
        return self.weight < other

    def __gt__(self, other):
        if self.match_graph(other):
            other = other.weight
        return self.weight > other

    def __lte__(self, other):
        if self.match_graph(other):
            other = other.weight
        return self.weight <= other

    def __gte__(self, other):
        if self.match_graph(other):
            other = other.weight
        return self.weight  >= other

    def __getattr__(self, key):
        return self.graph[key]

    def __getitem__(self, key):
        """subscriptable key fetch from this edgenode only"""
        return getattr(self, key)

    def __repr__(self):
        s = '<EdgeNode({}) "{}":{}>'.format(self.edge_type, self.value, self.weight)
        return s

    def __eq__(self, other):
        if isinstance(other, (str, bytes)):
            return other == self.value

        if isinstance(other, (int, float)):
            return other == self.weight

        if self.match_graph(other):
            return self.weight == other.weight

        if isinstance(other, self.__class__):
            # node to node relation of values as the graphs don't exist.
            return self.match_thin(other)

        return id(other) == id(self)


    def __contains__(self, other):
        for item in edges:
            if item == other:
                return True
        return False

    def __str__(self):
        s = '{}({}) from "{}"'.format(self.value,self.weight,
            self.root_graph.key if self.root_graph is not None else 'NO ROOT')
        return s

    def __hash__(self):
        values = (self.value,
                  self.weight,
                  self.edge_type, )
        return hash(values)


class Graph(Remap):

    edgenode_class = EdgeNode
    edges_class = Edges

    def __init__(self, key, values, db=None, edgenode_class=None,
                 edges_class=None, root_graph=None, parent_graph=None,
                 edgenode=None):
        # The key value as this graphs edge id.
        self.key = key
        # Values collected from the database
        self.values = values
        # A DB to extend the collect self search
        self.db = db
        # The original Graph word to spawn this potential child
        self.root_graph = root_graph
        # The graph producing this graph - usually the immediate - not given
        # to edgenodes.
        self.parent_graph = parent_graph
        # EdgeNode
        if edgenode_class is not None:
            self.edgenode_class = edgenode_class

        if edges_class is not None:
            self.edges_class = edges_class

        self.edgenode = edgenode
        self._values_dict_cache = None
        self.edges = self.unpack()

    def get_values(self, *keys, index=0):
        """Return a list of values for the given keys. If no keya aree given
        return all values.
        Provide an 'index' for the row value index to collect from each item.
        Default is [0], for the first element within the items such as a tuple or GRow
        """

        if len(keys) == 0:
            return self.values

        res = ()
        for item in self.values:
            if item[index] in keys:
                res += (item, )

        return res


    def edge(self, key):
        """Given a string or Graph return the associated edges
        """
        return self.edges[key]

    def edge_list(self):
        """Return a list of edges - rather than `self.edges` returning an object.
        """
        edges = self.edges
        return tuple(y for x in edges for y in edges[x])

    def edge_text(self, weight=False):
        """return a tuple of tuples for text readout of edge_list"""
        edges = self.edge_list()
        if weight:
            return tuple((x.edge_type, x.value, x.weight,) for x in edges)

        return tuple((x.edge_type, x.value,) for x in edges)

    def edge_values(self, weight=False, edge=False, as_tuple=False, sort=None,
        reverse=False, unique=False, return_value=None):
        """Returna tuple of values (words) from all edges ignoring relation type.
        Pass weight=True or edge=True to populate additional attributes
        If weight or edges is true each item returned is a tuple.
        to produce a tuple of one item for each entry (for compatability with
        edge population) provide as_tuple=True.

        list of words: 'word'

            self.edge_values()
            # as tuples of one.
            self.edge_values(as_tuple=True)


        with weight; (word, weight, )

            self.edge_values(True)

        with weight and relation. Tuple order (word, edge_type, weight)

            self.edge_values(True, True)

        sorted by text

            self.edge_values(sort=True)

        sort by weight, returning text only

            self.edge_values(weight=True, sort=(1,0), return_value=0)

        return multi-ordered with weight, unique only:

            self.edge_values(True, sort=(1, 0), reverse=True, unique=True)

        sort by _edge type_ then weight, return a unique list with each return value
        is a different order (word, weight, edge_type, )

            self.edge_values(True, True, sort=(1,2,), unique=True, return_value=(0, 2, 1))

        """
        res = ()
        for _edge in self.edge_list():
            value = _edge.value
            if (weight is True) or (edge is True):
                as_tuple = True

            item = value
            if as_tuple:
                item = (value, )

            if edge:
                item += (_edge.edge_type,)

            if weight:
                item += (_edge.weight, )

            res += (item, )

        if unique:
            res = set(res)

        if sort is not None:
            if sort is True:
                key = None
            else:
                if hasattr(sort, '__iter__') is False:
                    # User passed an int, rather than a multi-order tuple
                    sort = (sort,)
                key = operator.itemgetter(*sort)
            res = sorted(res, key=key, reverse=reverse)

        if return_value is not None:

            sub_res = ()
            if hasattr(return_value, '__iter__') is False:
                return_value = (return_value, )
            caller = operator.itemgetter(*return_value)
            # return a subset of each item.
            for item in res:
                sub_res += ( caller(item), )
            res = sub_res
        return res

    def unpack(self):
        """convert the given values into a walkable tree."""
        result = {}
        root_graph = self.root_graph or self
        for item in self.values:
            start_word, edge_type, end_word, weight, *meta = item
            if (edge_type in result) is False:
                result[edge_type] = self.edges_class(edge_type)
            # EdgeNode
            node = self.edgenode_class(end_word, weight,
                                        graph_db=self.db,
                                        root_graph=root_graph,
                                        parent_graph=self,
                                        edge_type=edge_type,
                                        parent_edgenode=self.edgenode,
                                        additional=meta,
                                        )
            result[edge_type].add(node)

        return result

    def __repr__(self):
        keys = self._string_edge_keys()
        s = '<{} "{}" {} edges of: ({})>'.format(
                self.__class__.__name__,
                self.key,
                len(self.values),
                keys
            )
        return s

    def _string_edge_keys_weights(self):
        s = []
        for x in self.edges.keys():
            s.append("{}({})".format(self.mapval(x), len(self.edges[x])))
        keys = ', '.join(s)
        return keys

    def _string_edge_keys(self):
        keys = self.edges.keys()
        return ', '.join(self.mapval(x) for x in keys)

    def __getattr__(self, key):
        return self.fetch_edges(key, False)

    def fetch_edges(self, key, safe=False):
        """Return a list of Edges using the given key. If self.edges has no
        attribute of 'key', convery it and attempt again.
        Failing to find any key, raise an Attribut.
        """
        try:
            return self.edges[key]
        except KeyError:
            valkey = self.valmap(key)
            try:
                return self.edges[valkey]
            except KeyError:
                pass

        if safe is True:
            return None

        es = 'Graph "{}" edges has no key attribute "{}" or "{}".'
        es += '\n  Available keys: {}'.format (self._string_edge_keys() )
        raise AttributeError(es.format(self.key, key, valkey))

    def get_edges(self, *keys):
        """Return a tuple of edges from the internal list matching the one or
        more keys given.
        """
        res = ()
        for edge in self.edge_list():
            if edge.value in keys:
                res += (edge, )

        return res

    def __getitem__(self, key):
        return self.fetch_edges(key, False)

    def __len__(self):
        return len(self.edges)

    def __and__(self, other):
        """Support graph intersection, returning a new graph consisting of edges
        with matching edges.
        """
        print('AND')
        # discovering the data in this routing:
        # (set(x[1] for x in hi.edge_text()) -  set(x[1] for x in he.edge_text()))
        # List of ordered words - sort by weight, return only word
        ev_kwargs = dict(sort=(1,), return_value=0, reverse=True)
        edges0 = self.edge_values(True, **ev_kwargs)
        edges1 = other.edge_values(True, **ev_kwargs)

        s0 = set(edges0)
        s1 = set(edges1)
        si01 = s0.intersection(s1)
        si10 = s1.intersection(s0)
        # Shared values
        map(si01.add, si10)

        edges = self.get_edges(*si01) + other.get_edges(*si01)

        # Set at 2 because each graph will _start_ with the key word and end with
        # the related edge word. This is position 2 in a GRow relation item
        # ('hello', 'related_to', 'other')
        values_index=2
        # Hmm. A special key combining two graphs?
        key = "{} [&] {}".format(self.key, other.key)

        reversed_values = ( self.get_values(*si01, index=values_index)
                          + other.get_values(*si01, index=values_index) )
        # Due to the index collection here the edges collect will be _backward_.
        # Noting their start word as the original graph start, and the end word
        # as the _edge_ we've collected.
        #

        # Produce a child graph with these edges.

        # something needs to be done here as this is a reverse child graph
        # + The keys a multple
        # + the values are backward.
        # + The edgenode is missing.
        #
        # Pretty messy. This needs to be fixed.
        child_graph = ChildGraph(
            key,
            reversed_values,
            # More than one db?
            db=self.db,
            edgenode_class=self.edgenode_class,
            edges_class=self.edges_class,
            root_graph=self.root_graph,
            # There are two parents?
            # # The parent of the given relation should be given for each
            # graph item.
            parent_graph=self,
            # This should be an internal reference,
            # create now for this new type of association.
            #
            # [update: This should pass the edgenodes leading to this child ?
            edgenode=None
            )

        return child_graph

"""Notes:

Perhaps this should be a CoupledGraph - with the ability to accept
multiple parent_graphs and use them for values and edge search.

Converting the 'parent_graph' to 'parent_graph' - defaulting to 1 parent,
The coupling doesn't need to so a unique class - all graphs have one or more
parents.

This extends to a new type of Edgenode classification for the system only.
Initially they'll be 'child graph edge node relation'. Later this extends
to all type of ML relations including online, live or pre-trained relations.

Therefore we can extend this to a single edgenode owning more than one edge per node.
The edge being the relation may be 'many' (is_a, related_to) resolving to a single node
'greeting'.
A single node may have more or more associated edges. A single node can maintain
a weight per edge reference, with a topological view of other nodes or graphs.

A graph handles the association of many edgenodes to many words (a standard graph pick)
An Edgenode associated the relation type (is_a) to a node word ('greeting').
And edge is a relation to a single node
A node is a single word or a unit of work et the end of a node

A node can render a graph, through `edgenode.graph.is_a...` but a node
_may_ not be attached to any graph to db.
In fact a node could be a single word 'help' with a large number for weights
with a topology of 'emergency' through reference of
[relative] edge (such as `partof` ) to an 'emergency graph' event.

pseudo:

    When Node('help') from edge('partof') through Graph('emergency') > 10 == 'run_func()'

When two graphs intersect in some way, it may produce

    a coupled graph, for a child of associated edges and many parents
    a new graph with the original graph as a parent through a relation.

---

A node may react to an event though another graphs _awakening_ of associated nodes or graphs.
In addition event modules may capture other graphs or events to populate 'help' and 'emergency'
detection. A node may optionally react with an event, applying weight to the 'run_graph' function
and general context [of emergency].

"""


class ChildGraph(Graph):
    """A Child graph spawns from working directory with a graph, producing a result
    qualifying for its own graph, such as a Graph & Graph intersection.
    A child graph acts like a normal graph for usage, but historical walking
    will step to the parent graph.

        + Given values (if any) may be reversed, applying the parent graph as the
            instigator
        + The values are edgenodes leading to this graph.
        + values (relations) may be duplicated

        + the edgenode may not exist, therefore a generated Edgenode associating
            this graph as a child should be created
        + More than one originating key; Leading to this child graph maintaining
            more than one parent.
    """
    pass


class Edge(object):
    """This class (to be renamed) associated the starting edge to  walkable unit
    providing a cleaner interaction with the graph walker.

        handle = Edge(db).apples.capable_of
    """

    def __init__(self, graph_db):
        self.graph_db = graph_db

    def __getattr__(self, key):
        if hasattr(self.graph_db, key):
           return getattr(self.graph_db, key)

        print('Assuming key search')
        return self.graph_db.pick(key)


class GraphWalker(object):
    """Additional functions to de-structure inbound data and automatically
    _graph_ the associated keys and edged.

    Calling a key's graph supplies additional walkable graph values to
    path the db values.

        hello > related-to > greeting > related-to > hello ...
    """
    graph_class = Graph

    def add(self, start, edge, end, weight, root=None, **kwargs_additional):
        """Apply a key value with additional values to bind graphing upon callback.
        """
        save = True
        if 'save' in kwargs_additional:
            save = kwargs_additional['save']
            del kwargs_additional['save']

        data = GRow(start, edge, end, weight, root, **kwargs_additional)
        self.db.put(start, data, as_dup=True, save=save)

    def bind(self, key, db, through=None, relation=None):
        """Bind a db relation to a key within this db for automatic
        graph binding.
            bind()
        """
        through = through or db.name
        relation = relation or key

        print ('Key "{}" > {} Graph({})'.format(key, through, relation))

    def pick(self, key, root_graph=None, parent_graph=None, edgenode=None):
        """select a key from the database using 'collect' and return a Graph
        populated with the db values.
        Provide a root graph as the original caller for the chain.
        Allow default None to spwan a graph as its own root - further nodes and graphs
        will receive the given graph instance as the root graph..
        """
        raw_values = self.db.collect(key)
        """ Combine all the given values into a graph for user walking"""
        # Graph
        graph = self.graph_class(key, raw_values,
            db=self,
            root_graph=root_graph,
            edgenode=edgenode,
            parent_graph=parent_graph)
        return graph


class ObjectDB(GraphWalker):
    """Mimic a GraphDB to work with the same format of data without a database
    connection. This is essentially a drop-in replacement for a Graph, and
    may be used as an attenuates connection graph or an in-memory static graph
    loaded from data.
    """
    def __init__(self,   name=None, load=None):
        self.name = name
        self.db = self
        self.encode =  GraphDB(auto_open=False).encode
        self.decode =  GraphDB(auto_open=False)._convert_out
        self.index = {}
        self._data = ()

        if (name is None) and (load is not None):
            self.load(load)

    def collect(self, key):
        return [self.decode(self._data[x])for x in self.index.get(key, ())]

    def get(self, word):
        return self.collect(word)[0]

    def wipe(self):
        self._data = ()

    def iter(self, **kw):
        for key in self.index:
            for index in self.index[key]:
                yield key, self._data[index]

    def put(self, key, value, encode=True, **kw):
        # def put(self, key, value, save=True, encode=True, encode_key=True,
        #     as_dup=None, **kwargs):
        if (key in self.index) is False:
            self.index[key] = ()
        self.index[key] += (len(self._data), )
        self._data += (self.encode(value) if encode else value,)

    def start(self, **kw):
        self.db = self
        super().start(**kw)

    def load(self, data):
        """Load an object into the internal data, utilizing create_index() if
        the 'index' key does not exist. Antithesis of dump()."""
        self.name = data.get('name', None)
        self._data = data.get('values', None)
        self.index = data.get('index', self.create_index(self._data))

    def dump(self, with_index=True):
        """Return the internal data as an object for digest through transport
        or storage."""
        result = {'name': self.name, 'values': self._data }
        if with_index:
            result['index'] = self.index
        return result

    def create_index(self, data):
        """Given a list of data for usage within the _data, return a new
        index."""

        counter = 0
        index = {}
        for item in data:
            row = self.decode(item)
            key=row[0]
            if (key in index) is False:
                index[key] = ()
            count = counter
            index[key] += ( count, )
            counter += 1
        return index


class GraphDB(AppendableDB, GraphWalker):
    # graph_class = Graph
    def start(self, **kw):
        self.db = self
        super().start(**kw)
