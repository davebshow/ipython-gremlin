import unittest
from IPython import get_ipython

ipython = get_ipython()
ipython.magic("load_ext gremlin")


class MagicTest(unittest.TestCase):

    def test_line_magic(self):
        result = ipython.magic("gremlin 1 + 1")
        self.assertEqual(result[0], 2)

if __name__ == "__main__":
    unittest.main()
