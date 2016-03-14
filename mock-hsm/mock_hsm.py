'''A simple mock hsm (tcp/ip server) to mock hardware calls for
popular Thales HSM commands'''

import socket
import logging
import logging.config
import logging.handlers

import mock_hsm_ui

log = None

if __name__ == "__main__":

    # HsmListenerThread(1510).start()
    mockHsmUi = mock_hsm_ui.MockHsmUi()
    mockHsmUi.show()
