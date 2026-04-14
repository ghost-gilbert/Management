from pymongo import MongoClient
from studentType import monthIntext, NormaliseText, CapitalizeText, Fright, DepositOnMongo, FetchPreviousDeposit, FetchBalance, FetchPaidMonth, FetchFreight
from time import localtime
from siblings import SiblingClass, FeeVerification
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
client = MongoClient(os.getenv('mongo_db'))
# if __name__ == "__main__":
# Database and Collections that are used
db = client['Management-database']
admission = db['admission']
feecollection = db['feeStructure']
bookfeecollection = db['BookFee']
freightVillages = db['FreightVillages']

session = f"{localtime().tm_year}-{str(localtime().tm_year+1)[2:4]}"

# Inserting a Fee Structure
def feeStructure(standard, feeName, feeAmount, filter_type):
    oneTimefeeData = {}
    monthlyfeeData = {}
    alreadyAvalibleClassList = []
    allClasses = feecollection.find({})
    for i in allClasses:
        alreadyAvalibleClassList.append(i['Class'])
    for std in standard:
        print(std)
        if std in alreadyAvalibleClassList:
            if filter_type=='m':
                getData = feecollection.find_one_and_update({'Class':std}, {"$set": {f"Monthly Fee Detail.{feeName}": feeAmount}})
            else:
                getData = feecollection.find_one_and_update({'Class':std}, {"$set": {f"One Time Fee Detail.{feeName}": feeAmount}})
        # standard = input("Enter the class(eg. NUR, NUR-UKG, 1-5 etc.):")
        else:
            # for i in standard:
            keyS = feeName
            # if keyS == 'exit' or keyS == '':
            #     break
            # filter_type = input("1. M for MonthlyFee\n2. O for OneTimeFee\n-> ")

            # valuE = int(input("Fee Amount(only in integer): "))
            valuE = feeAmount

            if filter_type.lower() == 'm':
                monthlyfeeData.update({f"{keyS}":f"{int(valuE)}"})

            elif filter_type.lower() == 'o':
                oneTimefeeData.update({f"{keyS}":f"{int(valuE)}"})

            document = {
                "Class":std,
                "One Time Fee Detail":oneTimefeeData,
                "Monthly Fee Detail":monthlyfeeData,
            }

            feeded = feecollection.insert_one(document)


# print(feeStructure())

# Fetch Fee Structure
def fetchFeeStructure():
    Objects = feecollection.find({})
    DictionaryList = []
    for i in Objects:
        objectId = i['_id']
        i.update({'_id':str(objectId)})
        DictionaryList.append(i)
    return DictionaryList

# Delete a Fee Structure
def DelFeeStruct(head):
    feecollection.find_one_and_delete({"Class":head})

    return f"Successfully Deleted Class:{head} Structure"

# Inserting Book Fee For Each Class
def setbookfee(standard, amount):
    alreadyExist = bookfeecollection.find_one({'Class':standard})
    if alreadyExist == None:
        document = {
            "Class":standard,
            "Book Charge":int(amount)
        }
        
        feedOnDB = bookfeecollection.insert_one(document)
        return feedOnDB.inserted_id
    else: 
        updatedInfo = bookfeecollection.update_one({'_id':alreadyExist['_id']},{'$set':{'Book Charge':int(amount)}})
        return updatedInfo

def DelBookFee(std):
    bookfeecollection.find_one_and_delete({"Class":std})

    return f"Successfully Deleted Class:{std} Book Fee"
# Docs = feeStructure()
# feeded = feecollection.insert_one(Docs)
# print(feeded.inserted_id)

# Getting Book Detail according to class
def getbookDetail(standard):
    booksFee = bookfeecollection.find({"Class":standard})
    for i in booksFee:
        return i.get("Book Charge")

