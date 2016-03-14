import log_utils
from spec_field import Field
from field_data import FieldData
import struct


class BitmapField(Field):
    def __init__(self, name=None, encoding='bin'):
        Field.__init__(self, name)
        self.name='Bitmap'

        self.encoding = encoding
        self.log = log_utils.get_logger('spec_bmp_field')
        self.long_value_1 = 0
        self.long_value_2 = 0

    def parse(self, msg, buf, pos, is_request):

        # for now, lets just assume we're dealing with a
        # binary bitmap
        sec_bmp = False
        bmp_data = None
        first_byte = struct.unpack_from('!B', buf, pos)[0]

        if first_byte & 0x80 == 0x80:
            sec_bmp = True
            bmp_data = buf[pos:pos + 16]
        else:
            bmp_data = buf[pos:pos + 8]

        field_data = FieldData(self)
        field_data.set_data(bmp_data)
        self.log.debug('parsing field = {} : field data = {}'.format(self.name, field_data))
        msg.update(self, field_data, is_request)
        if not sec_bmp:
            (self.long_value_1) = struct.unpack_from('!Q', bmp_data)
            pos += 8
        else:
            (self.long_value_1, self.long_value_2) = struct.unpack_from('!QQ', bmp_data)
            pos += 16

        # parse children if there are any
        c_pos = pos
        if len(self.children) > 0:
            for child_field in self.children:
                if self.is_on(child_field.get_bit_position()):
                    c_pos = child_field.parse(msg, buf, c_pos, is_request)

        return c_pos

    def is_on(self, pos):

        pos -= 1
        tmp = 0x8000000000000000
        target_val = 0
        if pos <= 64:
            target_val = self.long_value_1
        else:
            pos -= 64
            target_val = self.long_value_2

        s_val = (tmp >> pos)
        if s_val & target_val == s_val:
            return True
        else:
            return False

    def set_on(self, pos):
        print hex(self.long_value_1), hex(self.long_value_2)
        pos -= 1
        tmp = 0x8000000000000000
        sec_bmp = False
        if pos <= 64:
            target_val = self.long_value_1
        else:
            pos -= 64
            target_val = self.long_value_2

        s_val = (tmp >> pos)
        target_val |= s_val
        if not sec_bmp:
            self.long_value_1 = target_val
        else:
            self.long_value_2 = target_val
