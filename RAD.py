import requests, json
from Msgtype import *
from STATE import *
from ResultCode import *
from globalVar import *
from Database import MySqlite

class RAD_class:

    currentAirData = [1538291581, 24, 25, 26, 27, 28, 29, 34, 35, 36, 37, 38, 39, 40, 32.112223, -10.222422]

    # msgHeader[0]
    msgtype = SSP_RADTRN

    paylaod = {
        "dataTupleLen" : '3',
        "airQualityDataTuple" : [
        	[1538291581, 24, 25, 26, 27, 28, 29, 34, 35, 36, 37, 38, 39, 40, 32.112223, -10.222422],
            [1538291582, 24, 25, 26, 27, 28, 29, 34, 35, 36, 37, 38, 39, 40, 32.112223, -10.222422],
            [1538291583, 24, 25, 26, 27, 28, 29, 34, 35, 36, 37, 38, 39, 40, 32.112223, -10.222422]
        ]
    }

    # msgHeader[3:5]
    eId=""

    def packedMsg(self):
        packedMsg = {
            "header": {
                "msgType" : self.msgtype,
                "msgLen" : len(str(self.payload)),
                "endpointId" : self.eId
            },
            "payload" : self.payload
        }
        return packedMsg

    def setTimer(self):
        print("Timer")
        response = requests.post(url_2, json=self.packedMsg())  # 2.2 fnSendMsg => json
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

    # def UnpackMsg(self):


    def init(self):
        print("(check)msgtype : " + str(self.msgtype))
        print("(check)eId(=cId) : " + str(self.eId))

        self.setTimer()