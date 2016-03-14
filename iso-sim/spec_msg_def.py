from msg import Message


class SpecMessageDef:
    def __init__(self, name):
        self.name = name
        self.req_fields = []
        self.resp_fields = []

    def add_req_field(self, field):
        self.req_fields.append(field)

    def add_resp_field(self, field):
        self.resp_fields.append(field)

    def parse_request(self, buf):
        msg = Message(self)
        index = 0
        for f in self.req_fields:
            index = f.parse(msg, buf, index, True)
