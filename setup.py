import os

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files("./bricksdk/brick_commands/templates")
extra_files += package_files("./bricksdk/proto_store/protos")

setup(
    name='bricksdk',
    version='0.1.0-pre-release',
    description='SDK to create plugable bricks in lumoz.ai',
    scripts=["./bricksdk/brick_commands/brick"],
    url='',
    author='Attinad Software',
    author_email='attinad@attinadsoftware.com',
    license='MIT',
    install_requires=[
        'grpcio',
        'grpcio-tools',
    ],
    packages=['bricksdk',
              'bricksdk.brick_processors',
              'bricksdk.brick_commands',
              'bricksdk.observer',
              'bricksdk.configurations',
              'bricksdk.connectors',
              'bricksdk.connectors.grpc',
              'bricksdk.connectors.grpc.proto_processor',
              'bricksdk.solution_runner',
              'bricksdk.solution_runner.brick_runner',
              'bricksdk.proto_store',
              'bricksdk.proto_store.protos'
              ],
    package_data={'bricksdk': extra_files},
    zip_safe=False
)
