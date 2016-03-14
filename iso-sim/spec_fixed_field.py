import log_utils
from spec_field import Field
from field_data import FieldData


class FixedField(Field):
    def __init__(self, name=None, length=None, encoding=None):
        Field.__init__(self, name)
        self.length = length
        self.encoding = encoding
        self.log = log_utils.get_logger('spec_fixed_field')

    def parse(self, msg, buf, pos, is_request):

        data = buf[pos:pos + self.length]

        field_data = FieldData(self)
        field_data.set_data(data)
        self.log.debug('parsing field = {} : field data = {}'.format(self.name, field_data))
        msg.update(self, field_data, is_request)

        # parse children if there are any
        c_pos = pos
        if len(self.children) > 0:
            for child_field in self.children:
                c_pos = child_field.parse(msg, buf, c_pos, is_request)

        return pos + self.length
