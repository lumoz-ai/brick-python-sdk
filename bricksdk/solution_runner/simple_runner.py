from copy import deepcopy

from .base_runner import BaseRunner
from .brick_runner import BrickRunner


class SimpleRunner(BaseRunner):

    def __init__(self, input_brick_names, output_brick_names, graph_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependency_graph = dict()
        self.graph_config = graph_config
        self.input_brick_names = input_brick_names
        self.output_brick_names = output_brick_names
        self.state = None

    def generate_dependency_graph(self, json_graph=None):
        self.json_graph = json_graph
        output_nodes = self.output_brick_names
        while output_nodes:
            for output_node in output_nodes:
                output_nodes = self._find_parents(output_node)
                self.dependency_graph[output_node] = output_nodes

    def _find_parents(self, node_name):
        parents = []
        for name, value in self.json_graph.items():
            if node_name in value:
                parents.append(name)
        return parents

    def execute_graph(self, force_rerun=False):
        self.state = self.create_state()
        dependency_graph = deepcopy(self.dependency_graph)
        for output_brick_name in self.output_brick_names:
            dependency_graph.pop(output_brick_name)
        for output_brick_name in self.output_brick_names:
            return self._execute_brick(dependency_graph, output_brick_name, self.dependency_graph[output_brick_name],
                                       force_rerun)
        self.state = None

    def _execute_brick(self, dependency_graph, brick_name, dependencies, force_rerun=False):
        results = []
        if len(dependencies) > 1:
            for index, dependency in enumerate(dependencies):
                result = self.state[brick_name].execute(
                    proto=self._execute_brick(dependency_graph=dependency_graph, brick_name=dependency,
                                              dependencies=self.dependency_graph[dependency],
                                              force_rerun=force_rerun),
                    force_rerun=force_rerun
                )
                results.append(result)
                if index < len(dependencies) - 1:
                    continue
                return results
        elif len(dependencies) > 0:
            result = self.state[brick_name].execute(
                proto=self._execute_brick(dependency_graph=dependency_graph, brick_name=dependencies[0],
                                          dependencies=self.dependency_graph[dependencies[0]], force_rerun=force_rerun),
                force_rerun=force_rerun)
            return result
        else:
            result = self.state[brick_name].execute(force_rerun=force_rerun)
            return result

    def _get_config_for_brick(self, brick_name):
        return self.graph_config[brick_name]

    def get_bricks(self):
        bricks = []
        for brick, value in self.dependency_graph.items():
            bricks.append(brick)
        return bricks

    def create_state(self):
        state = dict()
        bricks = self.get_bricks()
        for brick in bricks:
            state[brick] = BrickRunner(brick_name=brick, brick_config=self._get_config_for_brick(brick))
        return state
