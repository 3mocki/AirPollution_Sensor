import requests, json
from Msgtype import *
# from STATE import *
# from ResultCode import *
from globalVar import *
from Database import MySqlite

class RAD_class:

    row=[0,0,0,0,0,0,0,0,0,0]

    # msgHeader[0]
    msgtype = SSP_RADTRN

    # Collect per 1 sec
    payload = {
        "airQualityDataListEncodings": {
            "dataTupleLen": '10',
            "airQualityDataTuples": row
        }
    }

    # msgHeader[3:5]
    eId=""

    def packedMsg(self):
        packedMsg = {
            "header": {
                "msgType": self.msgtype,
                "msgLen" : len(str(self.payload)),
                "endpointId": self.eId
            },
            "payload": self.payload
        }
        return packedMsg

    def setTimer(self):
        print("Timer Working")
        response = requests.post(url_2, json=self.packedMsg())
        # print('RAD-ACK => ', response.json())
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
        db=MySqlite('RAD')
        db.connectDB()
        db.getData()

        self.data = db.data

        #print('RAD-init() => ', self.data)
        for i in range(0, 10):
            self.row[i] = [self.data[i][1], geo_1, geo_2, geo_3, geo_4, self.data[i][2], self.data[i][3], self.data[i][4], self.data[i][5], self.data[i][6], self.data[i][7], self.data[i][8], self.data[i][9], self.data[i][10], self.data[i][11], self.data[i][12], self.data[i][13], self.data[i][14]]
            print('RAD_class self.row['+str(i)+'] => '+ str(self.row[i]))

        print("(check)msgtype : " + str(self.msgtype))
        print("(check)eId(=cId) : " + str(self.eId))

        self.setTimer()
        db.deleteData()
        db.closeDB()