#
# Copyright (C) 2023 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from abc import abstractmethod
from networkx import MultiDiGraph
from typing import List, Any

from typedb_graph_utils import NetworkXBuilder
from typedb_graph_utils.data_constraint import DataVertex, ConceptVertex, FunctionCallVertex, ExpressionVertex
from typedb.driver import Entity, Relation, Attribute, EntityType,  RelationType, AttributeType

class VertexStyle:
    def __init__(self, shape, color, label_fn):
        self.shape = shape
        self.color = color
        self.label_fn = label_fn



def _entity_relation_label(vertex: ConceptVertex):
        concept = vertex.concept
        return f"{concept.get_type().get_label()}({concept.get_iid()[-4:]})"

def _attribute_value_as_label(vertex: ConceptVertex):
    concept = vertex.concept
    return f"{concept.get_type().get_label()}({concept.get_value()})"

VERTEX_STYLES = {
    FunctionCallVertex: VertexStyle("s", "grey", lambda x: x.name),
    ExpressionVertex: VertexStyle("s", "grey", lambda x: x.text),

    Entity: VertexStyle("o", "pink", _entity_relation_label),
    Relation: VertexStyle("s", "yellow", _entity_relation_label),
    Attribute: VertexStyle("o", "green", _attribute_value_as_label),

    EntityType: VertexStyle("o", "maroon", str),
    RelationType: VertexStyle("s", "darkyellow", str),
    AttributeType: VertexStyle("o", "darkgreen", str),
}

def _get_attributes(node: DataVertex) -> VertexStyle:
    what = node.concept if isinstance(node, ConceptVertex) else node
    found = [c for c in VERTEX_STYLES.keys() if c and isinstance(what, c)]
    key = found[0] if len(found) > 0 else None
    return VERTEX_STYLES[key]

#
class PlottableGraphBuilder:
    def __init__(self):
        self.edges = []
        self.edge_labels = {}
        self.node_shapes = {}
        self.node_colours = {}
        self.node_labels= {}

    @staticmethod
    def from_networkx(graph: MultiDiGraph):
        self = PlottableGraphBuilder()
        node_attributes = {node: _get_attributes(node) for node in graph.nodes}
        self.node_colours = {node: node_attributes[node].color for node in graph.nodes}
        self.node_shapes = {node: node_attributes[node].shape for node in graph.nodes}
        self.node_labels = {node: node_attributes[node].label_fn(node) for node in graph.nodes}
        self.edge_labels = { (u,v): edge_type for (u, v, edge_type) in graph.edges(data="label")}
        self.edges = [(u,v) for (u, v, edge_type) in graph.edges(data="label")]
        return self
        
    def plot_interactive_graph(self):
        from netgraph import InteractiveGraph
        return InteractiveGraph(
            self.edges,
            edge_labels=self.edge_labels,
            node_shape=self.node_shapes,
            node_color=self.node_colours,
            node_labels=self.node_labels,
            arrows=True,
            node_label_offset=0.075
        )

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from netgraph import InteractiveGraph
    graph_data = [("a", "b"), ("b", "c")]
    node_shapes = { "a" : "o", "b" : "s", "c": "o"}
    plot_instance = InteractiveGraph(graph_data, node_shape=node_shapes)
    plt.show()
