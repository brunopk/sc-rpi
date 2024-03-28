import logging
from command import Command
from jsonschema import Draft7Validator
from webcolors import hex_to_rgb
from errors import ParseError, ApiError
from enums import ErrorCode


_logger = logging.getLogger(__name__)


class SectionAdd(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "$defs": {
                "section": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "integer"
                        },
                        "end": {
                            "type": "integer"
                        },
                        "color": {
                            "type": "string",
                            "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"
                        }
                    },
                    "required": ["start", "end", "color"]
                }
            },
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/section"}
                }
            },
            "required": ["sections"]
        }
        self.validator = Draft7Validator(arguments_schema)

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)
        self._test_overlapping([(s['start'], s['end']) for s in self.args['sections']])

    def exec(self) -> dict:
        ids = []
        captured_error = None

        for s in self.args['sections']:
            try:
                color = hex_to_rgb(s['color'])
                color = (int(color[0]), int(color[1]), int(color[2]))
                ids.append(self.hw_controller.new_section(s['start'], s['end'], color))
            except ApiError as e:
                captured_error = e

        # rollback in case of error
        if captured_error is not None:
            _logger.warn('Rollbacking sections.')
            self.hw_controller.remove_sections(ids)
            raise captured_error

        self.hw_controller.render()
        return {'sections': ids}

    def _test_overlapping(self, list):
        """
        Test section overlapping using the merge sort algorithm
        :param list:
        :return:
        """
        if len(list) > 1:
            result = []
            m = len(list) // 2
            l1 = list[:m]
            l2 = list[m:]
            l1 = self._test_overlapping(l1)
            l2 = self._test_overlapping(l2)
            i = 0
            j = 0
            while i < len(l1) and j < len(l2):
                if l2[j][0] <= l1[i][0] <= l2[j][1] or l2[j][0] <= l1[i][1] <= l2[j][1] or \
                        (l1[i][0] <= l2[j][0] and l1[i][1] >= l2[j][1]):
                    raise ApiError(
                        ErrorCode.BAD_REQUEST,
                        "Some sections in the request are overlapping themselves.")
                elif l1[i][1] < l2[j][0]:
                    result.append(l1[i])
                    i += 1
                else:
                    result.append(l2[j])
                    j += 1
            return result + l1[i:] + l2[j:]
        else:
            return list
