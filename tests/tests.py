import unittest
from IPython import get_ipython

ipython = get_ipython()
ipython.magic("load_ext gremlin")


class MagicTest(unittest.TestCase):

    def test_line_magic(self):
        result = ipython.magic("gremlin 1 + 1")
        self.assertEqual(result[0], 2)

    def test_session(self):
        ipython.magic("session '81b78527-4c12-49bc-ad4f-3861a9529f31'")
        ipython.magic("gremlin graph2 = TinkerFactory.createModern()")
        ipython.magic("gremlin g2 = graph.traversal(standard())")
        nodes = ipython.magic("gremlin g2.V()")
        self.assertEqual(len(nodes), 8)
        ipython.magic("session 81b78527-4c12-49bc-ad4f-3861a9529f32")
        try:
            ipython.magic("gremlin g2.V()")
            error = False
        except:
            error = True
        self.assertTrue(error)

    def test_session_get_set(self):
        ipython.magic("session 81b78527-4c12-49bc-ad4f-3861a9529f32")
        session = ipython.magic("session")
        self.assertEqual(session, "81b78527-4c12-49bc-ad4f-3861a9529f32")
        diff_session = ipython.magic("session 81b78527-4c12-49bc-ad4f-3861a9529f33")
        self.assertNotEqual(session, diff_session)


if __name__ == "__main__":
    unittest.main()
