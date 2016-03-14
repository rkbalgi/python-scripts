def handle(header=None, req_data=None):
    cc_resp_data = '04BE67C5692EF7459301'
    response_data = header + 'CD00' + cc_resp_data
    return response_data
