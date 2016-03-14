from com.github.rkbalgi.thales.string_component import StringComponent
from com.github.rkbalgi.thales.comms.thales_comms import hsm_comms

import sys
class MS:
    
    counter=0
    
    req_params = ['Header',
                  'Command Code',
                  'Message Block Number',
                  'Key Type',
                  'key Length',
                  'Message Type',  # 0 Binary, 1 Expanded Hex
                  'Key',
                  'IV',
                  'Message Length',  # 4H
                  'Message Block',
                  'Delimiter',
                  'LMK Identifier']
    resp_params = ['Header',
                   'Response Code',
                   'Error Code',
                   'MAB',
                   'End Message Delimiter',
                   'Message Trailer']

    
    def __init__(self, header_len):
        self.header_len = header_len
        MS.counter = MS.counter + 1
        self.header = StringComponent.withData(str(MS.counter).zfill(header_len))
        self.command_code = StringComponent.withData('MS')
        self.message_block_number = StringComponent.withData('0')
        self.key_type = StringComponent.withData('0') #0=TAK, 1=ZAK
        self.key_length = StringComponent.withData('1')
        self.message_type = StringComponent.withData('0')
        self.key = StringComponent()
        self.iv = StringComponent()
        self.message_length = StringComponent()
        self.message_block = StringComponent()
        self.delim = StringComponent.withData('%')
        self.lmk_id = StringComponent.withData('00')
        
        self.response_code = StringComponent()
        self.error_code = StringComponent()
        self.mab = StringComponent()
        self.end_msg_delim = StringComponent()
        self.msg_trailer = StringComponent()
        
        self.req_param_vals = [self.header, self.command_code, self.message_block_number, self.key_type, self.key_length,
                               self.message_type, self.key, self.iv, self.message_length, self.message_block, self.delim, self.lmk_id]
        self.resp_param_vals = [self.header, self.response_code, self.error_code,
                               self.mab, self.end_msg_delim, self.msg_trailer]
        
    def params(self,key=None,message_block=None):
        
        if key!=None:
            self.key.setValue(key)
        if message_block!=None:
            msg_len='{0:04d}'.format(len(message_block))
            self.message_length.setValue(msg_len)
            self.message_block.setValue(message_block)
                
    
    def execute(self):
        
        buf = bytearray()
        i = 0
        for param in self.req_param_vals:
            if param.hasData():
                buf.extend(param.getValue())
            else:
                print 'Warning: parameter [', MS.req_params[i], '] is not set.'     
            i = i + 1
        try:
            resp_data = hsm_comms.send_data(buf)
            # #parse resp_data
            #print resp_data
            next_pos=self.header_len
            resp_data[0:next_pos] ## header
            resp_code=resp_data[next_pos:next_pos+2]
            self.response_code.setValue(resp_code) #
            self.error_code.setValue(resp_data[next_pos+2:next_pos+4]) #
            
            if self.error_code.getValue()=="00":
                self.mab.setValue(resp_data[next_pos+4:next_pos+16])
            
            
        except IOError as e:
            print 'MS command execution failed. Reason: ', e
            return None
        except:
            print 'MS command execution failed. Reason: nil',sys.exc_info()
            return None
        

    def dump(self):
        buf = self.command_code.getValue() + ' Request = [\n';
        i = 0
        for param in self.req_param_vals:
            buf += '{0:40s} = <{1}>;\n'.format(MS.req_params[i], param.getValue());
            i = i + 1
               
        buf += ']\n'
        i = 0
        buf += self.command_code.getValue() + ' Response = [\n'
        for param in self.resp_param_vals:
            buf += '{0:40s} = <{1}>;\n'.format(MS.resp_params[i], param.getValue());
            i = i + 1;   
        buf += ']\n'
        
                
        return buf
    

if __name__ == "__main__":
    ms_obj = MS(12)
    ms_obj.params(key='U1034BF4ACB49620EE08F13FB25101A1A', message_block=bytearray.fromhex('00010203040506070809A1B2C3D4E5F6')) 
    ms_obj.lmk_id.setValue('01')
    ms_obj.execute()
    
    # hsm_comms.close()
    
    print ms_obj.dump()
    
    

