import requests, json
from Msgtype import *
from STATE import *
from ResultCode import *
from globalVar import *
from Database import MySqlite

class RAD_class:

    air = MySqlite()


    currentAirData = {'1993-01-04', '30', '1000', '15000', '20000', '300000', '5000', '100', '30', '30', '20', '10', '5', '30'  }

    # msgHeader[0]
    msgtype = SSP_RADTRN

    # msgHeader[1:2]
    payload_1 = {
        "EAQDLT": EAQDLT
    }
    payload_2 = {
        "AQDLT": AQLT
    }

    # msgHeader[3:5]
    eId=""

    def packedMsg(self):
        if self.currentAirData == None:
            return self.currentAirData
            quit()
        else:
            if len(self.currentAirData) > EDS:
                payload = self.payload_1
            else:
                payload = self.payload_2
        packedMsg = {
            "header": {
                "msgType" : self.msgtype,
                "msgLen" : len(str(self.payload)),
                "endpointId" : self.eId
            },
            "payload" : self.payload
        }
        return packedMsg # 1.6 return packedMsg

    def setTimer(self):
        print("Timer")
        response = requests.post(url, json=self.packedMsg())  # 2.2 fnSendMsg => json
        rt = response.elapsed.total_seconds()
        print('(check)rspTime :' + str(rt))
        return rt

    def rcvdMsg(self):
        if self.rt > 5:
            print("Retry Checking response time")
            self.setTimer()  # 3.2
        else:
            self.verifyMsgHeader()
            if rcvdPayload != RES_FAILED:
                print("(check)RES_FAILED")
                self.rt=0
                return rcvdPayload
            else:
                self.rcvdMsg()

    def verifyMsgHeader(self):
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType'] # rcvdMsgType
        self.rcvdPayload = self.json_response['payload']
        rcvdLength = len(str(self.rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId'] # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId: # rcvdEndpointId = SSN
            stateCheck = HALF_SSN_INFORMED_STATE
            if stateCheck == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return self.rcvdPayload
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
        print("(check)eId(=cId) : " + str(self.eId))

        self.setTimer()