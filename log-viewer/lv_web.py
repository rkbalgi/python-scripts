#! /usr/bin/python
import SimpleHTTPServer, SocketServer, BaseHTTPServer
import urlparse
import lv_utils, lv_config
from lv_list_last import list_last

log_file_table_row = r'''
<td>Log File Name</td>
<td>
<select name="p" >
<option value="Process_1">Process_1</option>
 <option value="Process_2">Process_2</option>
 <option value="Process_3">Process_3</option>
 <option value="Process_4">Process_4</option>
 <option value="Process_5">Process_5</option>
 <option value="Process_6">Process_6</option>
 <option value="Process_7">Process_7</option>
 <option value="Process_8">Process_8</option>
 <option value="Process_9">Process_9</option>
 <option value="Process_10">Process_10</option>
 <option value="Process_1">Process_1</option>
 <option value="Process_2">Process_2</option>
 <option value="Process_3">Process_3</option>
 <option value="Process_4">Process_4</option>
 <option value="Process_5">Process_5</option>

</select>
</td>
'''
home_page = r'''
<html>
<head><title>Gan Log Viewer v1.00</title></head>
<body bgcolor="##ccccff">
<h1> Gan Log Viewer</h1>
<hr/>
<br/>

<form name="log_view_form_by_time" method="GET" action="/show_in_interval">

<table>
<tr><td colspan="2"><h2>Show In Time Interval</h2></td></tr>
<tr>
''' + log_file_table_row + '''
</tr>
<tr>
<td>
Log File Date
</td>
<td>
<input type="text" value="2016-02-24" name="log_file_date"></input>
</td>
</tr>
<tr>
<td>
Time Interval
</td>
<td>
From <input type="time" value="00:00" name="from"></input>
</td>
<td>
To <input type="time" value="02:00" name="to"></input>
</td>
</tr>
</tr>
</table>
<input type="submit" value="Show In Time Interval">
</form>


<br/>

<form name="log_view_form_0" method="GET" action="/show_last_10">

<table>
<tr><td colspan="2"><h2>Show Last 10 Transaction</h2></td></tr>
<tr>
''' + log_file_table_row + '''
</tr>
<tr>
<td>
Log File Date
</td>
<td>
<input type="text" value="2016-02-24" name="log_file_date"></input>
</td>
</tr>
</tr>
</table>
<input type="submit" value="Show Last 10 Transaction">
</form>


<br/>

<form name="log_view_form_1" method="GET" action="/show_last">

<table>
<tr><td colspan="2"><h2>Get Last Transaction</h2></td></tr>


<tr>''' + log_file_table_row + '''
</tr>
<tr>
<td>
Log File Date
</td>
<td>
<input type="text" value="2016-02-24" name="log_file_date"></input>
</td>
</tr>
</tr>
</table>
<input type="submit" value="Get Last Transaction">
</form>
<br/>
<form name="log_view_form_2" method="GET" action="/show_by_field">
<table>
<tr><td colspan="2"><h2>Get Transaction By Field</h2></td></tr>
<tr>''' + log_file_table_row + '''
</tr>
<tr>
<td>
Log File Date
</td>
<td>
<input type="text" value="2016-02-24" name="log_file_date"></input>
</td>
</tr>
<tr>
<td>Field Name</td><td><input type="text" size="40" name="f"></input></td>
<td>Field Value</td><td><input type="text" name="f_val"></input></td>

</tr>
</table>

<input type="submit" value="Get Transaction By Field">
</input>
</form>
</body>
</html>'''


