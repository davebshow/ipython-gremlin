import collections
import enum

from aiogremlin.gremlin_python.structure.graph import (
    Graph, Property, Path, Vertex, Edge, VertexProperty)


TypeClasses = enum.Enum('TypeTypeClasses', 'ELEMENT CONTAINER PRIMITIVE')


gremlin_types = {
    Graph: TypeClasses.ELEMENT,
    Vertex: TypeClasses.ELEMENT,
    Edge: TypeClasses.ELEMENT,
    VertexProperty: TypeClasses.ELEMENT,
    Property: TypeClasses.ELEMENT,
    Path: TypeClasses.ELEMENT,
    list: TypeClasses.CONTAINER,
    dict: TypeClasses.CONTAINER,
    tuple: TypeClasses.CONTAINER,
    set: TypeClasses.CONTAINER,
    str: TypeClasses.PRIMITIVE,
    bytes: TypeClasses.PRIMITIVE,
    int: TypeClasses.PRIMITIVE,
    float: TypeClasses.PRIMITIVE,
    bool: TypeClasses.PRIMITIVE
}
