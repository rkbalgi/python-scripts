import encoding_helpers
import spec_fixed_field


class FieldData:
    def __init__(self, field):
        self.data = None
        self.field = field

    def set_data(self, data):
        self.data = data

    def __str__(self):

        if self.field.encoding == 'ascii':
            return self.data
        elif self.field.encoding == 'ebcdic':
            return encoding_helpers.ebcdic_to_str(self.data)
        else:
            return encoding_helpers.to_hex(self.data)
