from .db import AppendableDB, GRow
from collections import Counter


class Edges(object):

    def __init__(self, name):
        self.name = name
        self.items = ()
        self.index = {}

    def add(self, edge_node):
        self.index[edge_node.value] = len(self.items)
        self.items += (edge_node,)

    def __getitem__(self, key):
        return self.items[key]

    def __getattr__(self, word_key):
        return self.items[self.index[word_key]]

    def __repr__(self):
        keys = tuple(str(x) for x in self.items)
        s = '<Edges {} "{}" {}>'.format(len(self.items), self.name, keys)
        return s


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
        return self.walk_back('parent_graph', include_self, from_edgenode)

    def edgenode_chain(self, include_self=False, from_edgenode=None):
        return self.walk_back('parent_edgenode', include_self, from_edgenode, self_item=self)

    def walk_back(self, method, include_self=False, from_edgenode=None, self_item=None):
        edge = getattr((from_edgenode or self), method)
        items = ( (self_item or getattr(self, method) ), ) if include_self else ()
        while edge is not None:
            items += (edge, )
            edge = getattr(edge, method)
        return items

    def pair_chain(self, include_self=False, from_edgenode=None):
        chain_pair = zip(
            self.edgenode_chain(include_self, from_edgenode),
            self.graph_chain(include_self, from_edgenode)
        )
        return tuple(chain_pair)

    def text_chain(self, include_self=False, from_edgenode=None):
        chain = self.pair_chain(include_self, from_edgenode)
        result = ()
        for edge, graph in chain:
            if edge.parent_edgenode is not None:
                nv = edge.parent_edgenode.value
            else:
                nv = edge.parent_graph.key

            result +=( ( nv, edge.edge_type, graph.key, edge.weight),)
        return result

    def __getattr__(self, key):
        return self.graph[key]

    def __repr__(self):
        s = '<EdgeNode({}) "{}":{}>'.format(self.edge_type, self.value, self.weight)
        return s

    def __str__(self):
        s = '{}({}) from "{}"'.format(self.value,self.weight, self.root_graph.key)
        return s


class Graph(object):

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
        self.edges = self.unpack()

    def edge(self, key):
        """Given a string or Graph return the associated edges
        """

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
        s = '<Graph "{}" {} edges of {}>'.format(
                self.key,
                len(self.values),
                tuple(self.edges.keys())
            )
        return s

    def __getattr__(self, key):
        return self.edges[key]

    def __getitem__(self, key):
        return self.edges[key]

    def __len__(self):
        return len(self.edges)


class GraphWalker(object):
    """Additional functions to de-structure inbound data and automatically
    _graph_ the associated keys and edged.

    Calling a key's graph supplies additional walkable graph values to
    path the db values.

        hello > related-to > greeting > related-to > hello ...
    """
    graph_class = Graph

    def add(self, start, edge, end, weight, root=None):
        """Apply a key value with additional values to bind graphing upon callback.
        """
        print("Add: {} ({}) {} {} ({})".format(start, root, edge, end, weight))
        data = GRow(start, edge, end, weight, root)
        self.db.put(start, data, as_dup=True)

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
