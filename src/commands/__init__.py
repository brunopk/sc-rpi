"""Contains all available commands.

To implement a command:

- It must be implemented in its own module within the commands package.
- It must inherit from `Command` (`src/command.py`) class and be named with the
  camelized version of the module name. For example, if the module is section_add.py,
  the class name should be SectionAdd (the command name will be extracted from the
  module name).
- Copy and re-implement `run` and `validate_arguments` from `Command`.
"""
