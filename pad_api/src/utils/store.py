from rdflib import BNode
from rdflib import Dataset
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from utils.namespace import PADNamespaceManager


def bnode_to_sparql(node):
    if isinstance(node, BNode):
        return f"<bnode:b{node}>"
    return node.n3()


def sparql_store(query_endpoint) -> Dataset:
    db = SPARQLStore(
        node_to_sparql=bnode_to_sparql,
        query_endpoint=query_endpoint
    )
    graph = Dataset(store=db)
    graph.namespace_manager = PADNamespaceManager()
    return graph
