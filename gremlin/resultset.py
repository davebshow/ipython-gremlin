import collections
import itertools
try:
    import networkx as nx
except ImportError:
    nx = None
try:
    import pandas as pd
except ImportError:
    pd = None

from gremlin.types import (
    gremlin_types, TypeClasses, Vertex, Edge, VertexProperty, Property, Path)


class ResultSet(list):

    def __init__(self, results, traversal, side_effects=None):
        self._results = results
        self._traversal = traversal
        self._dataframe = None
        self._graph = None
        self._side_effects = None
        super().__init__(results)

    @property
    def side_effect_keys(self):
        if self._side_effects:
            return set(self._side_effects.keys())

    @property
    def side_effects(self):
        return self._side_effects

    @property
    def results(self):
        return self._results

    @property
    def traversal(self):
        return self._traversal

    raw = results

    def _evaluate(self, data):
        evaluated = collections.defaultdict(list)
        for result in data:
            result_type = type(result)
            type_class = gremlin_types.get(result_type, '')
            evaluated[(result_type, type_class)].append(result)
        return evaluated

    def get_dataframe(self):
        """
        Return a :py:class:`pandas.Dataframe` if possible.
        Possiblities:
         - A list of primitives (str, bytes, int, float, bool)
         - A list of graph elements (Vertex, Edge, VertexProperty)
         - A list of lists with the same length
         - A list of dictionaries with the same keys hmmm...
         - A dictionary with values that are lists of the same length or
           dictionaries with the same keys

        :returns: :py:class:`pandas.Dataframe`
        """
        if not pd:
            raise RuntimeError('Please install Pandas')
        if self._dataframe is None:
            evaluated = self._evaluate(self._results)
            keys = list(evaluated.keys())
            num_types = len(keys)
            if num_types > 1:
                raise RuntimeError(
                    'Cannot generate dataframe with mixed results')
            # The preferred scenario
            tp, tc = keys[0]
            values = list(evaluated.values())[0]
            if tc == TypeClasses.PRIMITIVE:
                self._dataframe = pd.Series(values)
            elif tc == TypeClasses.ELEMENT:
                values = [self._dictify_element(v, tp) for v in values]
                self._dataframe = pd.DataFrame(values)
            elif tc == TypeClasses.CONTAINER:
                if len(values) > 1:
                    self._dataframe = pd.DataFrame(values)
                else:
                    # Experimental/untested
                    value = values[0]
                    if tp == dict:
                        dvals = list(value.values())
                        devaluated = self._evaluate(dvals)
                        dkeys = list(devaluated.keys())
                        dnum_types = len(dkeys)
                        if dnum_types > 1:
                            raise RuntimeError(
                                'Cannot convert to dataframe')
                        dtp, dtc = dkeys[0]
                        if dtc == TypeClasses.CONTAINER:
                            self._dataframe = pd.DataFrame.from_dict(
                            value, orient='index')
                        elif dtc == TypeClasses.PRIMITIVE:
                            self._dataframe = pd.DataFrame(value)
                        elif dtc == TypeClasses.ELEMENT:
                            for k, v in value.items():
                                value[k] = self._dictify_element(v, dtp)
                            self._dataframe = pd.DataFrame(value)
                    else:
                        self._dataframe = pd.Series(value)
        if self._dataframe is None:
            raise RuntimeError('Unable to generate dataframe')
        return self._dataframe

    def _dictify_element(self, element, tp):
        if tp == Vertex:
            element = {'id': element.id, 'label': element.label}
        elif tp == Edge:
            element = {'id': element.id, 'label': element.label,
                       'outV': element.outV.id, 'inV': element.inV.id}
        elif tp == VertexProperty:
            element = {'id': element.id, 'label': element.label,
                       'key': element.key, 'value': element.value}
        elif tp == Property:
            element = {'key': element.key, 'value': element.value}
        else:
            raise RuntimeError('Unable to generate dataframe')
        return element

    dataframe = property(get_dataframe)

    def get_graph(self):
        """
        Return a :py:class`networkx.MultiDiGraph` if possible. Works best
        with results representing a list of
        :py:class:`Edge<aiogremlin.gremlin_python.structure.graph.Edge>`
        :py:class:`Path<aiogremlin.gremlin_python.structure.graph.Path>`
        object.

        :returns: :py:class`networkx.MultiDiGraph`
        """
        if not nx:
            raise RuntimeError('Please install NetworkX')
        if not self._graph:
            graph = nx.MultiDiGraph()
            self._graph = graph
            results = self._results
            if len(results) == 1:
                # untested
                if instance(results, dict):
                    results = itertools.chain.from_iterable(results.values())
            evaluated = self._evaluate(results)
            for (tp, tc), values in evaluated.items():
                if tc == TypeClasses.ELEMENT:
                    if tp == Path:
                        for p in values :
                            for e in p.objects:
                                self._add_element(e)

                    else:
                        for e in values:
                            self._add_element(e)
        if not len(self._graph):
            raise RuntimeError('Unable to generate graph')
        return self._graph

    def _add_element(self, e):
        if isinstance(e, Vertex):
            self._add_vertex(e)
        elif isinstance(e, Edge):
            self._add_edge(e)

    def _add_vertex(self, v):
        self._graph.add_node(v.id, {'label': v.label})

    def _add_edge(self, e):
        self._add_vertex(e.outV)
        self._add_vertex(e.inV)
        # import ipdb; ipdb.set_trace()
        self._graph.add_edge(e.outV.id, e.inV.id, e.id,
                             id=e.id, label=e.label)

    graph = property(get_graph)
