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
        self._session = None
        self._processor = ""

    @needs_local_scope
    @line_magic("gremlin")
    @cell_magic("gremlin")
    def execute(self, line, cell="", local_ns={}):
        query = """{}\n{}""".format(line, cell)
        query = query.lstrip("\n")

        @asyncio.coroutine
        def run():
            results = []
            resp = yield from aiogremlin.submit(query, session=self._session,
                                                processor=self._processor)
            while True:
                msg = yield from resp.stream.read()
                if msg is None:
                    break
                if msg.data is not None:
                    results += msg.data
            return results

        return self._loop.run_until_complete(run())

    @line_magic("session")
    def session(self, line=""):
        if line:
            self._session = line
        self._processor = "session"
        return self._session


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(GremlinMagic)
