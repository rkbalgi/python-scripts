def handle(header=None, req_data=None):
    nc_resp_data = '26860400000000001084-0907'
    response_data = header + 'ND00' + nc_resp_data
    return response_data
