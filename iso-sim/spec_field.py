class Field:
    """ Base class for all fields
    """

    def __init__(self, name):
        self.name = name
        self.children = []
        self.bit_position = -1

    def name(self):
        return self.name

    def get_bit_position(self):
        return self.bit_position

    def set_bit_position(self, pos):
        self.bit_position = pos

    def add_child(self, field):
        self.children.append(field)
        field.parent = self

    def add_child_at(self, field, pos):
        field.set_bit_position(pos)
        self.add_child(field)
        field.parent = self

    def parse(self, msg, buf, pos, is_request=True):
        return 0
