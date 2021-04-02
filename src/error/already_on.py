class AlreadyOn(Exception):

    def __init__(self):
        self.msg = 'it is already on'

    def get_msg(self) -> str:
        return self.msg
