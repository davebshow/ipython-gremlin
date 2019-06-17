.. ipython-gremlin documentation master file, created by
   sphinx-quickstart on Mon Jul 13 18:24:14 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
ipython-gremlin
===============

`ipython-gremlin` is an `IPython`_ extension module that allows the user to magically
submit scripts to the `TinkerPop Gremlin Server`_ using `%gremlin` (line) and `%%gremlin` (cell)
magic...

`ipython-gremlin` also provides basic integration with `pandas`_ and `NetworkX`_
data/graph analysis libraries to translate Gremlin traversal results to the
data structures commonly used in Python scientific computing.

This work is based on Javier de la Rosa's excellent `ipython-cypher` extension.

**Check out this example** `IPython notebook`_

Releases
========
The latest release of :py:mod:`ipython-gremlin` is **1.0.0**.


Requirements
============

- Python 3.5 +
- TinkerPop 3.2.4


Dependencies
============
- aiogremlin 3.2.4
- ipython 5.3.0

To leverage the full power of :py:mod:`ipython-gremlin`, please install commonly used
scientific computing libraries::

    $ pip install pandas
    $ pip install networkx
    $ pip install matplotlib


Installation
============
Install using pip::

    $ pip install ipython-gremlin


Getting Started
===============

Load the extension::

    %load_ext gremlin

Submit a script to the Gremlin Server::

    %gremlin g.V()

Store query results in a variable::

    verts = %gremlin g.V()

Get a `pandas`_ :py:class:`pandas.DataFrame`::

    verts = %gremlin g.V()
    df = verts.get_dataframe()

Get a `NetworkX`_ :py:class:`networkx.MultiDiGraph` from a collection of elements::

    edges = %gremlin g.E()
    graph = edges.get_graph()

Contribute
----------

Contributions are welcome. If you find a bug, or have a suggestion, please open
an issue on `Github`_. If you would like to make a pull request, please make
sure to add appropriate tests and run them::

    $ ipython setup.py test

I am particularly interested in adding features that integrate Pandas and NetworkX.
`ipython-cypher`_ has some good examples of this.


Contents:

.. toctree::
   :maxdepth: 3

   usage
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Github: https://github.com/davebshow/ipython-gremlin/
.. _TinkerPop Gremlin Server: http://tinkerpop.apache.org/
.. _`aiogremlin`: http://aiogremlin.readthedocs.org/en/latest/
.. _`IPython`: http://ipython.org/
.. _`ipython-cypher`: http://ipython-cypher.readthedocs.org/en/latest/
.. _IPython notebook: https://github.com/davebshow/ipython-gremlin/blob/master/example.ipynb
.. _Jupyter: https://jupyter.org/
.. _pandas: http://pandas.pydata.org/
.. _NetworkX: https://networkx.github.io/
