import socket
import struct
import sys
from com.github.rkbalgi.pycat.pycat import hexdump 
class hsm_config:
    
    
    ip = '127.0.0.1'
    #ip = '10.16.204.75'
    #ip='10.16.204.77'
    port = 1500
    
    @staticmethod
    def info():
        return hsm_config.ip + ':' + str(hsm_config.port)

class hsm_comms:
    
    sock = None
    sock_opened = 0
    
    @staticmethod
    def init():
        if hsm_comms.sock_opened == 0:
            print 'opening connection to hsm - ', hsm_config.info()
            try:
                hsm_comms.sock = socket.create_connection((hsm_config.ip, hsm_config.port))
            except:
                print 'unable to open connection to hsm', sys.exc_info()[0]
            else:
                print 'connection opened to hsm - ', hsm_config.info()
                hsm_comms.sock_opened = 1
            
    @staticmethod
    def close():
        if hsm_comms.sock != None:
            hsm_comms.sock.close();
    
            
    @staticmethod
    def send_data(data):
        
        hsm_comms.init();
        if hsm_comms.sock_opened == 0:
            raise Exception('hsm connection failure.')
        buf = bytearray(2)
        struct.pack_into(">H", buf, 0, len(data))
        buf.extend(data)
        print '>> \n', hexdump(buf);
        n = hsm_comms.sock.send(buf);
        if n == 2 + len(data):
            # all data has been written
            resp_mli = bytearray(2)
            n = hsm_comms.sock.recvfrom_into(resp_mli, 2);
            if n[0] == 2:
                data_length = struct.unpack(">H", resp_mli)[0]
                resp_data = bytearray(data_length);
                n = hsm_comms.sock.recvfrom_into(resp_data, data_length)
                if  n[0] == data_length:
                    print '<< \n', hexdump(resp_data);
                    return resp_data  
        return None
    
    
if __name__ == "__main__":
    print hsm_config.ip + ':' + str(hsm_config.port)
    hsm_comms.init()
    hsm_comms.close()
