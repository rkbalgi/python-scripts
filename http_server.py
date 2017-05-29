#!/usr/bin/python

import BaseHTTPServer
import optparse
import subprocess
import string,io,os
import re,json,time,tempfile

temp_file=tempfile.NamedTemporaryFile(prefix='tmp_rsp_times_$$')
cmd_args=None
ext_pr=None

class ResponseTime:
        def __init__(self):
                self.time_stamp=time.asctime();
                self.response_time=0.0

        def __str__(self):
                return 'timestamp: {0}\t response time: {1}'.format(self.time_stamp,self.response_time)

class RatesAndTime:
        def __init__(self):
                self.response_time=None
                self.rates_map=None

#Read last record from file
def get_response_times():
        f=open(temp_file.name,'r')
        f.seek(-1000,os.SEEK_END)
        i=0
        response_time=ResponseTime()
        time_stamp=''
        for line in f:
                if re.match('^???',line):
                        time_stamp=line.split(' ')[1]
                        response_time.time_stamp=time_stamp
                if line.startswith('???:'):
                        temp=string.strip(line[line.index(':')+1:line.index('(')])
                        if not temp:
                                temp='0.0'
                        response_time.response_time=float(temp)

        f.close()
        return response_time


## starts the external  process
def start_ext_reader():
        try:
                global ext_process
                ext_process=subprocess.Popen(cmd_args,stdout=subprocess.PIPE)
        except:
                print 'error starting atr stats reader process'


def get_otherhs():
        cmd=['/tmp/exe_bin',pr_inq,'???']
        try:
                rates_pr=subprocess.Popen(cmd,stdout=subprocess.PIPE)
                (data_stdout,data_stderr)=rates_pr.communicate()
                lines=string.split(data_stdout,'\n')
                rates=dict()
                for line in lines:
                        match_obj=re.match('\s+([0-9]+\.[0-9]+)\s([A-Z,0-9]+)',line)
                        if match_obj:
                                rates[match_obj.group(2)]=float(match_obj.group(1))
                response=dict()
                response['rates']=rates;
                response_time=get_response_times()
                response['response_time']=response_time.response_time
                response['time_stamp']=response_time.time_stamp
                return json.dumps(response,indent=4)
        except subprocess.CalledProcessError as e:
                print 'exception while retrieving rates from atr',e.cmd,e.returncode,e.output
        return None

class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
                print "received request for",self.path
                response=''
                if self.path=='/atr/rest/v0/rates_n_times':
                        response=get_otherhs()

                if not response:
                        self.send_error_response()
                        return
                else:
                        self.send_json_response(response);


        def send_error_response(self):
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write('{"error":"invalid_url: "'+self.path+ '}')

        def send_json_response(self,json):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json)

if __name__=="__main__":
        opt_parser=optparse.OptionParser()
        opt_parser.add_option('--??',dest='1_inq',type=str,help='????')
        opt_parser.add_option('--??',dest='1_file',type=str,help='???')

        (opts,args)=opt_parser.parse_args()
        global ext_inq
        ext_inq=opts.atr_inq
        cmd_args=['/usr/bin/echo',opts.1_file,'-output',temp_file.name]
        if not 1_inq or not opts.1_file:
                opt_parser.print_help()
                exit(1)
        print 'HTTP Server v0.1\n@--------------------------------------------'
        server_addr=('',8080)
        start_ext_reader()
        http_server=BaseHTTPServer.HTTPServer(server_addr,HttpHandler)
        try:
                http_server.serve_forever()
        except:
                ext_pr.kill()
