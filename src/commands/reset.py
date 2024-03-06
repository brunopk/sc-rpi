from command import Command


class Reset(Command):

    def __init__(self):
        super().__init__()

    def validate_arguments(self):
        pass

    def exec(self):
        self.hw_controller.remove_all_sections()
        self.hw_controller.render()
