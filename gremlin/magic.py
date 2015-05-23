import asyncio
import uuid

import aiogremlin

# from IPython.config.configurable import Configurable
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                needs_local_scope)
# from IPython.utils.traitlets import Int, Float, Unicode, Bool


@magics_class
class GremlinMagic(Magics):
    """Provides the Gremlin magic. This will be configurable etc. (eventually)
    """
    def __init__(self, shell):
        super().__init__(shell)
        self._loop = asyncio.get_event_loop()
        self._pool = aiogremlin.WebSocketPool("ws://localhost:8182/",
                                              loop=self._loop)
        self._session = str(uuid.uuid4())

    @needs_local_scope
    @line_magic("gremlin")
    @cell_magic("gremlin")
    def execute(self, line, cell="", local_ns={}):
        query = """{}\n{}""".format(line, cell)
        query = query.lstrip("\n")

        @asyncio.coroutine
        def run():
            results = []
            with (yield from self._pool) as conn:
                client = aiogremlin.GremlinClient(connection=conn,
                                                  processor="session",
                                                  loop=self._loop)
                resp = yield from client.submit(query, session=self._session)
                while True:
                    mssg = yield from resp.stream.read()
                    if mssg is None:
                        break
                    results += mssg.data
            return results

        return self._loop.run_until_complete(run())

    @line_magic("session")
    def session(self, line=""):
        if line:
            self._session = line
        return self._session


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(GremlinMagic)
