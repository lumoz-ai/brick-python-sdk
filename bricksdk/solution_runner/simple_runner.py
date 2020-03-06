from copy import deepcopy

from .base_runner import BaseRunner
from .brick_runner.base_brick_runner import TestBrickRunner
from .brick_runner.brick_runner import BrickRunner


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

    def execute_graph(self, inputs, force_rerun=False):
        self.state = self.create_state(inputs)
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
                inner_dependencies = dependency_graph[dependency]
                if inner_dependencies:
                    for inner_dependency in inner_dependencies:
                        result = self.state[dependency].execute(
                            proto=self._execute_brick(dependency_graph=dependency_graph, brick_name=inner_dependency,
                                                      dependencies=self.dependency_graph[inner_dependency],
                                                      force_rerun=force_rerun),
                            force_rerun=force_rerun
                        )
                        results.append(result)
                else:
                    results = [self.state[dependency].execute(
                        force_rerun=force_rerun
                    )]
                if index < len(dependencies) - 1:
                    continue
                results = ", ".join(results)
                result = self.state[brick_name].execute(
                    proto=results,
                    force_rerun=force_rerun
                )
                return result
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
        return self.graph_config.__dict__[brick_name]

    def get_bricks(self):
        bricks = []
        for brick, value in self.dependency_graph.items():
            bricks.append(brick)
        return bricks

    def create_state(self, inputs):
        state = dict()
        bricks = self.get_bricks()
        i = 0
        for brick in bricks:
            runner = BrickRunner(brick_name=brick, brick_config=self._get_config_for_brick(brick))
            if brick in self.input_brick_names:
                runner.proto = inputs[i]
                runner.result = inputs[i]
                i += 1
            state[brick] = runner
        return state
