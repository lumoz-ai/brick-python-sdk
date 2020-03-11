import inspect
import os

from . import create

CREATE_COMMAND = "create"
INITIALIZE_COMMAND = "initialize"


class BrickCommandHandler:

    def __init__(self, *, command_line_arguments):
        self.command_line_arguments = command_line_arguments

    def execute_commands(self):
        template_folder = inspect.getfile(self.__class__)
        template_folder = template_folder[:template_folder.rfind("/")]
        template_folder = os.path.join(template_folder, "templates")
        if self.command_line_arguments.command == CREATE_COMMAND:
            create.create(brick_name=self.command_line_arguments.name,
                          set_as_input=self.command_line_arguments.set_as_input,
                          template_folder=template_folder
                          )
        if self.command_line_arguments.command == INITIALIZE_COMMAND:
            create.initialize(brick_name=self.command_line_arguments.name,
                              set_as_input=self.command_line_arguments.set_as_input,
                              template_folder=template_folder
                              )
