# Brick Python SDK

Python SDK for creating lumoz bricks.

## Getting Started

### Installation

```bash
$ pip install bricksdk==0.3.21
```

### Create Brick Project

```bash
$ brick create -n brick_name
```

To create an input brick
```bash
$ brick create -n brick_name -i
```

```bash
$ cd brick_name
```

At this point change the configuration to use the input and output protofiles you want to use.

### Download Proto files

```bash
$ brick proto -d
```

### Compile Proto files
```bash
$ brick proto -c
```

Alternatively you can download and compile using the shorthand
```bash
$ brick proto -d -c
```

Note : Go through the TODOs in the code

The brick.processor.BrickProcessor().process method is invoked every time the brick receives a new input. 
The process method in our case acts as the entry point to the brick. 

Add your brick logic to the brick module in the project root.