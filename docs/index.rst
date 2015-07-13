.. ipython-gremlin documentation master file, created by
   sphinx-quickstart on Mon Jul 13 18:24:14 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
ipython-gremlin
===============

A simple `IPython`_ extension for the `Gremlin Server`_ based on `aiogremlin`_.  Works in
both the IPython interpreter and the `Jupyter`_ notebook.

**Check out this example** `IPython notebook`_

Releases
========
The latest release of :py:mod:`ipython-gremlin<gremlin>` is **0.0.4**.


Requirements
============

- Python 3.4
- Tinkerpop 3 Gremlin Server 3.0.0.M9


Dependencies
============
- aiogremlin 0.0.11
- ipython 3.2.1

Installation
============
Install using pip::

    $ pip install ipython-gremlin


Getting Started
===============

Minimal Example
---------------
Submit a script to the Gremlin Server::

    >>> %load_ext gremlin
    >>> %gremlin 1 + 1
    [2]

Contribute
----------

Contributions are welcome. If you find a bug, or have a suggestion, please open
an issue on `Github`_. If you would like to make a pull request, please make
sure to add appropriate tests and run them::

    $ ipython setup.py test

I am particularly interested in adding features that integrate Pandas and NetworkX.
`ipython-cypher`_ has some good examples of this. In the future there will be CI and
more info on contributing.


Contents:

.. toctree::
   :maxdepth: 3

   gremlin


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Github: https://github.com/davebshow/ipython-gremlin/
.. _Gremlin Server: http://tinkerpop.incubator.apache.org/
.. _`aiogremlin`: http://aiogremlin.readthedocs.org/en/latest/
.. _`IPython`: http://ipython.org/
.. _`ipython-cypher`: http://ipython-cypher.readthedocs.org/en/latest/
.. _IPython notebook: https://github.com/davebshow/ipython-gremlin/blob/master/example.ipynb
.. _Jupyter: https://jupyter.org/
