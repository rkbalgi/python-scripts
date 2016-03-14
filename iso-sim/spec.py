class Spec:
    """Base class for all message specifications"""
    all_specs = dict()

    def __init__(self, name, is_bitmapped=True):
        self.name = name
        self.messages = dict()
        self.is_bitmapped = is_bitmapped

    def name(self):
        return self.name

    def parse(self, buf, is_request=True):

        msg_def = self.get_msg(buf)
        if is_request:
            msg = msg_def.parse_request(buf)
        else:
            msg = msg_def.parse_response(buf)
        return msg

    def get_msg_by_name(self, msg_name):
        print self.messages
        return self.messages[msg_name]

    @staticmethod
    def register_spec(spec):
        Spec.all_specs[spec.name] = spec

    @staticmethod
    def get_spec(name):
        return Spec.all_specs[name]
