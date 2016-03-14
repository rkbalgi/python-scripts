#! /usr/bin/python

import lv_config, commands, os, lv_utils, re

field_val_re = re.compile('^\s*\[([^\]:]+?):([^\]:]+?)\]$')


class last_few_txn_info:
    def __init__(self):
        self.last_few_ptrs = []
        self.last_few_keys = []

    def append(self, ptr, key):
        self.last_few_ptrs.append(ptr)
        self.last_few_keys.append(key.strip())

    def get_info(self, n):
        return self.last_few_ptrs[n] + ' = ' + self.last_few_keys[n]

    def get_info_html_anchor(self, n, in_log_file):
        return '<a href="/show_txn_by_ptr?ptr=' + self.last_few_ptrs[n] + '&log_file=' + in_log_file + '">' + \
               self.last_few_keys[n] + '</a>'

    def count(self):
        return len(self.last_few_ptrs)


def list_last(in_log_file, n):
    last_5 = []
    lf_info = last_few_txn_info()

    grep_result = commands.getstatusoutput(
        "grep -b 'Parsing incoming message from java.nio.channels.SocketChannel.*MsgIN' " + lv_config.log_dir + in_log_file + " | awk   'BEGIN {FS=\":\"} {print $1}'")
    if grep_result[0] != 0:
        return 'error: no transactions found. error code =' + grep_result[0]

    file_ptrs = grep_result[1].split();
    # file_handle=open(lv_config.log_dir+in_log_file,'r')
    print 'file ptrs', file_ptrs
    if len(file_ptrs) == 0:
        return 'error: no transactions found'
    last_ptr = file_ptrs[len(file_ptrs) - 1]
    if len(file_ptrs) > n:
        for i in range(len(file_ptrs) - n, len(file_ptrs)):
            last_5.append(file_ptrs[i])
    else:
        for i in range(0, len(file_ptrs)):
            last_5.append(file_ptrs[i])
    fh = None
    try:
        fh = open(lv_config.log_dir + in_log_file, 'r')
    except IOError as e:
        return 'error: file not found. file = ' + in_log_file
    if not fh:
        return 'error: unable to open file'
    prev_line = None
    line = None
    done = 0
    for ptr in last_5:
        fh.seek(long(ptr), os.SEEK_SET)
        current_key = ''
        done = 0
        prev_line = None
        line = None
        while not done:
            prev_line = line
            line = fh.readline()
            if line.find('Parsing failed') != -1:
                current_key = 'error: parsing failed'
                done = 1
            match_res = field_val_re.match(line.strip())
            if match_res != None and prev_line.find('[SocketConnectionHandler]') != -1:
                while match_res != None:
                    key = match_res.group(1)
                    if should_extract(key):
                        current_key = current_key + line.strip()
                    line = fh.readline()
                    if not line:
                        done = 1
                        break
                    match_res = field_val_re.match(line.strip())
                    if match_res == None:
                        done = 1
        lf_info.append(ptr, current_key)
    return lf_info


def should_extract(key):
    if (key.lower().find('acquirer') != -1 or
                key.lower().find('amount') != -1 or
                key.lower().find('mti') != -1 or
                key.lower().find('message type') != -1 or
                key.lower().find('track') != -1 or
                key.lower().find('stan') != -1 or
                key.lower().find('number') != -1 or
                key.lower().find('trace') != -1):
        return 1
    return 0


if __name__ == "__main__":
    lf_info = list_last('US_Process_5_2016-02-24.log', 10)
    # lf_info=list_last_5('test.log')
    for i in range(0, lf_info.count()):
        print lf_info.get_info(i)
