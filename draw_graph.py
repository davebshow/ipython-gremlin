import networkx as nx


def draw_simple_graph(graph, node_type_attr='type',
                      edge_label_attr='weight', show_edge_labels=True,
                      label_attrs=['label'], k=None):
    """
    Utility function to draw a labeled, colored graph with Matplotlib.
    :param graph: networkx.Graph
    """
    lbls = labels(graph, label_attrs=label_attrs)
    clrs = colors(graph, node_type_attr=node_type_attr)
    pos = nx.spring_layout(graph, weight=None, k=k)
    if show_edge_labels:
        e_labels = edge_labels(graph, edge_label_attr=edge_label_attr)
    else:
        e_labels = {}
    nx.draw_networkx(graph, pos=pos, node_color=clrs, arrows=False)
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=e_labels)
    nx.draw_networkx_labels(graph, pos=pos, labels=lbls)


def labels(graph, label_attrs=['label']):
    """
    Utility function that aggreates node attributes as
    labels for drawing graph in Ipython Notebook.
    :param graph: networkx.Graph
    :returns: Dict. Nodes as keys, labels as values.
    """
    labels_dict = {}
    for node, attrs in graph.nodes(data=True):
        label = u''
        for k, v in attrs.items():
            if k in label_attrs:
                try:
                    label += u'{0}: {1}\n'.format(k, v)
                except:
                    label += u'{0}: {1}\n'.format(k, v).encode('utf-8')
        labels_dict[node] = label
    return labels_dict


def edge_labels(graph, edge_label_attr='weight'):
    """
    Utility function that aggreates node attributes as
    labels for drawing graph in Ipython Notebook.
    :param graph: networkx.Graph
    :returns: Dict. Nodes as keys, labels as values.
    """
    labels_dict = {}
    for i, j, attrs in graph.edges(data=True):
        label = attrs.get(edge_label_attr, '')
        labels_dict[(i, j)] = label
    return labels_dict


def colors(graph, node_type_attr='type'):
    """
    Utility function that generates colors for node
    types for drawing graph in Ipython Notebook.
    :param graph: networkx.Graph
    :returns: Dict. Nodes as keys, colors as values.
    """
    colors_dict = {}
    colors = []
    counter = 1
    for node, attrs in graph.nodes(data=True):
        if attrs[node_type_attr] not in colors_dict:
            colors_dict[attrs[node_type_attr]] = float(counter)
            colors.append(float(counter))
            counter += 1
        else:
            colors.append(colors_dict[attrs[node_type_attr]])
    return colors
