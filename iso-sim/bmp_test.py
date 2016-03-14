import struct
import binascii


class Test:
    def __init__(self):

        (self.long_value_1, self.long_value_2) = struct.unpack_from('!QQ', binascii.unhexlify(
            '73000000000000018000000000000001'))
        # self.long_value_2=

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

        print 'shifted ', s_val, 'target ', hex(target_val)
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
            sec_bmp = True

            target_val = self.long_value_2

        s_val = (tmp >> pos)
        target_val |= s_val
        if not sec_bmp:
            self.long_value_1 = target_val
        else:
            self.long_value_2 = target_val

        print hex(self.long_value_1), hex(self.long_value_2)


if __name__ == "__main__":
    t = Test()
    for i in range(1, 129):
        print 'testing ', i, t.is_on(i)
    #t.set_on(127)
    t.set_on(35)
