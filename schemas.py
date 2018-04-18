import colander


# Cannot use colander.Range because we need greater-then check
class GT:
    def __init__(self, value):
        self._min = value

    def __call__(self, node, value):
        if value <= self._min:
            raise colander.Invalid(node,
                                   'Should be greater than {}'.format(self._min))


class ConfigSchema(colander.MappingSchema):
    Invalid = colander.Invalid

    suits = colander.SchemaNode(colander.Int(), validator=GT(0))
    overbooking = colander.SchemaNode(colander.Int(), validator=colander.Range(0))