# Getting Total Fee Detail
def getFeeDetail(standard, *frightAmount):
    # def confirmClass(standard):
    #     if standard in range(1,5+1):
    #         return "1-5"
    #     elif standard in range(6,8+1):
    #         return "6-8"
    #     elif standard in range(9,12+1):
    #         return f"{standard}"
    #     elif standard in ["NUR","LKG","UKG"]:
    #         return "NUR-UKG"
    # listOFstandard = confirmClass(standard)
    getColl = feecollection.find({"Class":standard})
    savedData = {}
    try:
        for i in getColl:
            savedData.update({"One Time Fee Detail":i.get("One Time Fee Detail")})
            try:
                monthlyFeeDetail = i.get("Monthly Fee Detail")
                frightUpdated=monthlyFeeDetail.update({"Freight Fee":f"{int(frightAmount[0])}"})
                print(monthlyFeeDetail)
                savedData.update({"Monthly Fee Detail":monthlyFeeDetail})
            except:
                savedData.update({"Monthly Fee Detail":i.get("Monthly Fee Detail")})
        savedData.update({"Book Charge":getbookDetail(standard)})

        return savedData
    except:
        return savedData

# Get Whole detail of that kid
def getWholeDetail(ID):
    studentDetail = admission.find_one({"_id":ID})
    return studentDetail

def setFright(Address, Charge):
    response = freightVillages.insert_one({Address:Charge})
    return response
    
def getFright():
    FreightList = []
    freightCursor = freightVillages.find({})
    for villages in freightCursor:
        objectId = villages['_id']
        villages.update({'_id':str(objectId)})
        FreightList.append(villages)
    return FreightList

def delFright(objID):
    response = freightVillages.find_one_and_delete({'_id': objID})
    return response

    

def getPaidMonth(name, standard):
    student = admission.find({"Name":name,"Class":standard})
    for keys in student:
        return keys['Paid Month']

class typeOfFee:

    def totalfee(self, ID):
        totalOTFD = 0
        totalMFD = 0

        detail = getWholeDetail(ID)

        feeDetail = detail['Fee Detail']
        otfd = feeDetail['One Time Fee Detail']
        mfd = feeDetail['Monthly Fee Detail']
        paidmonth = detail['Paid Month']
        bookfee = 0 if type(feeDetail['Book Charge'])==type(None) else feeDetail['Book Charge']
        totalOTFD = totalOTFD+bookfee

        for i in otfd:
            totalOTFD = totalOTFD+int(otfd[i])
        for i in mfd:
            totalMFD = totalMFD+int(mfd[i])

        # print((totalMFD*(12-paidmonth))+totalOTFD)

        return [totalMFD, totalOTFD, paidmonth]

    def customMonth(self, ID, month, paidMonth):
        # month = int(fetchMonthNo)-paidMonth
        fakeMonth = int(month)-paidMonth

        print(month)

        PreviousPaidAmount = FetchPreviousDeposit(ID)
        Balance = FetchBalance(ID)
        Paid_Month = FetchPaidMonth(ID)

        # Check for the all fees paid
        showMonth = month
        
        # month = Paid_Month+month
        toTal = self.totalfee(ID)
        
        print(f"'--> {showMonth} month = {((toTal[0]*month) + toTal[1])-PreviousPaidAmount}\n '--> till {monthIntext(month)}")
        return [None,(((toTal[0]*month) + toTal[1])-PreviousPaidAmount), monthIntext(month), ((toTal[1]+(toTal[0]*Paid_Month))-PreviousPaidAmount)-Balance, (toTal[0]*fakeMonth), Balance]

class deposit(typeOfFee):
    def __init__(self, ID):
        self.ID = ID
    
    def depositMoney(self, fetchedNo, paidMonth):
        # It gives: [None, the amount, etc.....]
        certainData = self.customMonth(self.ID, fetchedNo, paidMonth)
        depositedResponse = DepositOnMongo(self.ID, certainData[1])
        admission.find_one_and_update({"_id":self.ID},{"$set":{"Paid Month":fetchedNo}})
        admission.find_one_and_update({"_id":self.ID},{"$set":{"Balance":0}})
        return "success"
        
    def partialDepositMoney(self, fetchedNo, paidMonth, amount):
        # It gives: [None, the amount, etc.....]
        certainData = self.customMonth(self.ID, fetchedNo, paidMonth)
        admission.find_one_and_update({"_id":self.ID},{"$set":{"Paid Month":fetchedNo}})

        leftMoney = amount-certainData[1]
        # Balance
        # When the deposited amount is smaller than the have to be paid amount
        if leftMoney<0:
            print(amount, certainData[1], leftMoney)
            postiveValue = abs(leftMoney)
            depositedResponse = DepositOnMongo(self.ID, amount)
            admission.find_one_and_update({"_id":self.ID},{"$set":{"Balance":postiveValue}})
            return {"success":0}

        # When the deposited amount is bigger than the have to be paid amount
        else:
            print("Lodu Else mein Ja raha hai",amount, certainData[1], leftMoney)
            depositedResponse = DepositOnMongo(self.ID, certainData[1])
            return {"success":leftMoney}


        
