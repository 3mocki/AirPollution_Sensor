from SIR import SIR_class
from DCA import DCA_class
# from RAD import RAD_class

if __name__ == '__main__':
    print("-----------Generate SIR-----------")
    sir = SIR_class()
    sir.init()

    print("-----------Generate DCA-----------")
    dca = DCA_class()
    dca.eId = sir.ssn
    dca.init()
    #
    # print("-----------Generate RAD-----------")
    # rad = RAD_class()
    # rad.eId = dca.cId
    # rad.init()