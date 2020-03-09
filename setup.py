from setuptools import setup

setup(
    name='bricksdk',
    version='0.1.0-pre-release',
    description='SDK to create plugable bricks in lumoz.ai',
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
    package_data={'bricksdk': ['proto_store/protos/*.proto']},
    zip_safe=False
)
