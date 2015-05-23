import unittest
from IPython import get_ipython


ipython = get_ipython()
ipython.magic("load_ext gremlin")


class MagicTest(unittest.TestCase):

    def test_line_magic(self):
        result = ipython.magic("gremlin 1 + 1")
        self.assertEqual(result[0], 2)

    def test_session(self):
        ipython.magic("gremlin graph = TinkerFactory.createModern()")
        ipython.magic("gremlin g = graph.traversal(standard())")
        ipython.magic(
            "gremlin g.V().has('name','marko').out('knows').values('name')")
        ipython.magic("session new_session")
        try:
            ipython.magic("gremlin g.V()")
            error = False
        except:
            error = True
        self.assertTrue(error)

    def test_session_get_set(self):
        session = ipython.magic("session")
        self.assertIsNotNone(session)
        ipython.magic("session diff_session")
        diff_session = ipython.magic("session")
        self.assertEqual(diff_session, "diff_session")
        self.assertNotEqual(session, diff_session)


if __name__ == "__main__":
    unittest.main()
