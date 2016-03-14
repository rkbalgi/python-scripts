from com.github.rkbalgi.thales.keys import thales_keys
from com.github.rkbalgi.thales.string_component import StringComponent
from com.github.rkbalgi.thales.comms.thales_comms import hsm_comms

class A6:
    
    counter=0
    
    req_params = ['Header',
                  'Command Code',
                  'Key Type',
                  'ZMK',
                  'Key',
                  'Key Scheme LMK',
                  'Delimiter',
                  'LMK Identifier']
    resp_params = ['Header',
                   'Response Code',
                   'Error Code',
                   'Key',
                   'Key Check Value',
                   'End Message Delimiter',
                   'Message Trailer']

    
    def __init__(self, header_len):
        self.header_len = header_len
       
        A6.counter = A6.counter + 1
        self.header = StringComponent.withData(str(A6.counter).zfill(header_len))
        self.command_code = StringComponent.withData('A6')
        self.key_type = StringComponent()
        self.zmk = StringComponent()
        self.key = StringComponent()
        self.key_scheme_lmk = StringComponent.withData('U')
        self.delim = StringComponent.withData('%')
        self.lmk_id = StringComponent.withData('00')
        
        self.response_code = StringComponent()
        self.error_code = StringComponent()
        self.resp_key = StringComponent()
        self.key_check_val = StringComponent()
        self.end_msg_delim = StringComponent()
        self.msg_trailer = StringComponent()
        
        self.req_param_vals = [self.header, self.command_code, self.key_type, self.zmk,
                               self.key, self.key_scheme_lmk, self.delim, self.lmk_id]
        self.resp_param_vals = [self.header, self.response_code, self.error_code,
                               self.resp_key, self.key_check_val, self.end_msg_delim, self.msg_trailer]
    
    def execute(self):
        
        buf = bytearray()
        i = 0
        for param in self.req_param_vals:
            if param.hasData():
                buf.extend(param.getValue())
            else:
                print 'Warning: parameter [', A6.req_params[i], '] is not set.'     
            i = i + 1
        try:
            resp_data = hsm_comms.send_data(buf)
            # #parse resp_data
            print resp_data
        except IOError as e:
            print 'A6 command execution failed. Reason: ', e
        except:
            print 'A6 command execution failed. Reason: nil'         
        
    def dump(self):
        buf = self.command_code.getValue() + ' Request = [\n';
        i = 0
        for param in self.req_param_vals:
            buf += '{0:40s} = <{1}>;\n'.format(A6.req_params[i], param.getValue());
            i = i + 1
               
        buf += ']\n'
        i = 0
        buf += self.command_code.getValue() + ' Response = [\n'
        for param in self.resp_param_vals:
            buf += '{0:40s} = <{1}>;\n'.format(A6.resp_params[i], param.getValue());
            i = i + 1;   
        buf += ']\n'
        
                
        return buf
    
    def set_zmk(self, data):
        self.zmk = data

if __name__ == "__main__":
    a6_obj = A6(12)
    a6_obj.zmk.setValue('UE10BB4BDA12B57F45799D565A4D427F0')
    a6_obj.key.setValue('32F68193ADD0760F')
    a6_obj.key_type.setValue(thales_keys.KEY_TYPE_MAC)
    a6_obj.lmk_id.setValue('00')
    a6_obj.execute()
    
    # hsm_comms.close()
    
    print a6_obj.dump()
    
    

