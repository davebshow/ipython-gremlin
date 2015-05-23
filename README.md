# ipython-gremlin 0.0.2

###A simple extension for the Gremlin Server based on [aiogremlin](https://pypi.python.org/pypi/aiogremlin/0.0.8). Works in both the IPython interpreter and the jupyter notebook. Requires Python 3.3 with Asyncio or Python 3.4.

[Example notebook](https://github.com/davebshow/ipython-gremlin/blob/master/example.ipynb)

Inspired by [ipython-cypher](https://github.com/versae/ipython-cypher) from @versae

Uses sessions to persist Gremlin across cells.

Example use:

```python
# Load the extension
>>> %load_ext gremlin

# Line magic with %gremlin
>>> %gremlin 1 + 1
[2]

# Cell magic with %%gremlin
>>> %%gremlin
... graph = TinkerFactory.createModern()
... g = graph.traversal(standard())
... g.V().has('name','marko').out('knows').values('name')
...
['vadas', 'josh']

# Store results in a variable using line magic
>>> nodes = %gremlin g.V()
>>> nodes[0]
{'id': 1,
 'label': 'person',
 'properties': {'age': [{'id': 1, 'properties': {}, 'value': 29}],
  'name': [{'id': 0, 'properties': {}, 'value': 'marko'}]},
 'type': 'vertex'}

# Get session id.
>>> %session
'0b9df5a5-7023-4a5a-b16b-def9f02a8a78'

# Change to a new session.
>>> new_session = "my_new_session_id"
>>> %session $new_session
"my_new_session_id"

 # g is not defined so now this will throw error.
>>> %gremlin g.V()
```

### TODO:

* Add support for config options:
  - session control
  - multiple connection management (multiple dbs)
  - connection pooling???

* Add integration with Python scientific libraries, [ipython-cypher](https://github.com/versae/ipython-cypher) has some good examples here.
  - NetworkX
  - Pandas
  - Matplotlib
