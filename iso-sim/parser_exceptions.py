class FieldParseException(BaseException):
    def __init__(self, msg):
        BaseException.__init__(self, msg)
