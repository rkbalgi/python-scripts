

'''
Created on 15-Dec-2014

# A simple utility to write data to a TCP/IP destination

# An mli or message length indicator are bytes at the beginning of the packet/message
# that specify the number of bytes (or length) of the message
# as 2i is a two byte (short in Java) indicator that says how long the message is and is inclusive of the 2 bytes of the 
# so 2e is a two byte (short in Java) indicator that says how long the message is
# indicator itself

@author: Raghavendra Balgi
'''

import socket,base64
import struct, logging
import argparse

def hexdump(data):
    last_index = 0
    n = 0
    while True:
        tmp = data[last_index:last_index + 16]
        if len(tmp) == 0:
            break
        print '{0}: {1} |{2}|'.format(format(n, "08x"), __split__(bytearray(tmp)), __normalize__(tmp))
        # print 
        n += len(tmp)
        last_index += 16
        if len(tmp) < 16:
            break

def to_hex(ascii_str):
    ba=bytearray()
    i=0
    while i<len(ascii_str)-1:
        tmp=ascii_str[i:i+2]
        ba.append(int(tmp,16))
        i+=2 
    return ba    


def from_hex(byte_array):
    hex_str = base64.b16encode(byte_array)
    return hex_str
# 
# def from_hex_str(hex_str):
#     print type(base64.b16decode(hex_str))
#     return bytearray(base64.b16decode(hex_str))

def __split__(byte_array):
        tmp = ''
        n = 0
        for b in byte_array:
            n += 1
            tmp = tmp + format(b, '02x') + ' '
            if n == 8:
                tmp += ' '
                
        short = 16 - len(byte_array)
        
        
        if short != 0:
            for _ in range(short * 3):
                tmp += ' '
        if len(byte_array) <= 8: tmp += ' '        
        return tmp

def __normalize__(str1):
    tmp = ''
    for c in str1:
        # include only printable characters
        if c >= 32 and c <= 126:
            # print 'appending'
            tmp = tmp + chr(c)
        else:
            tmp += '.'
    while len(tmp) < 16:
        tmp += ' '        
    
    return tmp
    

if __name__ == "__main__":
    
    
    argparser = argparse.ArgumentParser(epilog='If no mli is specified, data will be written as is')
    
    argparser.add_argument('--ip', required=True, help='destination ip - Example: localhost, www.acme.com')
    argparser.add_argument('--port', required=True, type=int, help='port - Example: 1500')
    argparser.add_argument('--mli', help='mli type - [2i | 2e]')
    argparser.add_argument('--data', required=True,help='data in hex digits - Example - 30303030')

    args = argparser.parse_args()

    in_data = to_hex(args.data)
    c_mli=None
    
    if args.mli != None:
        if args.mli not in ['2i','2e']:
            argparser.print_help()
            quit()
        else:
            
            if args.mli=="2e":
                c_mli=struct.pack('!h',len(in_data))    
            else:
                c_mli=struct.pack('!h',len(in_data)+2)
    
    request_data=bytearray(1000)
    request_data=c_mli+in_data
                    
    logging.basicConfig(format='%(asctime)-15s - %(module)-10s - %(message)s')
    logger = logging.getLogger("pyutils")
    logger.setLevel(logging.DEBUG)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((args.ip, args.port))
    except IOError as e:
        logger.error('Connection Error: %s', e)
        quit()    
        
    # request_data=bytearray('\x00\x0E\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\30NC')
    logger.debug('sending ...')
    hexdump(request_data)
    sock.send(request_data)

    
    logger.debug('receiving ...')
    mli=None
    try:
        mli = sock.recv(2)
    except IOError as e:
        if e.message.find('timed out')!=-1:
            logger.error('no data received.')
            quit()
    if mli!=None and len(mli) == 2:
        mli_len = struct.unpack("!H", mli)
        response_data_len=mli_len[0]
        if(args.mli!=None):
            if args.mli=="2i":
                response_data_len-=2
        response_data = sock.recv(response_data_len)
        hexdump(bytearray(response_data))
    else:
        logger.error('no data received.')



    
        
