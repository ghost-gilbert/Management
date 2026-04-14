from pymongo import MongoClient
import os
from dotenv import load_dotenv, dotenv_values, set_key

load_dotenv()
client = MongoClient(os.getenv('mongo_db'))

db = client['Management-database']
admission = db['admission']

class SiblingClass:
    def __init__(self, father_name, mother_name, village):
        self.father = father_name        
        self.mother = mother_name        
        self.village = village   

    def CheckSibling(self):
        rawData = admission.find({"Father Name":self.father,"Mother Name":self.mother,"Village":self.village})
        TempList = []
        for i in rawData:
            TempList.append(i['_id'])
        if len(TempList) == 1:
            return None
        else:
            return TempList
    
    def CheckSiblingName(self):
        rawData = admission.find({"Father Name":self.father,"Mother Name":self.mother,"Village":self.village})
        TempDict = {}
        for i in rawData:
            TempDict.update({i['Name']:i['Class']})
        if len(TempDict) == 1:
            return None
        else:
            return TempDict
    
def giveSibling(ID):
    StudentData = admission.find_one({"_id":ID})
    TempSibObj = SiblingClass(StudentData['Father Name'],StudentData['Mother Name'],StudentData['Village'])
    siblings = TempSibObj.CheckSiblingName()
    return siblings
    
def FeeVerification(name, std):
    student = admission.find_one({"Name":name,"Class":std})

    totalOTFD = 0
    totalMFD = 0

    feeDetail = student['Fee Detail']
    otfd = feeDetail['One Time Fee Detail']
    mfd = feeDetail['Monthly Fee Detail']
    paidmonth = student['Paid Month']
    bookfee = 0 if type(feeDetail['Book Charge'])==type(None) else feeDetail['Book Charge']
    totalOTFD = totalOTFD+bookfee
    deposit = student['Deposit']
    depositValue = 0

    for i in otfd:
        totalOTFD = totalOTFD+int(otfd[i])
    for i in mfd:
        totalMFD = totalMFD+int(mfd[i])
    for i in deposit:
        depositValue = depositValue+deposit[i]

    totalFee = (totalMFD*12)+totalOTFD

    # print((totalMFD*(12-paidmonth))+totalOTFD)
    # print("Total Fee: ",totalFee, "Deposit: ",depositValue)
    # print("Left Amount: ",totalFee-depositValue)
    # return [totalMFD, totalOTFD, paidmonth]
    if totalFee!=depositValue:
        print(f"Fees Completely not Paid\nBalance: {totalFee-depositValue}")
        return totalFee-depositValue
    else:
        print(f"Fees Completely Paid\nBalance: {totalFee-depositValue}")
        return totalFee-depositValue

