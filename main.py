from pymongo import MongoClient
from feeStruct import getFeeDetail, feeStructure, setbookfee, getWholeDetail, typeOfFee,DelFeeStruct, fetchFeeStructure, DelBookFee, setFright, delFright, deposit, DeleteData, ListFancyShow, SingleFancyShow
from studentType import checkStudentType, NormaliseText, CapitalizeText, monthIntext, Fright, FetchBalance
from siblings import SiblingClass
from supplementaryFunctions import MCDTH
from feeStruct import feeStructure
import time
import json
import os
from dotenv import load_dotenv, dotenv_values, set_key

load_dotenv()
client = MongoClient(os.getenv('mongo_db'))

monthNames = [None, 'Apr','May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']


db = client['Management-database']
collection = db['admission']
freightVillages = db['FreightVillages']
feecollection = db['feeStructure']
bookfeecollection = db['BookFee']

def insertDocs(data, feeDetail, paidmonth):
    document = {"Name":f"{data[0]}", "Father Name":f"{data[1]}","Mother Name":f"{data[2]}", "Village":f"{data[3]}", "Date of Birth":f"{data[4]}", "Mobile No":f"{data[5]}", "Aadhar No":f"{data[6]}", "PEN No":f"{data[7]}", "Student Type":f"{data[8]}", "Class":data[9],"Freight":data[10], "Fee Detail":feeDetail, "Paid Month":paidmonth}
    # document = {"name":"Ghost", "class":"High School"}
    # document = {"name":"Kumar Harsh", "class":"Intermediate"}
    insert_doc = collection.insert_one(document)

    print(f"inserted {insert_doc.inserted_id}")

def Entry(rawData):
    OrganisedList = [NormaliseText(rawData["Name"]),NormaliseText(rawData["Father Name"]), NormaliseText(rawData["Mother Name"]), NormaliseText(rawData["Village"]), rawData["DOB"], rawData["Mobile No"], rawData["Aadhar No"], rawData["PEN No"], rawData["Student Type"], MCDTH(rawData["Class"]), rawData["Freight"]]
    return OrganisedList

    # Name = NormaliseText(input("Student Name: "))
    # FatherName = NormaliseText(input("Father Name: "))
    # MotherName = NormaliseText(input("Mother Name: "))
    # Village = NormaliseText(input("Address: "))
    # dob = input("Date of Birth(dd/mm/yyyy): ")
    # MobileNo = NormaliseText(input("Mobile No: "))
    # Aadhar = input("Aadhar No: ")
    # Pen = input("PEN no: ")
    # standard = int(input("Class: "))
    # studentType = NormaliseText(input("Student Type(NEW or OLD): "))
    # freight = NormaliseText(input("T for Transport\nL for Local: "))
    # , MotherName, Village, dob, MobileNo, Aadhar, Pen

# , name, father_name, mother_name, village, dob, mobile_no, aadhar, pen_no, standard

class WritePersonalData:
    def __init__(self,data):
        self.data = data
        # self.name = "Kumar Harsh"
        # self.father_name = data[1]
        # self.father_name = "Double Chicken"
        # self.mother_name = mother_name
        self.village = data[3]
        # self.dob = dob
        # self.mobile_no = mobile_no
        # self.aadhar = aadhar
        # self.pen_no = pen_no
        self.standard = data[9]
        self.studentType = data[8]
        self.fright = data[10]


    def AdmissionForm(self):
        # detail get's the fee detail and book charge according to standard
        frightAmount = Fright(self.fright, self.village)
        detail = getFeeDetail(MCDTH(self.standard), frightAmount)
        paidmonth = checkStudentType(self.studentType)
        insertDocs(self.data, detail, paidmonth[1])
        

# Printing the Options and Taking Input
# print("Choose what to do:\n1 for Entry\n2 for Find\n3 for Check Fees\n4 for Update Fee Month\n0 for Managing Fee Structure\n-1 for Adding Classwise book Fee")
# print("\r-----------------------------------------------------------------------------------")
# print("  |1|\t |2|\t   |3|\t\t|4|\t\t   |0|\t\t\t|-1|")
# print("|Entry| |Find| |Check Fee| |Update Fee| |Managing Fee Structure| |Adding Book Fee|")
# print("-----------------------------------------------------------------------------------")
# Options = ["1 for Entry","2 for Find","3 for Check Fee","4 for Update Fee", "5 for Fright", "6 for Delete", "0 for Managing Fee Structure", "-1 for Adding Book Fee"]
# for i in Options:
#     print(f"|--> {i}")
# option = input("Choosed Option: ")

def Entry_Function(rawDataDictionary):
    data = Entry(rawDataDictionary)
    obj1 = WritePersonalData(data)
    obj1.AdmissionForm()

def Find_Function(name, standard):
    # name = NormaliseText(input("Student Name: "))
    # standard = int(input("Class: "))
    try:
        # DataList = []
        DataList = ListFancyShow(NormaliseText(name), standard)
        # DataList.append(singleData)
        return DataList
    except:
        return None

