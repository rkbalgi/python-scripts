#!/usr/bin/python

## A set of utils to generate rsa keys, validate and generate rsa signatures

import socket,struct,binascii

OK="00"

## hsm ip/port details
hsmIp="127.0.0.1"
hsmPort=9999

## for signature generation
## the below is not required if the private key is in hsm storage
privateKey=binascii.unhexlify('27D36664C124C00AB4500135B4B58994D4E3BC952B534EF9611431BEDB4C55C2AC70E3CD75AA8DFD8A2956506DE9FD11D5BABBA6A572A710B9C6B78CF8CDEC3549977218599D09D27B699775DB2BDC2D7BC555005F01E852EAC4ED19EB3CE44913BD8A887019F96D80521920AB64F68593630A6A98833AE4B9247EFA704EDEB8CF3451EA1FC52D0E99D19709DBF4A7668FF7EB6B3D5AC8DA94E965C32EB874BAD86E02DC3F7D34F4F9D89DB2F12E14C84D95F7B051138BCD4B3639EFC9CD725E51943C27A1B5D9EE9C280D351018E8ABD63E7E2E4B53EF22ABBAAB70CA9224802611EE388793539E98C69E91A4365F046B2C40A12DF49FE18800599907913F9808049C0FCDDD023F4C621DB7413EC124C2CA4D00F9C0BF2977AF53A20BF4DA6C823218BE00225DE09C038DBC99D43788ED996023CA46B452A2C8CBF83AA2BD96F73EBD8A5017E80CDFB5728D3B26089A9F67E7416A13A9F8')


publicKey=binascii.unhexlify('308188028180BE14D6AE9F2AB650835847F8787C737338E991730A7B77EC4FD6788DAAB69A8F3EA29100E24A0F56F17511966B6C14110B4659C7A35258730FC9495E37EF046F8DDB1EF5ED86716081F826FA9B620850697D26FAFB4CAA86E99607B1163F020E443E084905080F700C4BC590991F652F2A4BCCAD458AF5F2F75E2CD33618CF570203010001')
#mac on the RSA public key
mac = binascii.unhexlify('5434cd1e');


## if the private key is used from hsm storage then the below variable should just have the value of the slot - for example - privateKeyInfo='00'
privateKeyInfo='99'+'{0:04d}'.format(len(privateKey))+privateKey

##lmk id
lmkId='00'

rawData='RSA Signature Input - Daalitoy '

## for verification
signature=binascii.unhexlify('27fbb4479b1a4041eb590bb6b3260c43209b5e3c91027c686f95cd46f49610bc51dfd06e37f3518b87faeac99824a518708eb28946628afde9831181e9078b8ce2837a50c8ffdc801197ba0c6166b31a67beb604d1419264b812fa3ed6cb8ee27c19096be7f0b1d00c01ea07548a2c2467bfb1b5eceb0de262c6f223751a8895')


##hsm command strings
ewCmd='000000000001EW060101'+'{0:04d}'.format(len(rawData))+rawData+';'+privateKeyInfo+'%'+lmkId
eyCmd='000000000002EY060101'+'{0:04d}'.format(len(signature))+signature+';'+'{0:04d}'.format(len(rawData))+rawData+';'+mac+publicKey+'~'+'%'+lmkId
ncCmd="000000000001NC"
e0Cmd='000000000000EO01'+publicKey+'~'+'%'+lmkId

def generate_mac_on_rsa_public_key():
        cmd=e0Cmd
        sock=socket.create_connection((hsmIp,hsmPort))
        if sock!=None:
                pLen=struct.pack('!H',len(cmd))
                finalCmd=pLen+cmd
                print "e0 command = {0}".format(binascii.hexlify(finalCmd))
                sock.send(finalCmd)

                data=sock.recv(2)
                if data!=None and len(data)==2:
                        pLen=struct.unpack('!H',data)
                        print 'response length = ',pLen[0]
                        data=sock.recv(pLen[0])
                        print 'response = '+binascii.hexlify(data)
                        responseCode=data[14:16]
                        if responseCode==OK:
                                mac=data[16:20]
                                importedPublicKey=data[20:]
                                print 'mac = '+binascii.hexlify(mac)
                                print 'imported key = '+binascii.hexlify(importedPublicKey)
                        else:
                                print 'hsm call (E0) failed. response code = '+responseCode
                        sock.close()

## end


def verify_signature():
        cmd=eyCmd
        sock=socket.create_connection((hsmIp,hsmPort))
        if sock!=None:
                pLen=struct.pack('!H',len(cmd))
                finalCmd=pLen+cmd
                print "ey command = {0}".format(binascii.hexlify(finalCmd))
                sock.send(finalCmd)

                data=sock.recv(2)
                if data!=None and len(data)==2:
                        pLen=struct.unpack('!H',data)
                        print 'response length = ',pLen[0]
                        data=sock.recv(pLen[0])
                        print 'response = '+binascii.hexlify(data)
                        responseCode=data[14:16]
                        if responseCode==OK:
                                print 'signature verification ok.'
                        else:
                                print 'hsm call (EY) failed (signature verification failed). response code = '+responseCode
                        sock.close()

## end

