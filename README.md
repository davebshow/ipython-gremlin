# ipython-gremlin 0.0.1

###A simple extension for the Gremlin Server based on [aiogremlin](https://pypi.python.org/pypi/aiogremlin/0.0.8). Works in both the IPython interpreter and the jupyter notebook. Requires Python 3.3 with Asyncio or Python 3.4.

[Example notebook](https://github.com/davebshow/ipython-gremlin/blob/master/example.ipynb)


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

# Change to a new session.
>>> import uuid
>>> new_session = str(uuid.uuid4())
>>> %session $new_session

 # g is not defined so now this will throw error.
>>> %gremlin g.V()
```
