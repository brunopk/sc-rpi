class AlreadyOff(Exception):

    def __init__(self):
        self.msg = 'it is already off'

    def get_msg(self) -> str:
        return self.msg
