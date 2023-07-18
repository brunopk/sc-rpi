from command import Command


class Disconnect(Command):

    def __init__(self):
        super().__init__()

    def validate_arguments(self):
        pass

    def exec(self) -> dict:
        pass