class gan_logview_http_handler:
    def __init__(self):
        self.my_name = 'gan_logview_http_handler'

    def write_error_msg(self, err_msg, http_response):
        http_response.write('<html><body><h2>' + err_msg + '</h2></body></html>')

    def handle_interval_req(self, s):

        s.send_response(200)
        s.send_header('Content-Type', 'text/html')
        s.end_headers()

        index = s.path.find('?')
        if index == -1:
            self.write_error_msg('error: query parameters missing')
            return

        qs = s.path[index + 1:len(s.path)]
        params = urlparse.parse_qs(qs)
        if 'p' in params and 'from' in params and 'to' in params and 'log_file_date' in params:
            s.wfile.write('all ok')
            if params['log_file_date'][0]:
                log_file = params['p'][0] + '_' + params['log_file_date'][0] + '.log'
            else:
                log_file = params['p'][0] + '.log'
            lf_info = lv_utils.get_txn_in_interval()

        else:
            self.write_error_msg('error: mandatory query params missing')

    def handle_show_last_10(self, s):

        s.send_response(200)
        s.send_header('Content-Type', 'text/html')
        s.end_headers()

        index = s.path.find('?')
        print 'requested url = ' + s.path
        print 'index = ' + str(index)
        if index != -1:
            qs = s.path[index + 1:len(s.path)]
            params = urlparse.parse_qs(qs)
            # print params
            if 'p' not in params:
                s.send_response(500, 'bad request, p query params missing')
                return
            if 'log_file_date' in params:
                log_file = params['p'][0] + '_' + params['log_file_date'][0] + '.log'
            else:
                log_file = params['p'][0] + '.log'

            s.send_response(200)
            lf_info = list_last(log_file, 10)
            # print 'count',lf_info.count()
            if isinstance(lf_info, str):
                self.write_error_msg(lf_info, s.wfile)
            else:
                s.wfile.write('<div style="font-family: Consolas, Times, serif; font-size: 0.92em;">')
                s.wfile.write('<ol>\n')
                for i in range(0, lf_info.count()):
                    s.wfile.write('<li>' + lf_info.get_info_html_anchor(i, log_file) + '</li>\n')
                s.wfile.write('</ol></div>\n')

        else:
            s.send_response(500, 'bad request, query params missing')

    def handle_show_last_txn(self, s, file_ptr=None):

        s.send_response(200)
        s.send_header('Content-Type', 'text/html')
        s.end_headers()

        index = s.path.find('?')
        print 'requested url = ' + s.path
        print 'index = ' + str(index)
        if index != -1:
            qs = s.path[index + 1:len(s.path)]
            params = urlparse.parse_qs(qs)
            log_file = ''

            if file_ptr != None:
                if 'ptr' not in params or 'log_file' not in params:
                    s.send_response(500, 'bad request, ptr or log_file query params missing')
                    return
                else:
                    file_ptr = params['ptr'][0]
                    log_file = params['log_file'][0]
            else:
                if 'p' not in params:
                    s.send_response(500, 'bad request, p query params missing')
                    return
                if 'log_file_date' in params:
                    log_file = params['p'][0] + '_' + params['log_file_date'][0] + '.log'
                else:
                    log_file = params['p'][0] + '.log'
                file_ptr = None

            s.send_response(200)
            txn_info = lv_utils.get_txn(log_file, file_ptr)
            if isinstance(txn_info, str):
                self.write_error_msg(txn_info, s.wfile)
            else:
                txn_info.write_http(s.wfile)

        else:
            s.send_response(500, 'bad request, query params missing')

    def handle_home(self, s):
        s.send_response(200)
        s.send_header('Content-Type', 'text/html')
        s.end_headers()
        s.wfile.write(home_page)

    def handle_show_txn_by_field(self, s):
        s.send_response(200)
        s.send_header('Content-Type', 'text/html')
        s.end_headers()

        index = s.path.find('?')
        print 'requested url = ' + s.path
        print 'index = ' + str(index)
        if index != -1:
            qs = s.path[index + 1:len(s.path)]
            params = urlparse.parse_qs(qs)

            if 'log_file_date' in params:
                log_file = params['p'][0] + '_' + params['log_file_date'][0] + '.log'
            else:
                log_file = params['p'][0] + '.log'

            # print params
            if 'p' in params and 'f' in params and 'f_val' in params:
                s.send_response(200)
                txn_info = lv_utils.get_txn_by_field(log_file, params['f'][0], params['f_val'][0])
                if isinstance(txn_info, str):
                    self.write_error_msg(txn_info, s.wfile)
                else:
                    txn_info.write_http(s.wfile)
            else:
                s.send_response(500, 'bad request, f or f_val or p query params missing')
        else:
            s.send_response(500, 'bad request, query params missing')


class default_http_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):

        if s.path == '/home' or s.path == '/':
            print 'handling home request'
            gan_logview_http_handler().handle_home(s)
        elif s.path.find('/show_in_interval') != -1:
            gan_logview_http_handler().handle_interval_req(s);
        elif s.path.find('/show_last_10') != -1:
            gan_logview_http_handler().handle_show_last_10(s);
        elif s.path.find('/show_last') != -1:
            gan_logview_http_handler().handle_show_last_txn(s);
        elif s.path.find('/show_txn_by_ptr') != -1:
            gan_logview_http_handler().handle_show_last_txn(s, 'ptr');
        elif s.path.find('/show_by_field') != -1:
            gan_logview_http_handler().handle_show_txn_by_field(s);
        else:
            http_resp = 'invalid url'
            s.wfile.write(http_resp);


if __name__ == "__main__":
    handler = default_http_handler
    server = BaseHTTPServer.HTTPServer(('', lv_config.httpd_port), handler)
    # SocketServer.TCPServer(('localhost', port), handler)
    # server = SocketServer.TCPServer(('localhost', port), handler)
    print 'gan log viewer serving @ ' + str(lv_config.httpd_port)
    server.serve_forever()
