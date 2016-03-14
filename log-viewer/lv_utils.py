#! /usr/bin/python

import commands, sys, os, re, lv_config
import StringIO
from datetime import datetime

log_line_re = re.compile('([0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3})\s+(ERROR|DEBUG)\s+.*$')
field_val_re = re.compile('^\s*\[(.*?):(.*?)\]$');
'''when reading a log file, we expect to see things like sent to core, or sending reply which marks the end of transaction data for that file
   and processing continues with the next file. If there are exceptions or errors then we may not be find such lines and so there needs to be a hard 
   stop to when we stop looking and the below limit for that
'''
g_line_limit = 1000

error_table_fmt_str = r'''<table border="1" style="border: 1px solid black; font-family: consolas, serif; background-color: red">
<tr><th align="center">Process Name</th> <th align="center">Errors</th></tr>
<tr>
<td>{0}</td><td><pre style="white-space: pre-wrap; word-wrap: break-word;">{1}</pre></td>
</tr>
<tr>
<td>{2}</td><td><pre style="white-space: pre-wrap; word-wrap: break-word;">{3}</pre></td>
</tr>
<tr>
<td>{4}</td><td><pre style="white-space: pre-wrap; word-wrap: break-word;">{5}</pre></td>
</tr>
</table><br/>'''


def hello():
    print 'hello world\n'


class c_txn_info:
    def __init__(self):
        self.txn_key = ''
        self.acq_log_info = ''
        self.core_log_info = ''
        self.core_in = None
        self.core_name = ''
        self.host_name = None
        self.host_log_info = ''
        self.src_file_date = None
        self.acq_errors = ''
        self.core_errors = ''
        self.host_errors = ''

    def set_core_info(self, sent_to_core_at, core_name):
        self.core_in = sent_to_core_at
        self.core_name = core_name
        print self.core_in, "|", self.core_name

    def append_key(self, key):
        self.txn_key = self.txn_key + "|" + key

    def update_acq_info(self, acq_info):
        self.acq_log_info = self.acq_log_info + acq_info

    def update_core_info(self, core_info):
        self.core_log_info = self.core_log_info + core_info

    def update_host_info(self, host_info):
        self.host_log_info = self.host_log_info + host_info

    def update_info(self, process_type, info):
        if process_type == 'core':
            self.update_core_info(info)
        elif process_type == 'host':
            self.update_host_info(info)
        elif process_type == 'acq':
            self.update_acq_info(info)

    def get_errors(self):
        stringio_input = StringIO.StringIO(self.acq_log_info)
        self.acq_errors = self.capture_errors(stringio_input)
        self.core_errors = self.capture_errors(StringIO.StringIO(self.core_log_info))
        self.host_errors = self.capture_errors(StringIO.StringIO(self.host_log_info))

    # print 'errors = ',acq_errors,core_errors,host_errors

    def capture_errors(self, stringio_obj):

        capture = 0
        errors = ''
        for line in stringio_obj:
            match_res = log_line_re.match(line)
            if match_res != None:
                if match_res.group(2) == 'ERROR' or match_res.group(2) == 'FATAL':
                    capture = 1
                else:
                    capture = 0
            if capture:
                errors = errors + line
            elif line.lower().find('error') != -1 or line.lower().find('exception') != -1:
                ignore = 0
                for ignore_error in lv_config.ignore_errors:
                    if line.find(ignore_error) != -1:
                        ignore = 1
                if not ignore:
                    errors = errors + line
        return errors

    def write_to_file(self, o_file_name):
        o_file = open(o_file_name, 'w')
        o_file.write(self.acq_process_name + '\n')
        o_file.write('-------------------------------------\n')
        o_file.write(self.acq_log_info + '\n\n\n\n')
        o_file.write('-------------------------------------\n')
        if self.core_in != None:
            o_file.write(self.core_name + '\n')
            o_file.write('-------------------------------------\n')
            o_file.write(self.core_log_info + '\n\n\n\n')
            o_file.write('-------------------------------------\n')
        if self.host_name != None:
            o_file.write(self.host_name + '\n')
            o_file.write('-------------------------------------\n')
            o_file.write(self.host_log_info + '\n\n\n\n')
            o_file.write('-------------------------------------\n')
        o_file.close()

    def write_http(self, http_response):
        self.get_errors()
        http_response.write('<html><head><title>Gan Log Viewer</title></head><body bgcolor="##4da6ff"><br/>\n')
        http_response.write('<h1> Gan Log Viewer </h1> <hr> <br/>')
        links = '[ <a href="#' + self.acq_process_name + '">' + self.acq_process_name + '</a>'
        http_response.write(
            error_table_fmt_str.format(self.acq_process_name, self.acq_errors, self.core_name, self.core_errors,
                                       self.host_name, self.host_errors))
        if self.core_in != None:
            links = links + '| <a href="#' + self.core_name + '">' + self.core_name + '</a>'
        if self.host_name != None:
            links = links + '| <a href="#' + self.host_name + '">' + self.host_name + '</a> '
        links = links + ' ]'
        http_response.write(links + '<br/>')
        http_response.write('<h3 id="' + self.acq_process_name + '">' + self.acq_process_name + '</h3><br/>\n')
        http_response.write(
            '<pre bgcolor="#ffffb3" style="background-color:#aaff00; white-space: pre-wrap; word-wrap: break-word;">' + self.acq_log_info + '</pre> \n\n\n\n')
        if self.core_in != None:
            http_response.write('<h3 id="' + self.core_name + '">' + self.core_name + '</h3><br/>\n')
            http_response.write(links + '<br/>')
            http_response.write(
                '<pre bgcolor="#66ff66" style="background-color:#66ff66; white-space: pre-wrap; word-wrap: break-word;">' + self.core_log_info + '</pre> \n\n\n\n')
        if self.host_name != None:
            http_response.write('<h3 id="' + self.host_name + '">' + self.host_name + '</h3><br/>\n')
            http_response.write(links + '<br/>')
            http_response.write(
                '<pre bgcolor="#ff8080" style="background-color:#ff8080; white-space: pre-wrap; word-wrap: break-word;">' + self.host_log_info + '</pre> \n\n\n\n')
        http_response.write('\n</body></html>')

    def to_string(self):
        return "txn_key = [" + self.txn_key + "] [acq_info = " + self.acq_log_info + " ]"


