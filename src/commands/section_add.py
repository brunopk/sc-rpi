from command import Command
from jsonschema import Draft7Validator
from webcolors import hex_to_rgb
from error import Overlapping, ParseError, ValidationError, ExecutionError


# noinspection PyShadowingBuiltins
def test_overlapping(list):
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
        l1 = test_overlapping(l1)
        l2 = test_overlapping(l2)
        i = 0
        j = 0
        while i < len(l1) and j < len(l2):
            if l2[j][0] <= l1[i][0] <= l2[j][1] or l2[j][0] <= l1[i][1] <= l2[j][1] or \
                    (l1[i][0] <= l2[j][0] and l1[i][1] >= l2[j][1]):
                raise Overlapping()
            elif l1[i][1] < l2[j][0]:
                result.append(l1[i])
                i += 1
            else:
                result.append(l2[j])
                j += 1
        return result + l1[i:] + l2[j:]
    else:
        return list


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
                            "type": "string"
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
        try:
            test_overlapping([(s['start'], s['end']) for s in self.args['sections']])
        except Overlapping:
            raise ValidationError('section overlapping')

    def exec(self) -> dict:
        ids = []
        error = None

        for s in self.args['sections']:
            try:
                color = hex_to_rgb(s['color'])
                color = (int(color[0]), int(color[1]), int(color[2]))
                ids.append(self.controller.new_section(s['start'], s['end'], color))
            except Overlapping:
                error = ExecutionError('section overlapping')
                break
            except ValueError:
                error = ExecutionError('start > end for some section')
                break

        # rollback in case of error
        if error is not None:
            self.controller.remove_sections(ids)
            raise error

        self.controller.render()
        return {'sections': ids}
