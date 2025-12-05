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

from typedb.analyze import Pipeline
from typedb.driver import ConceptRow
from typedb_graph_utils import NetworkXBuilder
from typing import List

def visualise(rows: List[ConceptRow]):
    if len(rows) > 0:
        pipeline = rows[0].query_structure()
        if pipeline is None:
            raise ValueError("rows must have query_structure. Use 'include_query_structure=True' in QueryOptions")
        builder = NetworkXBuilder(pipeline)
        for (i, answer) in enumerate(rows):
            builder.add_answer(i, answer)
        graph = builder.finish()
    else:
        from networkx import MultiDiGraph
        graph = MultiDiGraph()
    from .answer import PlottableGraphBuilder
    visualiser = PlottableGraphBuilder.from_networkx(graph)
    visualiser.plot_interactive_graph()
