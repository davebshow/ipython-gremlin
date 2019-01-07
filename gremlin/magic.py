"""IPython Gremlin custom magic"""
import argparse
import atexit
import ssl

from traitlets import Unicode, Dict, Float, Bool, Instance
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
                                line_cell_magic, needs_local_scope)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring


from gremlin import config, registry, utils


@magics_class
class GremlinMagic(Magics):
    """
    First of all, keep him out of the light, he hates bright light, especially
    sunlight, it'll kill him. Second, don't give him any water, not even to
    drink. But the most important rule, the rule you can never forget, no
    matter how much he cries, no matter how much he begs, never feed him after
    midnight.
    """

    aliases = Dict(
        config.defaults.aliases, allow_none=True, config=True, help="""
        Aliases for underlying graph
    """)

    bindings = set()

    password = Unicode(config.defaults.password, config=True, help="""
        Password used in SASL authentication
    """)

    response_timeout = Float(
        config.defaults.response_timeout,
        allow_none=True, config=True, help="""
        Timeout for server response
    """)

    ssl_context = Instance(
        klass=ssl.SSLContext, default_value=config.defaults.ssl_context,
        allow_none=True, config=True, help="""
        `ssl.SSLContext` object for SSL
    """)

    uri = Unicode(config.defaults.uri, config=True, help="""
        Default database URI if none is defined inline
    """)

    username = Unicode(config.defaults.username, config=True, help="""
        Username used in SASL authentication
    """)

    use_local_namespace = Bool(
        config.defaults.use_local_namespace,
        config=True,
        help="Whether to load local namespace for each query."
    )

    warnings = Bool(
        config.defaults.warnings,
        config=True,
        help="Whether to enable warning messages."
    )

    @needs_local_scope
    @line_cell_magic('gremlin')
    def gremlin(self, line, cell=None, local_ns=None):
        """I make the illogical logical"""
        local_ns = local_ns or dict()

        if cell is None:
            connection_str = ''
            script = line.lstrip("\n")
        else:
            connection_str = line
            script = cell

        user_ns = self.shell.user_ns
        user_ns.update(local_ns)

        if self.use_local_namespace:

            # private variables have to be registered explicitly in this case
            bindings = utils.sanitize_namespace(user_ns, self.bindings)

        else:

            bindings = {
                k: v for k, v in user_ns.items() if k in self.bindings
            }

        descriptors = utils.parse(connection_str)
        connection = registry.ConnectionRegistry.get(descriptors, self)
        return utils.submit(script, connection, bindings, self.aliases)

    @line_magic('gremlin.close')
    def close(self, line):
        """Explicity close underlying DB connections"""
        registry.ConnectionRegistry.close()

    @line_magic('gremlin.connection.close')
    def close_connection(self, line):
        registry.ConnectionRegistry.close(line)

    @line_magic('gremlin.connection.set_alias')
    def set_connection_alias(self, line):
        """Set alias for specified connection"""
        descriptors = utils.parse(line)
        registry.ConnectionRegistry.set_connection_alias(descriptors, self)

    @line_magic('gremlin.connection.set_current')
    def set_current_connection(self, line):
        """Set specified connection as current"""
        descriptors = utils.parse(line)
        registry.ConnectionRegistry.set_current_connection(descriptors, self)

    @line_magic('gremlin.connection.current')
    def get_current_connection(self, line):
        """Get the currently used connection object"""
        return registry.ConnectionRegistry.current

    @line_magic('gremlin.clean_bindings')
    def clean_bindings(self, line):
        self.bindings = set()

    @line_magic('gremlin.register_binding')
    def register_binding(self, binding: str):
        self.bindings.add(binding)

    @line_magic('gremlin.register_namespace')
    def register_namespace(self, params=''):
        parser = argparse.ArgumentParser()
        parser.add_argument('--allow-private', action='store_true',
                            help="Whether to include private variables.")
        args = parser.parse_args(params.split())

        namespace = self.shell.user_ns
        for var, value in utils.sanitize_namespace(
                namespace, self.bindings, args.allow_private):

            self.bindings.add(var)

    @line_magic('gremlin.remove_binding')
    def remove_binding(self, key: str):
        self.bindings.remove(key)

    @line_magic('gremlin.get_bindings')
    def get_bindings(self, line):
        bindings = self.bindings

        if self.use_local_namespace:

            bindings = utils.sanitize_namespace(
                self.shell.user_ns,
                bindings=bindings
            )

        return bindings


def close():
    """uh oh"""
    print('CLOSING GREMLIN SERVER CONNECTIONS')
    registry.ConnectionRegistry.close()


atexit.register(close)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(GremlinMagic)
