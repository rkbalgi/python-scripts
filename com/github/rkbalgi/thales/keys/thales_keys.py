KEY_TYPE_PIN='001'
KEY_TYPE_MAC='003'

SINGLE_LEN_KEY_SIZE=8
DOUBLE_LEN_KEY_SIZE=16

# creates a key representation by 
# appending the key_scheme
def key_repr(scheme,key_str):
    
    if len(key_str)==SINGLE_LEN_KEY_SIZE*2:
        return key_str
    elif len(key_str)==DOUBLE_LEN_KEY_SIZE*2:
        return   scheme+key_str
    else:
        raise Exception('invalid key size')
    
    