class DeleteData:
    def __init__(self, ID):
        self.ID = ID
    
    def DeleteStudent(self):
        deleted = admission.find_one_and_delete({"_id":self.ID})
        print(deleted)
    
    def FieldDeletion(self, key):
        Field = []
        FieldCaption = []

        RawData = admission.find_one({"_id":self.ID})

        for keys in RawData:
            Field.append(keys)
            FieldCaption.append(keys)
            
            if type(RawData[keys]) == type({}):
                for i in RawData[keys]:
                    temp = RawData[keys]
                    def RecursiveIternation(toIternate, *persistingValue):
                        for key in toIternate:
                            if not persistingValue:
                                Field.append(key)
                                FieldCaption.append(f"{keys}.{key}")
                            else:
                                for i in persistingValue:
                                    Field.append(key)
                                    FieldCaption.append(f"{keys}.{i}.{key}")
                            IterableObject = toIternate
                            if type(IterableObject[key]) == type({}):
                                return RecursiveIternation(IterableObject[key],key)
                    RecursiveIternation({i:temp[i]})

            for ind,i in enumerate(range(len(Field))):
                print(f"{ind+1}. {Field[i]}")

        choose = Field.index(key)
        fIndex = FieldCaption[choose]
        admission.find_one_and_update({"_id":self.ID},{"$unset":{fIndex:""}})

def FancyShowDependencie(ID, detail):
    tempID = None
    
    tempFeeObject = typeOfFee()
    distinctFeeList = tempFeeObject.totalfee(ID)
    
    directDictionary = {}
    dummyKeyList = []
    dummyValueList = []
    FeedetailListNo = None


    # This is just for pinting in terminal
    def listingDetail(detail):
        for i in detail.keys():
            dummyKeyList.append(i)
        for i in detail.values():
            dummyValueList.append(i)

    listingDetail(detail)
    # for i in range(len(dummyKeyList)):
    #     print(f"{dummyKeyList[i]}: {dummyValueList[i]}")
    feeDetail = None
    for i in detail:
        if i == 'Fee Detail':
            print(f"'--> {i}:")
            feeDetail = detail.get('Fee Detail')

            for i in feeDetail:
                if type(feeDetail[i])==type(feeDetail):
                    for j in feeDetail[i]:
                        print(f"'   '--> {j}: {feeDetail[i][j]}")
                        directDictionary.update({j:feeDetail[i][j]})
                else:
                    newDepolyment = feeDetail[i]
                    directDictionary.update({i:newDepolyment})

            continue
        print(f"'--> {i}: {CapitalizeText(detail[i])}")
        directDictionary.update({i:CapitalizeText(detail[i])})

        if i == '_id':
            tempID = detail[i]
            newDepolyment = str(detail[i])
            directDictionary.update({i:newDepolyment})
        if i == 'Paid Month':
            isFreight = FetchFreight(tempID)
            if isFreight == 0:
                directDictionary.update({i:f"{monthIntext(detail[i])} Month Fees and Freight Paid"})
            else:
                directDictionary.update({i:f"{monthIntext(detail[i])} Month Fees Paid"})


            print(f"   '-->{monthIntext(detail[i])} Month Fees Paid")
    
    totalAmount = (distinctFeeList[0]*12)+distinctFeeList[1]
    directDictionary.update({"Total": totalAmount})
    # return [dummyKeyList, feeDetail]
    return directDictionary

def SingleFancyShow(ID):
    detail = getWholeDetail(ID)
    dataDict = FancyShowDependencie(ID, detail)
    return dataDict


def ListFancyShow(name, standard):
    listofdetail = admission.find({"Name":name,"Class":standard})
    print(listofdetail)
    ModifiedDetailsList = []
    for detail in listofdetail:
        directDictionary = FancyShowDependencie(name, standard, detail)
        ModifiedDetailsList.append(directDictionary)
    return ModifiedDetailsList