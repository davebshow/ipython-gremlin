import unittest
from IPython import get_ipython

from gremlin.magic import GremlinMagic
from gremlin.registry import ConnectionRegistry
from gremlin.types import Vertex, Edge, VertexProperty
from gremlin.utils import parse


ipython = get_ipython()
ipython.run_line_magic("load_ext", "gremlin")


class MagicTest(unittest.TestCase):

    def test_line_magic(self):
        result = ipython.run_line_magic("gremlin", "1 + 1")
        self.assertEqual(result[0], 2)

    def test_line_magic_with_bindings(self):
        x = 1
        result = ipython.magic("gremlin x + x")
        self.assertEqual(result[0], 2)

    def test_cell_magic(self):
        result = ipython.run_cell_magic("gremlin", "", "1 + 1")
        self.assertEqual(result[0], 2)

    def test_cell_magic_with_uri(self):
        result = ipython.run_cell_magic(
            "gremlin", "ws://localhost:8182/gremlin", "1 + 1")
        self.assertEqual(result[0], 2)

    def test_registry(self):
        result = ipython.run_cell_magic("gremlin", "", "1 + 1")
        self.assertIn("ws://localhost:8182/gremlin",
                      ConnectionRegistry.connections)
        self.assertIn("localhost", ConnectionRegistry.connections)
        conns = list(ConnectionRegistry.connections.values())
        self.assertEqual(len(conns), 2)
        conn = conns[0]
        conn1 = conns[1]
        self.assertIs(conn, conn1)
        conn2 = ConnectionRegistry.get(('', ''), GremlinMagic)
        self.assertIs(conn2, conn)

    def test_set_current(self):
        ipython.run_line_magic(
            'gremlin.connection.set_current', 'ws://localhost:8182/gremlin')

    def test_set_alias(self):
        ipython.run_cell_magic("gremlin", "", "1 + 1")
        self.assertIsNotNone(
            ConnectionRegistry.connections['ws://localhost:8182/gremlin'])
        self.assertIsNotNone(ConnectionRegistry.connections['localhost'])
        ipython.run_line_magic(
            'gremlin.connection.set_alias',
            'ws://localhost:8182/gremlin as sweethost')
        self.assertEqual(
            ConnectionRegistry.connections['ws://localhost:8182/gremlin'],
            ConnectionRegistry.connections['sweethost'])
        self.assertIsNone(ConnectionRegistry.connections.get('localhost'))
        ipython.run_cell_magic("gremlin", "sweethost as test1", '1 + 1')
        self.assertEqual(
            ConnectionRegistry.connections['ws://localhost:8182/gremlin'],
            ConnectionRegistry.connections['test1'])
        self.assertIsNone(ConnectionRegistry.connections.get('sweethost'))
        ipython.run_cell_magic("gremlin", "test1", '1 + 1')
        ipython.run_line_magic('gremlin.connection.set_current', 'test1')

class ParserTest(unittest.TestCase):

    def test_parser(self):
        uri = 'ws://localhost:8182/gremlin'
        alias = 'TestAlias'
        conn_str1 = 'ws://localhost:8182/gremlin as TestAlias'
        conn_str2 = 'ws://localhost:8182/gremlin As TestAlias'
        conn_str3 = 'ws://localhost:8182/gremlin AS TestAlias'
        primary, secondary = parse(uri)
        self.assertEqual(primary, uri)
        self.assertIsNone(secondary)
        primary, secondary = parse(alias)
        self.assertEqual(primary, alias)
        self.assertIsNone(secondary)
        primary, secondary = parse(conn_str1)
        self.assertEqual(primary, uri)
        self.assertEqual(secondary, alias)
        primary, secondary = parse(conn_str2)
        self.assertEqual(primary, uri)
        self.assertEqual(secondary, alias)
        primary, secondary = parse(conn_str3)
        self.assertEqual(primary, uri)
        self.assertEqual(secondary, alias)


class PandasSupportTest(unittest.TestCase):

    def test_cant_get_df(self):
        result = ipython.run_line_magic(
            "gremlin", "g.V().outE().inV().outE().inV().path()")
        with self.assertRaises(RuntimeError):
            result.dataframe

    def test_get_primitive_series(self):
        result = ipython.run_line_magic("gremlin", "[1,2,3,4]")
        sr = result.dataframe
        self.assertEqual(sr.tolist(), [1, 2, 3, 4])

    def test_get_vertex_df(self):
        result = ipython.run_line_magic("gremlin", "g.V()")
        df = result.dataframe
        self.assertEqual(df.id.tolist(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(
            df.label.tolist(),
            ['person', 'person', 'software', 'person', 'software', 'person'])

    def test_get_edge_df(self):
        result = ipython.run_line_magic("gremlin", "g.E()")
        df = result.dataframe
        self.assertEqual(df.id.tolist(), [7, 8, 9, 10, 11, 12])
        self.assertEqual(
            df.label.tolist(),
            ['knows', 'knows', 'created', 'created', 'created', 'created'])
        self.assertEqual(df.inV.tolist(), [2, 4, 3, 5, 3, 3])
        self.assertEqual(df.outV.tolist(), [1, 1, 1, 4, 4, 6])

    def test_get_vertex_prop_df(self):
        result = ipython.run_line_magic("gremlin", "g.V().properties('name')")
        df = result.dataframe
        self.assertEqual(df.id.tolist(), [0, 3, 5, 7, 9, 11])
        self.assertEqual(
            df.key.tolist(),
            ['name', 'name', 'name', 'name', 'name', 'name'])
        self.assertEqual(
            df.value.tolist(),
            ['marko', 'vadas', 'lop', 'josh', 'ripple', 'peter'])

    def test_get_dict_df(self):
        result = ipython.run_line_magic("gremlin", "g.V().valueMap(true)")
        df = result.dataframe
        self.assertEqual(df.id.tolist(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(
            df.label.tolist(),
            ['person', 'person', 'software', 'person', 'software', 'person'])
        self.assertEqual(
            df.name.tolist(),
            [['marko'], ['vadas'], ['lop'], ['josh'], ['ripple'], ['peter']])

    def test_list_of_list_df(self):
        result = ipython.run_line_magic("gremlin", "[[1,2,3,4], [5,6,7,8]]")
        df = result.dataframe
        self.assertEqual(df.ix[0].tolist(), [1, 2, 3, 4])
        self.assertEqual(df.ix[1].tolist(), [5, 6, 7, 8])

    # NEED TO TEST SINGLE OBJECT RETURNS


class NetworkXSupportTest(unittest.TestCase):

    def test_cant_get_graph(self):
        result = ipython.run_line_magic("gremlin", "g.V().valueMap(true)")
        with self.assertRaises(RuntimeError):
            result.graph

    def test_generate_from_vertex_list(self):
        result = ipython.run_line_magic("gremlin", "g.V()")
        self.assertEqual(len(result.graph.nodes()), 6)

    def test_generate_from_edge_list(self):
        result = ipython.run_line_magic("gremlin", "g.E()")
        self.assertEqual(len(result.graph.nodes()), 6)
        self.assertEqual(len(result.graph.edges()), 6)

    def test_generate_from_path_list(self):
        result = ipython.run_line_magic(
            "gremlin", "g.V().outE().inV().outE().inV().path()")
        self.assertEqual(len(result.graph.nodes()), 4)
        self.assertEqual(len(result.graph.edges()), 3)


if __name__ == "__main__":
    unittest.main()
    ipython.run_line_magic('gremlin.close', '')
