class Message:
    def __init__(self, msg_def):
        self.msg_def = msg_def
        self.request_data = dict()
        self.response_data = dict()

    def update(self, field, field_data, is_request):

        if is_request:
            self.request_data[field.name] = field_data
        else:
            self.response_data[field.name] = field_data;
