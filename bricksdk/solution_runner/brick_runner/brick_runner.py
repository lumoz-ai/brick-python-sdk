class BrickRunner:

    def __init__(self, brick_name, brick_config):
        self.brick_name = brick_name
        self.brick_config = brick_config
        self.result = None

    def execute(self, *args, force_rerun=False, **kwargs):
        if force_rerun or self.result is None:
            self.result = "{}({})".format(self.brick_name, kwargs.get("proto", "input"))
        return self.result
