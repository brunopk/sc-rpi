"""Contains the `IgnoreLokiFilter` class."""

from logging import Filter


class IgnoreLokiFilter(Filter):
    """Filter to avoid infinite loop."""

    def filter(self, record):
      # Ignore logs coming from logging_loki itself
      return not record.name.startswith("urllib3.connectionpool")