from .base_brick_runner import BaseBrickRunner


class BrickRunner(BaseBrickRunner):

    def _execute(self, *args, force_rerun=False, **kwargs):
        return "{}".format(self.brick_name)
