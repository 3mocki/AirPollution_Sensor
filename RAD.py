import requests, json
from Msgtype import *
# from STATE import *
# from ResultCode import *
from globalVar import *
# from Database import MySqlite

class RAD_class:
    # msgHeader[0]
    msgtype = SSP_RADTRN

    payload = {
        "airQualityDataListEncodings": {
            "dataTupleLen": '10',
            "airQualityDataTuples": [[1541124718,'32.879184,-117.235084','Q30','Q99','Q16552', 25, 55.54, 68.73, 12.32, 93.03, 94.07, 77.51, 322, 387, 277, 348, 219, 90],
                                  [1541124719,'32.879184,-117.235084','Q30','Q99','Q16552', 30, 16.58, 98.36, 21.42, 75.43, 70.07, 28.12, 53, 40, 255, 403, 158, 467],
                                  [1541124720,'32.879184,-117.235084','Q30','Q99','Q16552', 28, 91.92, 42.14, 58.7, 6.65, 97.91, 68.7, 344, 116, 448, 230, 156, 57],
                                  [1541124721,'32.879184,-117.235084','Q30','Q99','Q16552', 26, 85.88, 87.2, 79.81, 33.93, 64.07, 96.37, 248, 464, 355, 480, 439, 230],
                                  [1541124722,'32.879184,-117.235084','Q30','Q99','Q16552', 22, 94.64, 94.86, 85.42, 19.4, 88.71, 94.4, 467, 298, 167, 23, 131, 116],
                                  [1541124723,'32.879184,-117.235084','Q30','Q99','Q16552', 23, 45.63, 58.65, 3.31, 55.48, 48.44, 12.92, 261, 455, 198, 73, 231, 442],
                                  [1541124724,'32.879184,-117.235084','Q30','Q99','Q16552', 25, 82.85, 97.31, 82.87, 2.59, 74.83, 29.52, 256, 240, 371, 264, 441, 118],
                                  [1541124725,'32.879184,-117.235084','Q30','Q99','Q16552', 23, 59.41, 28.66, 3.89, 84.15, 9.97, 51.88, 58, 345, 259, 350, 151, 200],
                                  [1541124726,'32.879184,-117.235084','Q30','Q99','Q16552', 22, 90.74, 43.26, 2.66, 29.11, 95.92, 48.27, 142, 173, 409, 95, 256, 150],
                                  [1541124727,'32.879184,-117.235084','Q30','Q99','Q16552', 27, 16.98, 69.75, 86.26, 93.86, 6.71, 88.37, 243, 139, 255, 456, 325, 139]]
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