def get_file_name_from_process(process_name, txn_info):
    file_name = None
    if process_name == 'CORE-A':
        file_name = 'Core-A'
    elif process_name == 'CORE-B':
        file_name = 'Core-B'
    elif process_name == 'AR_Queue':
        file_name = 'AR_PROCESS'
    elif process_name == 'CAS-Multiplexed':
        file_name = 'CAS'
    elif process_name == 'CAS-Auth':
        file_name = 'CAS-Auth'
    elif process_name == 'CAS_AAV':
        file_name = 'CAS_AAV'

    if file_name != None:
        if txn_info.src_file_date != None:
            file_name = file_name + '_' + txn_info.src_file_date + '.log'
        else:
            file_name = file_name + '.log'
    return file_name


def extract_process_info(process_name, txn_info, process_type):
    file_name = get_file_name_from_process(process_name, txn_info)

    print 'file name = ', file_name

    if file_name != None:
        # match_obj=re.match(self.core_name+'-processMessageQueue():Executing List:([^\[]+)\[+ self.core_in+'\]',
        grep_cmd = 'grep -b -e \'' + process_name + '-processMessageQueue():Executing List:.* \[' + txn_info.core_in + '\]\' ' + lv_config.log_dir + file_name
        print 'grep_cmd = ', grep_cmd
        grep_res = commands.getstatusoutput(grep_cmd)
        print 'grep_res = ', grep_res
        if grep_res[0] == 0:
            fptr = grep_res[1].split(':')[0]
            print 'opening file' + file_name + ' @ ptr' + fptr
            file_handle = open(lv_config.log_dir + file_name, 'r')
            file_handle.seek(int(fptr), os.SEEK_SET)
            n_lines = 0
            while 1:
                line = file_handle.readline()
                # print 'core line = '+line
                # raw_input('...')
                n_lines = n_lines + 1
                if not line:
                    txn_info.update_info(process_type, 'Giving up ... reason = EOF');
                    break
                txn_info.update_info(process_type, line);
                match_obj = re.match('\s*Sending reply to \[([^\]]+)\] \[' + txn_info.core_in + '\]', line)
                if match_obj != None:
                    print 'ending at' + line
                    break
                if n_lines > g_line_limit:
                    txn_info.update_info(process_type, 'Giving up ... reason = line limit exceeded');
                    break
                match_res = re.match('\s*Sent msg@(.*) to Queue=\[([^\]]+)\].*$', line)
                if match_res != None:
                    print 'matches = ' + match_res.group(2)
                    print 'host process name =' + match_res.group(2)
                    txn_info.host_name = match_res.group(2)
                    extract_process_info(match_res.group(2), txn_info, 'host');


        else:
            txn_info.update_info(process_type, 'failed to read transaction info from -' + process_name);
    else:
        print 'unable to capture info for process name =' + process_name


def extract_txn_key(line, match_obj, txn_info):
    res = ''
    key = match_obj.group(1)
    if key == '^Acquirer Name^':
        res = 'AcquirerName=' + match_obj.group(2)
    if key.lower().find('amount') != -1 or key.lower().find('mti') != -1 or key.lower().find(
            'message type') != -1 or key.lower().find('track') != -1 or key.lower().find(
            'stan') != -1 or key.lower().find('number') != -1 or key.lower().find('trace') != -1:
        txn_info.append_key(res)


