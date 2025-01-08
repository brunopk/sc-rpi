from commands import Command


class Status(Command):
    def validate_arguments(self):
        pass

    def exec(self) -> dict:
        return self.controller.status()
