from commands import Command
from controller import Controller


class Disconnect(Command):

    def __init__(self):
        super().__init__()

    def validate_arguments(self):
        pass

    def exec(self) -> dict:
        pass
