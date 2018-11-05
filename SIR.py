import random, requests, json
from uuid import getnode as get_mac
from Msgtype import *
from ResultCode import *
from globalVar import *
from STATE import *

class SIR_class:
    mac = get_mac()  # 1.3 WiFi MAC Address
    hexmac = hex(mac).split('x')[1]
    # 1.2 msgHeader[0]
    msgtype = SSP_SIRREQ
    # 1.5 msgHeader[1:2]
    payload = {
        "wmac": str(hexmac)
    }

    # 1.1 Generate Temporary SID(randomly generated by a sensor)
    eId = random.randrange(1, 10 ** 3)

    ssn =""

    # 1.0 packedMsg
    def packedMsg(self):
        # 1.5 packedMsg include Header and Payload
        packedMsg = {
            "header": {
                "msgType" : self.msgtype,
                "msgLen" : len(str(self.payload)), # 1.4 size(msgPayload)
                "endpointId" : self.eId # 1.2 msgHeader[3:5]
            },
            "payload" : self.payload
        }
        return packedMsg # 1.6 return packedMsg

    def setTimer(self):
        global response, rt
        print("Timer Working")
        response = requests.post(url_1, json=self.packedMsg())  # 2.2 fnSendMsg => json
        rt = response.elapsed.total_seconds()
        print('(check)rspTime :' + str(rt))
        return rt

    # 3.1 fnRecvMsg()
    def rcvdMsgPayload(self):
        if rt > 5:
            print("Retry Checking response time")
            self.setTimer()  # 3.2 => go to setTimer 2.0
        else:
            self.verifyMsgHeader()
            if rcvdPayload != RES_FAILED:
                print("check")
                return rcvdPayload

    def verifyMsgHeader(self): # 3.3.1
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType'] # rcvdMsgType
        rcvdPayload = self.json_response['payload']
        # rcvdLength = len(str(rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId'] # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId: # rcvdEndpointId = fnGetTemporarySensorId
            stateCheck = 1
            if stateCheck == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return rcvdPayload
        else:
            return RES_FAILED

    def UnpackMsg(self):
        if self.json_response['payload']['resultCode'] == RESCODE_SSP_SIR_OK: # 4.1
            self.ssn = self.json_response['payload']['ssn'] # 4.2
            print("(check)ssn :" + str(self.ssn))
        else:
            if self.json_response['payload']['resultCode'] == RESCODE_SSP_SIR_CONFLICT_OF_TEMPORARY_SENSOR_ID:
                self.setTimer()
            else:
                print("check quit")
                quit()

    def init(self):
        print('(check)mac : ' + str(self.hexmac))
        print('(check)msgtype : ' + str(self.msgtype))
        print('(check)eId : ' + str(self.eId))

        self.setTimer()

        t = response.json()
        print('(check)Received Msg : ' + str(t))  # check log
        data = response.text
        self.json_response = json.loads(data)

        self.rcvdMsgPayload()
        self.UnpackMsg()