def extract_txn(file_handle, txn_info):
    acq_log_info = ''
    txn_key = '';
    n_lines = 0
    while 1:
        line = file_handle.readline()
        # if line.find('[SocketConnectionHandler]')!=-1: # and line.find('[^Acquirer Name^:')!=-1:
        #		txn_key=extract_txn_key(line);
        # print 'line = '+line
        n_lines = n_lines + 1
        match_res = field_val_re.match(line)
        if match_res != None:
            extract_txn_key(line, match_res, txn_info)
        match_res = re.match('\s*Sent msg@(.*) to Queue=\[([^\]]+)\].*$', line)
        if match_res != None:
            print 'matches = ' + match_res.group(2)
            txn_info.set_core_info(match_res.group(1), match_res.group(2))
            # now, we can set off and go look at the core file
            extract_process_info(match_res.group(2), txn_info, 'core');

        # print match_res
        txn_info.update_info('acq', line);
        if not line:
            txn_info.update_acq_info('giving up ... reason = EOF');
            break
        if line.find("MsgOUT:") != -1:
            break
        if line.find('Parsing failed: MsgIN') != -1:
            txn_info.update_acq_info('giving up ... reason = parse failure');
            break
        if n_lines > g_line_limit:
            txn_info.update_acq_info('giving up ... reason = line limit exceeded');
            break
    return txn_info


def get_acq_process_name(txn_info, in_log_file):
    obj = re.match('.*([0-9]{4}\-[0-9]{2}\-[0-9]{2})\.log', in_log_file)
    if obj != None:
        src_file_date = in_log_file[obj.start(1):obj.start(1) + 10]
        txn_info.src_file_date = src_file_date
        acq_process_name = in_log_file[0:obj.start(1) - 1]
    else:
        index = in_log_file.find('.log')
        acq_process_name = in_log_file[0:index]
    return acq_process_name


def get_txn(in_log_file, file_ptr=None):
    txn_info = c_txn_info()
    acq_process_name = get_acq_process_name(txn_info, in_log_file)
    if file_ptr == None:

        grep_result = commands.getstatusoutput(
            "grep -b 'Parsing incoming message from java.nio.channels.SocketChannel.*MsgIN' " + lv_config.log_dir + in_log_file + " | awk   'BEGIN {FS=\":\"} {print $1}'")
        if grep_result[0] != 0:
            return 'error: no transactions found. error code =' + grep_result[0]

        file_ptrs = grep_result[1].split();
        if len(file_ptrs) == 0:
            return 'error: no transactions found'
        last_ptr = file_ptrs[len(file_ptrs) - 1]
    else:
        last_ptr = file_ptr
    file_handle = open(lv_config.log_dir + in_log_file, 'r')
    print 'looking for transaction at =', last_ptr, file_ptr

    txn_info.acq_process_name = acq_process_name
    file_handle.seek(int(last_ptr), os.SEEK_SET);
    extract_txn(file_handle, txn_info);
    # out_file='txn_extract_'+ datetime.now().strftime('%d%m%Y_%H%M%S_%f')+'.log'
    # print 'out_file = '+out_file
    # txn_info.write_to_file(out_file)
    return txn_info


def get_txn_by_field(in_log_file, field_name, field_val):
    grep_result = commands.getstatusoutput(
        "grep -b 'Parsing incoming message from java.nio.channels.SocketChannel.*MsgIN' " + lv_config.log_dir + in_log_file + " | awk   'BEGIN {FS=\":\"} {print $1}'")
    if grep_result[0] != 0:
        return 'error: no transactions found. error code =' + str(grep_result[0])
    file_ptrs = grep_result[1].split();

    grep_res = commands.getstatusoutput(
        'grep -b -e \'\[' + field_name + ':' + field_val + '\]\' ' + lv_config.log_dir + in_log_file)
    if grep_res[0] != 0:
        return 'error: no transaction found. error code = ' + str(grep_res[0])
    fptrs = grep_res[1].split('\n')
    last_fptr = fptrs[len(fptrs) - 1].split(':[')[0]
    prev_ptr = fptrs[0]
    for ptr in file_ptrs:
        if long(ptr) > long(last_fptr):
            break
        else:
            prev_ptr = ptr

    file_handle = open(lv_config.log_dir + in_log_file, 'r')
    if not file_handle:
        return 'error: unable to open file. file = ' + in_log_file
    file_handle.seek(long(prev_ptr), os.SEEK_SET)
    txn_info = c_txn_info()
    acq_process_name = get_acq_process_name(txn_info, in_log_file)
    txn_info.acq_process_name = acq_process_name
    extract_txn(file_handle, txn_info);
    # out_file='txn_extract_'+ datetime.now().strftime('%d%m%Y_%H%M%S_%f')+'.log'
    # print 'out_file = '+out_file
    # txn_info.write_to_file(out_file)
    return txn_info


def get_txn_in_interval(in_log_file, from_time, to_time):
    if from_time.matches('[0-9]{2}:[0-9]{2}') and to_time.matches('[0-9]{2}:[0-9]{2}'):
        print 'ok'
    else:
        return 'error: invalid from/to time format'


if __name__ == "__main__":
    file = 'US_Process_5_2016-02-24.log'
    # get_last_txn(file);
    txn_info = get_txn_by_field(file, 'System trace audit number', '700029')
    txn_info.get_errors()
