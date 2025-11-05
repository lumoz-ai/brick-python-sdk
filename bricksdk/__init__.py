from .base_brick import BrickFactory, Brick


def get_brick():
    brick = Brick()
    if brick.configuration is None:
        raise Exception("Initialize brick with brick factory before using get brick")
    return brick
