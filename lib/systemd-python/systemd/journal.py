from logging import LogRecord, StreamHandler


class JournalHandler(StreamHandler):
    def handle(self, record: LogRecord) -> bool:
        return True
