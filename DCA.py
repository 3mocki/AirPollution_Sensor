import requests, json
from Msgtype import *
from ResultCode import *
from globalVar import *
from STATE import *

class DCA_class:
    msgtype = SSP_DCAREQ

    lat = '32.88247'
    lng = '-117.23484'
    nat = 'Q30'
    state = 'Q99'
    city = "Q16552"

    payload = {
        "latitude": lat,
        "longitude": lng,
        "tlv": {
            "nation": nat,
            "state": state,
            "city": city
        }
    }

    rcvdPayload = None
    # eId is Sensor Serial Number
    eId = ""
    cId = ""
    MTI = ""
    TTI = ""


    def packedMsg(self):
        packedMsg = {
            "header": {
                "msgType": self.msgtype,  # msgHeader[0]
                "msgLen": len(str(self.payload)),  # msgHeader[1:2]
                "endpointId": self.eId  # msgHeader[3:5]
            },
            "payload": self.payload
        }
        return packedMsg  # return packedMsg

    def setTimer(self):
        global response, rt
        print("Timer Working")
        response = requests.post(url_1, json=self.packedMsg())
        rt = response.elapsed.total_seconds()
        print('(check)rspTime :' + str(rt))
        return rt

    def rcvdMsg(self):
        if rt > 5:
            print("Retry Checking response time")
            self.setTimer()
        else:
            self.verifyMsgHeader()
            if self.rcvdPayload != RES_FAILED:
                print("check")
                return self.rcvdPayload
            else:
                self.rcvdMsg()

    def verifyMsgHeader(self):
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType'] # rcvdMsgType
        rcvdPayload = self.json_response['payload']
        # rcvdLength = len(str(self.rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId'] # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId: # rcvdEndpointId = SSN
            stateCheck = 1
            if stateCheck == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return rcvdPayload
        else:
            return RES_FAILED

    def UnpackMsg(self):
        if self.json_response['payload']['resultCode'] == RESCODE_SSP_DCA_OK: # 4.1
            self.cId = self.json_response['payload']['cId']
            self.MTI = self.json_response['payload']['MTI']
            self.TTI = self.json_response['payload']['TTI']
            return RES_SUCCESS
        else:
            return RES_FAILED

    def init(self):
        print("(check)msgtype : " + str(self.msgtype))
        print("(check)eId(=SSN) : " + str(self.eId))

        self.setTimer()

        t = response.json()
        print('(check)Received Msg : ' + str(t))  # check log
        data = response.text
        self.json_response = json.loads(data)

        self.rcvdMsg()
        self.UnpackMsg()