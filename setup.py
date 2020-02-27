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
              'bricksdk.configurations',
              'bricksdk.connectors',
              'bricksdk.connectors.grpc',
              'bricksdk.connectors.grpc.proto_processor'],
    zip_safe=False
)
