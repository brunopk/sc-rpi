from command import Command


class Status(Command):

    def __init__(self):
        super().__init__()

    def validate_arguments(self):
        pass

    def exec(self) -> dict:
        return self.hw_controller.status()
