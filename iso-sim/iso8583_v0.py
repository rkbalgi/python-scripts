import spec
from spec_msg_def import SpecMessageDef
from spec_fixed_field import FixedField
from spec_var_field import VariableField
from spec_bmp_field import BitmapField


class Iso8583v0Spec(spec.Spec):
    def __init__(self):
        spec.Spec.__init__(self, name='Iso8583 v0 - Test')

        msg = SpecMessageDef('Authorization Message - 0100')
        # add all fields
        msg.add_req_field(FixedField(name='Message Type', length=4, encoding='ebcdic'))

        bmp = BitmapField(encoding='bin')

        processing_code = FixedField(name='Processing Code', length=6, encoding='ascii');
        processing_code.add_child(FixedField(name='Transaction Type', length=2, encoding='ascii'))
        processing_code.add_child(FixedField(name='Acct From', length=2, encoding='ascii'))
        processing_code.add_child(FixedField(name='Acct To', length=2, encoding='ascii'))

        bmp.add_child_at(VariableField(name='PAN', v_length=1, encoding='bin', v_length_encoding='bin', nibbles=False),
                         2)
        bmp.add_child_at(processing_code, 3)
        bmp.add_child_at(FixedField(name='Amount', length=10, encoding='ascii'), 4)
        bmp.add_child_at(FixedField(name='Date', length=4, encoding='ascii'), 7)
        bmp.add_child_at(FixedField(name='Time', length=6, encoding='ascii'), 8)
        bmp.add_child_at(VariableField(name='Track II', v_length=3, encoding='ebcdic', v_length_encoding='ebcdic'), 35)
        bmp.add_child_at(FixedField(name='MAC', length=8, encoding='bin'), 64)
        bmp.add_child_at(VariableField(name='Extended Info', v_length=3, encoding='ebcdic', v_length_encoding='ebcdic'),
                         65)
        bmp.add_child_at(FixedField(name='MAC (2)', length=8, encoding='bin'), 128)
        msg.add_req_field(bmp)

        self.messages[msg.name] = msg

        msg = SpecMessageDef('Reversal Message - 0420')
        # add all fields
        msg.add_req_field(FixedField(name='Message Type', length=4, encoding='ebcdic'))
        msg.add_req_field(FixedField(name='Amount', length=10, encoding='ascii'))
        msg.add_req_field(FixedField(name='Pin Data', length=8, encoding='bin'))

        self.messages[msg.name] = msg

        '''
            returns the msg to use based on contents of the buffer
        '''

    def get_msg(self, buf):
        if len(buf) > 4:
            if buf[0:4] == '\xf1\xf1\xf0\xf0':
                return self.messages['Authorization Message - 0100']
            if buf[0:4] == '\xf1\xf4\xf2\xf0':
                return self.messages['Reversal Message - 0100']
            else:
                return None
