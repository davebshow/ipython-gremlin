"""Utility functions to support GremlinMagic operations"""
import asyncio
import json
import re
import sys

from gremlin_python.driver import request
from gremlin import config, registry, resultset


_IPYTHON_VARS = {'In', 'Out'}


def parse(connection_str):
    """Parse connection string passed by user"""
    if ' as ' in connection_str.lower():
        descriptors = re.split(' as ', connection_str,  flags=re.IGNORECASE)
    else:
        descriptors = (connection_str, None)
    return descriptors


def sanitize_namespace(user_ns, bindings=None, allow_private=False):
    bindings = bindings or dict()
    namespace = dict()

    for k, v in user_ns.items():

        try:
            json.dumps(v)
        except Exception as exc:
            if config.defaults.warnings:
                print("[WARNING] Serialization of object `{obj}` failed. Skipping.".format(obj=k),
                      exc, file=sys.stderr)
            continue

        # pop ipython vars (if they are not overridden by user)
        if k in _IPYTHON_VARS and k not in bindings:
            continue

        if k.startswith('_') and not allow_private:
            if k in bindings:
                namespace[k] = v
            else:
                continue

        namespace[k] = v

    return namespace


def submit(gremlin, conn, bindings, aliases):
    """
    Submit a script to the Gremlin Server using the IPython namespace
    using the IPython namespace to pass bindings using Magics configuration
    and a connection registered with
    :py:class:`ConnectionRegistry<gremlin.registry.ConnectionRegistry>`
    """
    message = request.RequestMessage(
        processor='', op='eval',
        args={'gremlin': gremlin, 'aliases': aliases, 'bindings': sanitize_namespace(bindings)})
    return asyncio.run_coroutine_threadsafe(_submit(conn, message), registry.LOOP).result()


async def _submit(conn, message):
    result_set = await conn.write(message)
    results = await result_set.all()
    return resultset.ResultSet(results, message)