def CheckFee_Function(ID, fetchNo):
    data = collection.find_one({"_id": ID})

    SiblingObject = SiblingClass(data["Father Name"], data["Mother Name"], data["Village"])
    response = SiblingObject.CheckSibling()
    FeeObject = typeOfFee()

    if response == None:
        showFee = FeeObject.customMonth(ID, fetchNo, data['Paid Month'])
        balance = FetchBalance(ID)
        TotalAmount = showFee[1]
        return {"One Time Fee": showFee[3], "Monthly Fee": showFee[4], "Paid Month":showFee[2], "Balance":balance, "Total Fee":TotalAmount}
    else:
        TotalAmount = 0
        otf = 0
        mf = 0
        month = None
        showDetail = []
        totalBalance = 0
        for item in response:
            showFee = FeeObject.customMonth(item, fetchNo, data['Paid Month'])
            balance = FetchBalance(item)
            totalBalance = totalBalance+balance
            print(showFee[1])
            TotalAmount = TotalAmount+showFee[1]
            month = showFee[2]
            otf = otf+showFee[3]
            mf = mf+showFee[4]
            print(otf, mf, month)

        print(TotalAmount, month)
        return {"One Time Fee": otf, "Monthly Fee": mf,"Paid Month": month, "Total Fee": TotalAmount, "Balance":totalBalance}

def UpdateFee_Function(ID, monthTxt):
    data = collection.find_one({"_id": ID})

    SiblingObject = SiblingClass(data["Father Name"], data["Mother Name"], data["Village"])
    response = SiblingObject.CheckSibling()
    monthNo = monthNames.index(monthTxt)

    if response == None:
        tempObj = deposit(ID)
        returnedMessage = tempObj.depositMoney(monthNo, data['Paid Month'])
        return [returnedMessage]
    else:
        msgStore = []
        for IDs in response:
            # monthNo = monthNames.index(monthTxt)
            tempObj = deposit(IDs)
            returnedMessage = tempObj.depositMoney(monthNo, data['Paid Month'])
            msgStore.append(returnedMessage)
        return msgStore

def Partial_UpdateFee_Function(ID, monthTxt, amount):
    data = collection.find_one({"_id": ID})

    SiblingObject = SiblingClass(data["Father Name"], data["Mother Name"], data["Village"])
    response = SiblingObject.CheckSibling()
        
    monthNo = monthNames.index(monthTxt)

    if response == None:
        tempObj = deposit(ID)
        returnedMessage = tempObj.partialDepositMoney(monthNo, data['Paid Month'], amount)
        return [list(returnedMessage.keys())[0]]
    else:
        msgStore = []
        subtractedAmount = 0
        isFirst = True
        for IDs in response:
            # monthNo = monthNames.index(monthTxt)
            tempObj = deposit(IDs)
            if isFirst==True:
                returnedMessage = tempObj.partialDepositMoney(monthNo, data['Paid Month'], amount)
            else:
                returnedMessage = tempObj.partialDepositMoney(monthNo, data['Paid Month'], subtractedAmount)

            msgStore.append(list(returnedMessage.keys())[0])
            subtractedAmount=returnedMessage['success']
            isFirst = False
        return msgStore
    

def Fright_Function():
    options = NormaliseText(input("[S]et Fright\n[D]elete Fright\nSelect Letter: "))
    if options == 's':
        setFright()
    elif options == 'd':
        address = NormaliseText(input("Enter Village Name: "))
        print(delFright(address))

def Delete_Cell_Function(ID, key):
    objectOfDeletion = DeleteData(ID)
    objectOfDeletion.FieldDeletion(f"{key}")

def Delete_Student_Function(ID):
    objectOfDeletion = DeleteData(ID)
    objectOfDeletion.DeleteStudent()

def create_FeeStructure_Function(standard, feeName, feeAmount, filter_type):
    feededID = feeStructure(standard, feeName, feeAmount, filter_type)
    newData = feecollection.find_one({"_id":feededID})
    return newData

def delete_FeeStructure_Function(standard):
    DeletedOne = DelFeeStruct(MCDTH(standard))

def createBookStructure_Function(std, amount):
    fed = setbookfee(std, amount)
    return fed

def deleteBookStructure_Function(std):
    DeletedOne = DelBookFee(std)
    return DeletedOne

def fetchBookStructure():
    bookChargeList = []
    Objects = bookfeecollection.find()
    for i in Objects:
        objectId = i['_id']
        i.update({'_id':str(objectId)})
        bookChargeList.append(i)
    return bookChargeList

def ShowDetail():
    allDetail = collection.find({})
    KeyList = []
    # dictionaryList = []
    FinalList = []
    
    for i in allDetail:
        # Name = i['Name']
        # Standard = i['Class']
        ID = i['_id']

        RefinedDetail = SingleFancyShow(ID)
        for key in RefinedDetail:
            try:
                KeyList.index(key)
            except:
                KeyList.append(key)
        FinalList.append(RefinedDetail)

        print(FinalList)
    
    return [KeyList ,FinalList]

class environmentVarible:
    def changeDatabase(newURI):
        modifiedValue = set_key('.env', 'mongo_db', newURI)
        return modifiedValue


            