if __name__=="__main__":

        #generate_mac_on_rsa_public_key();
        verify_signature();
        exit(0);

        cmd=ewCmd
        sock=socket.create_connection((hsmIp,hsmPort))
        if sock!=None:
                pLen=struct.pack('!H',len(cmd))
                finalCmd=pLen+cmd
                print "command = {0}".format(binascii.hexlify(finalCmd))
                sock.send(finalCmd)

                data=sock.recv(2)
                if data!=None and len(data)==2:
                        pLen=struct.unpack('!H',data)
                        print 'response length = ',pLen[0]
                        data=sock.recv(pLen[0])
                        print 'response = '+binascii.hexlify(data)
                        responseCode=data[14:16]
                        if responseCode==OK:
                                signatureLen=data[16:20]
                                signature=data[20:20+128]
                                print 'signature = '+binascii.hexlify(signature)
                                print 'writing signature to file .. temp.sig'
                                sigFile=open('temp.sig','w')
                                sigFile.write(signature)
                                sigFile.close()
                        else:
                                print 'hsm call (EW) failed. response code = '+responseCode
                        sock.close()

        else:
                print 'unable to open connection to hsm ('+hsmIp+':'+hsmPort+')'

#command = 01a0303030303030303030303031455730363031303130303338525341205369676e617475726520496e707574202d20416d65726963616e20457870726573733b39393033343427d36664c124c00ab4500135b4b58994d4e3bc952b534ef9611431bedb4c55c2ac70e3cd75aa8dfd8a2956506de9fd11d5babba6a572a710b9c6b78cf8cdec3549977218599d09d27b699775db2bdc2d7bc555005f01e852eac4ed19eb3ce44913bd8a887019f96d80521920ab64f68593630a6a98833ae4b9247efa704edeb8cf3451ea1fc52d0e99d19709dbf4a7668ff7eb6b3d5ac8da94e965c32eb874bad86e02dc3f7d34f4f9d89db2f12e14c84d95f7b051138bcd4b3639efc9cd725e51943c27a1b5d9ee9c280d351018e8abd63e7e2e4b53ef22abbaab70ca9224802611ee388793539e98c69e91a4365f046b2c40a12df49fe18800599907913f9808049c0fcddd023f4c621db7413ec124c2ca4d00f9c0bf2977af53a20bf4da6c823218be00225de09c038dbc99d43788ed996023ca46b452a2c8cbf83aa2bd96f73ebd8a5017e80cdfb5728d3b26089a9f67e7416a13a9f8253030
#response length =  148
#response = 303030303030303030303031455830303031323827fbb4479b1a4041eb590bb6b3260c43209b5e3c91027c686f95cd46f49610bc51dfd06e37f3518b87faeac99824a518708eb28946628afde9831181e9078b8ce2837a50c8ffdc801197ba0c6166b31a67beb604d1419264b812fa3ed6cb8ee27c19096be7f0b1d00c01ea07548a2c2467bfb1b5eceb0de262c6f223751a8895
#signature = 27fbb4479b1a4041eb590bb6b3260c43209b5e3c91027c686f95cd46f49610bc51dfd06e37f3518b87faeac99824a518708eb28946628afde9831181e9078b8ce2837a50c8ffdc801197ba0c6166b31a67beb604d1419264b812fa3ed6cb8ee27c19096be7f0b1d00c01ea07548a2c2467bfb1b5eceb0de262c6f223751a8895

#DER Sequence
#    Integer(-46289614555128044229053993964856826820779864508756005652062932223068228595549917598752603150056635333477563705457363445468819616473845497620925631753763518126119442017749183466288382725424747820534570296357361440593483480398328092705792934075291582023711778240872391492546680582035583659072781220117330997417)
#    Integer(65537)

#Public Key (DER) : [308188028180BE14D6AE9F2AB650835847F8787C737338E991730A7B77EC4FD6788DAAB69A8F3EA29100E24A0F56F17511966B6C14110B4659C7A35258730FC9495E37EF046F8DDB1EF5ED86716081F826FA9B620850697D26FAFB4CAA86E99607B1163F020E443E084905080F700C4BC590991F652F2A4BCCAD458AF5F2F75E2CD33618CF570203010001]
#Private Key (LMK): [27D36664C124C00AB4500135B4B58994D4E3BC952B534EF9611431BEDB4C55C2AC70E3CD75AA8DFD8A2956506DE9FD11D5BABBA6A572A710B9C6B78CF8CDEC3549977218599D09D27B699775DB2BDC2D7BC555005F01E852EAC4ED19EB3CE44913BD8A887019F96D80521920AB64F68593630A6A98833AE4B9247EFA704EDEB8CF3451EA1FC52D0E99D19709DBF4A7668FF7EB6B3D5AC8DA94E965C32EB874BAD86E02DC3F7D34F4F9D89DB2F12E14C84D95F7B051138BCD4B3639EFC9CD725E51943C27A1B5D9EE9C280D351018E8ABD63E7E2E4B53EF22ABBAAB70CA9224802611EE388793539E98C69E91A4365F046B2C40A12DF49FE18800599907913F9808049C0FCDDD023F4C621DB7413EC124C2CA4D00F9C0BF2977AF53A20BF4DA6C823218BE00225DE09C038DBC99D43788ED996023CA46B452A2C8CBF83AA2BD96F73EBD8A5017E80CDFB5728D3B26089A9F67E7416A13A9F8]

