import threading
import command_nc
import command_cc
import struct


class ClientSessionHandlerThread(threading.Thread):
    Count = 0

    def __init__(self, sock):

        threading.Thread.__init__(self, name='Thread -' + str(self.Count))
        self.Count += 1
        self.sock = sock

    def run(self):

        while 1:
            try:
                data = self.sock.recv(2)

                if data is not None and len(data) > 0:
                    n = struct.unpack('!H', data[0:2])[0]
                    req_data = self.sock.recv(n)
                    if len(req_data) == n:
                        self.process_req(req_data)

            except TypeError as typeError:
                log.error('error handling client connection' + typeError.message);
                return
            except:
                log.error('error handling client connection' + str(sys.exc_info()));
                return

    """def handle_command_nc(self, header):
        nc_resp_data = '26860400000000001084-0907'
        response_data = header + 'ND00' + nc_resp_data
        response_len = struct.pack('!H', len(response_data))
        # print 'response length = ', response_len, len(response_data) + 2
        log.debug('writing ..' + (response_len + response_data))
        print len(response_len), len(response_data)
        n = self.sock.send(response_len + response_data)
        print 'sent', n, ' bytes'

    def handle_command_cc(self, header):
        cc_resp_data = '04BE67C5692EF7459301'
        response_data = header + 'CD00' + cc_resp_data"""

    def process_req(self, req_data):

        header = req_data[0:12]
        command_code = req_data[12:14]
        req_data = req_data[14:]
        print 'header= {0} command code = {1}'.format(header, command_code)
        response_data = None
        if command_code == 'NC':
            response_data = command_nc.handle(header, req_data)
        elif command_code == 'CC':
            response_data = command_cc.handle(header, req_data)

        if response_data is not None:
            response_len = struct.pack('!H', len(response_data))
            n = self.sock.send(response_len + response_data)
            print 'sent', n, ' bytes'
