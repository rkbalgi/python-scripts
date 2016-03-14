import codecs, binascii

ebcdic_decoder = codecs.getdecoder('cp037')
ebcdic_encoder = codecs.getencoder('cp037')


def ebcdic_to_str(data):
    return ebcdic_decoder(data)[0]


def ebcdic_from_str(str):
    return ebcdic_encoder(str)[0]


def ascii_to_str(data):
    res = codecs.getdecoder('ascii')(data)
    return res[0]
    # print res


def ascii_from_str(strval):
    res = codecs.getencoder('ascii')(strval)
    return res[0]


def from_hex(strval):
    return binascii.unhexlify(strval)


def to_hex(data):
    return binascii.hexlify(data)


