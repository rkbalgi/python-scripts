import threading
import socket
import hsm_client_session_handler
import sys
import logging
import mock_hsm_ui


class HsmListenerThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self, name='Thread - Hsm-Listener')
        self.port = port
        self.log = logging.getLogger('HsmListener::')
        self.log.setLevel(logging.DEBUG)
        self.ssock = None

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        self.log.addHandler(stream_handler)

    def run(self):
        self.log.info('starting mock hsm at port -' + str(self.port))

        self.ssock = socket.socket()
        self.ssock.bind(('localhost', self.port))
        self.ssock.listen(1)

        try:
            while mock_hsm_ui.hsm_started:
                (csock, addr) = self.ssock.accept()
                self.log.info('client connection accepted from - ' + str(addr))
                hsm_client_session_handler.ClientSessionHandlerThread(csock).start()
            self.log.info('hsm stopped listening ..')
            mock_hsm_ui.hsm_started = 0
        except:
            self.log.err('error while running hsm', str(sys.exc_info()))
            mock_hsm_ui.hsm_started = 0

    def stop_hsm(self):
        self.ssock.shutdown(socket.SHUT_RDWR)
        self.ssock.close()
        mock_hsm_ui.hsm_started = 0
