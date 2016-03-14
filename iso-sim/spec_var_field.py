import log_utils
import encoding_helpers
from spec_field import Field
from field_data import FieldData
from parser_exceptions import *


class VariableField(Field):
    """
    This class represents a variable field in message specification. It has all the functions to parse and then
    assemble fields

    Author: Raghavendra Balgi

    """
    log = log_utils.get_logger('spec_var_field')

    def __init__(self, name=None, v_length=None, v_length_encoding=None, encoding=None, nibbles=False):
        Field.__init__(self, name)
        self.v_length = v_length
        self.encoding = encoding
        self.log = VariableField.log
        self.v_length_encoding = v_length_encoding

        # nibbles is True if the length portion signifies nibbles (half bytes) rather than bytes
        # say, 15 for 2 bytes (with one digit for padding)
        self.nibbles = nibbles

    def parse(self, msg, buf, pos, is_request):

        f_len = self.compute_length(buf, pos)
        pos += self.v_length
        if f_len > len(buf) - pos:
            raise FieldParseException('not enough data to parse field -' + self.name)

        data = buf[pos:pos + f_len]

        field_data = FieldData(self)
        field_data.set_data(data)
        self.log.debug('parsing field = {} : field data = {}'.format(self.name, field_data))
        msg.update(self, field_data, is_request)

        # parse children if there are any
        c_pos = pos
        if len(self.children) > 0:
            for child_field in self.children:
                c_pos = child_field.parse(msg, buf, c_pos, is_request)

        return pos + f_len

    def compute_length(self, buf, pos):

        len_buf = buf[pos:pos + self.v_length]

        n = 0
        if self.v_length_encoding == 'ascii':
            n = int(str(len_buf))
        elif self.v_length_encoding == 'ebcdic':
            n = int(encoding_helpers.ebcdic_to_str(len_buf))
        elif self.v_length_encoding == 'bin':
            n = int(encoding_helpers.to_hex(len_buf), 16)
        else:
            n = int(encoding_helpers.to_hex(len_buf))

        if self.nibbles:
            if n % 2 == 0:
                return n / 2
            else:
                return (n + 1) / 2
        else:
            return n
