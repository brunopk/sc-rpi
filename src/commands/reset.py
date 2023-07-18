from command import Command


class Reset(Command):

    def __init__(self):
        super().__init__()

    def validate_arguments(self):
        pass

    def exec(self):
        self.controller.remove_all_sections()
        self.controller.render()
