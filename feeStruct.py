from pymongo import MongoClient
from studentType import monthIntext, NormaliseText, CapitalizeText, Fright, DepositOnMongo, FetchPreviousDeposit, FetchBalance, FetchPaidMonth
from time import localtime
from siblings import SiblingClass, FeeVerification

client = MongoClient('mongodb+srv://khc07979_db_user:5Ld8806ZCHOuayLp@claust.3gj3ip7.mongodb.net/?appName=Claust')

# if __name__ == "__main__":
# Database and Collections that are used
db = client['Management-database']
admission = db['admission']
feecollection = db['feeStructure']
bookfeecollection = db['BookFee']
freightVillages = db['FreightVillages']

session = f"{localtime().tm_year}-{str(localtime().tm_year+1)[2:4]}"

# Inserting a Fee Structure
def feeStructure():
    oneTimefeeData = {}
    monthlyfeeData = {}
    standard = input("Enter the class(eg. NUR, NUR-UKG, 1-5 etc.):")
    while True:
        keyS = input("[Type'exit']Fee Type: ")
        if keyS == 'exit' or keyS == '':
            break
        filter_type = input("1. M for MonthlyFee\n2. O for OneTimeFee\n-> ")

        valuE = int(input("Fee Amount(only in integer): "))

        if filter_type.lower() == 'm':
            monthlyfeeData.update({f"{keyS}":f"{int(valuE)}"})

        elif filter_type.lower() == 'o':
            oneTimefeeData.update({f"{keyS}":f"{int(valuE)}"})

    document = {
        "Class":standard,
        "One Time Fee Detail":oneTimefeeData,
        "Monthly Fee Detail":monthlyfeeData,
    }

    feeded = feecollection.insert_one(document)

    return feeded.inserted_id

# print(feeStructure())

# Fetch Fee Structure
def fetchFeeStructure():
    Objects = feecollection.find()
    for i in Objects:
        print(f"'--> {i["Class"]}")

# Delete a Fee Structure
def DelFeeStruct(head):
    feecollection.find_one_and_delete({"Class":head})

    return f"Successfully Deleted Class:{head} Structure"

# Inserting Book Fee For Each Class
def setbookfee(standard):
    fee = int(input(f"For Class {standard} the fee will be: "))
    document = {
        "Class":standard,
        "Book Charge":fee
    }
    
    feedOnDB = bookfeecollection.insert_one(document)
    return feedOnDB.inserted_id

def fetchBookFee():
    Objects = bookfeecollection.find()
    for i in Objects:
        print(f"'--> {i["Class"]}")

def DelBookFee(head):
    bookfeecollection.find_one_and_delete({"Class":head})

    return f"Successfully Deleted Class:{head} Book Fee"
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
    def confirmClass(standard):
        if standard in range(1,5+1):
            return "1-5"
        elif standard in range(6,8+1):
            return "6-8"
        elif standard in range(9,12+1):
            return f"{standard}"
        elif standard in ["NUR","LKG","UKG"]:
            return "NUR-UKG"
    listOFstandard = confirmClass(standard)
    getColl = feecollection.find({"Class":listOFstandard})
    savedData = {}
    for i in getColl:
        savedData.update({"One Time Fee Detail":i.get("One Time Fee Detail")})
        try:
            monthlyFeeDetail = i.get("Monthly Fee Detail")
            frightUpdated=monthlyFeeDetail.update({"Freight":f"{int(frightAmount[0])}"})
            print(monthlyFeeDetail)
            savedData.update({"Monthly Fee Detail":monthlyFeeDetail})
        except:
            savedData.update({"Monthly Fee Detail":i.get("Monthly Fee Detail")})
    savedData.update({"Book Charge":getbookDetail(standard)})

    return savedData

# Get Whole detail of that kid
def getWholeDetail(name, standard):
    studentDetail = admission.find({"Name":name,"Class":standard})
    for i in studentDetail:
        # print(i['_id'])
        studentDetail = admission.find({"_id":i["_id"]})

        keysStudentDetail = []
        listOFDetail = []
        
        for j in studentDetail:
            return j
            for i in j.keys():
                keysStudentDetail.append(i)
            for i in j.values():
                listOFDetail.append(i)
            # for i in range(len(keysStudentDetail)):
            #     print(f"{keysStudentDetail[i]}: {listOFDetail[i]}")

    # return [keysStudentDetail,listOFDetail]s

def FancyShow(name, standard):
    detail = getWholeDetail(name, standard)
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
            continue
        print(f"'--> {i}: {CapitalizeText(detail[i])}")
        if i == 'Paid Month':
            print(f"   '-->{monthIntext(detail[i])} Month Fees Paid")
    
    return [dummyKeyList, feeDetail]

def setFright():
    while True:
        Address = NormaliseText(input("Village: "))
        Charge = input("Transport Fees: ")
        if Address == "":
            break
        response = freightVillages.insert_one({Address:Charge})
        print(response)
    
def delFright(village):
    allVillage = freightVillages.find({})
    for i in allVillage:
        # print(i)
        for ind, mykey in enumerate(i.keys()):
                # print(ind)
            if ind==1:
                if mykey==village:
                    print(mykey,i[f"{mykey}"])
                    resoponse = freightVillages.find_one_and_delete({mykey:i[f"{mykey}"]})
                    return resoponse

def getPaidMonth(name, standard):
    student = admission.find({"Name":name,"Class":standard})
    for keys in student:
        return keys['Paid Month']

class typeOfFee:

    def totalfee(self, name, standard):
        totalOTFD = 0
        totalMFD = 0

        detail = getWholeDetail(name, standard)

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

    # def oneMonth(self, name, standard):
    #     PreviousPaidAmount = FetchPreviousDeposit(name, standard)
    #     month = FetchPaidMonth(name, standard)+1
    #     toTal = self.totalfee(name, standard)
    #     return f"The total fee of this month is {((toTal[0] + toTal[1])*month)-PreviousPaidAmount}"

    def customMonth(self, name, standard, month):
        PreviousPaidAmount = FetchPreviousDeposit(name, standard) # 9000
        showMonth = month   # 4
        month = FetchPaidMonth(name, standard)+month
        toTal = self.totalfee(name, standard)
        if month >= 12:
            leftMonth = 12-FetchPaidMonth(name,standard) 
            if leftMonth==0:
                print(f"All Fees Paid for the session {session}")
            print(f"Only {leftMonth} Month Fees left to pay in this Session of {session}")
            return [f"--> {leftMonth} month = {((toTal[0]*12) + toTal[1])-PreviousPaidAmount}\n '--> till {monthIntext(12)}",None]
        else:
            return [f"'--> {showMonth} month = {((toTal[0]*month) + toTal[1])-PreviousPaidAmount}\n '--> till {monthIntext(month)}",((toTal[0]*month) + toTal[1])-PreviousPaidAmount,monthIntext(month)]

    def customMonthRaw(self, name, standard, month):
        toTal = self.totalfee(name, standard)
        return [f"--> {month} month = {(toTal[0]*month) + toTal[1]}\n '--> till {monthIntext(toTal[2])}",(toTal[0]*month) + toTal[1]]
    
    # def paidMonth_increment(self, name, standard, month):
    #     increased = admission.update_one({"Name":f"{name}","Class":standard},{"$inc": {"Paid Month":month}})
    #     return increased

class DepositeFees(typeOfFee):
    def __init__(self, name, standard):
        self.name = name
        self.standard = standard
        super().__init__()
    def UpdateFeePreText(self):
        paidMonth = getPaidMonth(self.name,self.standard)
        if paidMonth == 12:
            FeeVerification(self.name, self.standard)
            return None
        DepoAmount = int(input("Enter the Deposit Amount: "))
        previosDeposit = FetchPreviousDeposit(self.name, self.standard)
        balance = FetchBalance(self.name, self.standard)
        MixPay = DepoAmount+previosDeposit
        ToBePaid = 0
        while ToBePaid<=MixPay:
            MonthFetch = super().customMonthRaw(self.name, self.standard, paidMonth)
            ToBePaid = MonthFetch[1]
            if ToBePaid>=MixPay:
                break
            if paidMonth==12:
                print("Deposited Amount is More than the Total Amount\nSo the fee for this session has been closed\nLeft amount will be returned to the customer")
                break
            paidMonth = paidMonth+1

        if DepoAmount>(ToBePaid-previosDeposit):
            amount = super().customMonthRaw(self.name, self.standard, paidMonth)
            RefinedAmount = amount[1]-previosDeposit
            print(f"{RefinedAmount+balance} is left in the session {session}")
            return [RefinedAmount+balance,paidMonth, DepoAmount, None]
        else:
            amount = super().customMonthRaw(self.name, self.standard, paidMonth-1)
            extraAmount = super().customMonthRaw(self.name, self.standard, paidMonth)
            RefinedAmount = amount[1]-previosDeposit
            RefinedExtraAmount = extraAmount[1]-previosDeposit
            if paidMonth==0:
                print(f"{RefinedAmount+balance} for Admission can be paid currently")
            else:
                print(f"{RefinedAmount+balance} for {paidMonth-1}th month can be paid currently")
            print(f"but {RefinedExtraAmount+balance} for {paidMonth}th month can be paid if the deposit amounts are increased")
            return [RefinedAmount+balance,RefinedExtraAmount+balance,paidMonth, DepoAmount]
    
    def SiblingUpdateFeePreText(self, CollectedAmount, otherSibling):
        paidMonth = getPaidMonth(self.name,self.standard)
        if paidMonth == 12:
            FeeVerification(self.name, self.standard)
            return None
        DepoAmount = int(input(f"Left: ({CollectedAmount-otherSibling}) Enter the Deposit Amount: "))
        while DepoAmount>CollectedAmount-otherSibling:
            DepoAmount = int(input(f"Amount is greater than the collective deposit (only {collectedAmount-otherSibling})\nPlease re-enter the deposit value: "))
        previosDeposit = FetchPreviousDeposit(self.name, self.standard)
        balance = FetchBalance(self.name, self.standard)
        MixPay = DepoAmount+previosDeposit
        ToBePaid = 0
        while ToBePaid<=MixPay:
            MonthFetch = super().customMonthRaw(self.name, self.standard, paidMonth)
            ToBePaid = MonthFetch[1]
            if ToBePaid>=MixPay:
                break
            if paidMonth==12:
                print("Deposited Amount is More than the Total Amount\nSo the fee for this session has been closed\nLeft amount will be returned to the customer")
                break
            paidMonth = paidMonth+1

        if DepoAmount>(ToBePaid-previosDeposit):
            amount = super().customMonthRaw(self.name, self.standard, paidMonth)
            RefinedAmount = amount[1]-previosDeposit
            print(f"{RefinedAmount+balance} is left in the session {session}")
            return [RefinedAmount+balance,paidMonth, DepoAmount, None]
        else:
            amount = super().customMonthRaw(self.name, self.standard, paidMonth-1)
            extraAmount = super().customMonthRaw(self.name, self.standard, paidMonth)
            RefinedAmount = amount[1]-previosDeposit
            RefinedExtraAmount = extraAmount[1]-previosDeposit
            if paidMonth!=0:
                print(f"{RefinedAmount+balance} for {paidMonth-1}th month can be paid currently")
            else:
                print(f"{RefinedAmount+balance} for Admission can be paid currently")
            print(f"but {RefinedExtraAmount+balance} for {paidMonth}th month can be paid if the deposit amounts are increased")
            return [RefinedAmount+balance,RefinedExtraAmount+balance,paidMonth, DepoAmount]
    
    def DepositAndBalanceHandling(self):
        PreValue = self.UpdateFeePreText()
        if PreValue == None:
            print(f"All Fees paid for session {session}")
        elif PreValue[3]==None:
            DepositOnMongo(self.name, self.standard, PreValue[0])
            admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[1]}})
            admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":0}})
            leftAmount = PreValue[2]-PreValue[0]
            print(f"Amount to Return {leftAmount}")
        else:
            # [RefinedAmount+balance,RefinedExtraAmount+balance,paidMonth, DepoAmount]
            option = NormaliseText(input(f"[F]ull Payment {PreValue[0]}\n[P]artial Payment {PreValue[3]}\n:- "))
            if option == 'p':
                DepositOnMongo(self.name, self.standard, PreValue[3])
                balanceAmount = PreValue[1]-PreValue[3]
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":balanceAmount}})
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[2]}})
            else:
                DepositOnMongo(self.name, self.standard, PreValue[0])
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[2]}})
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":0}})

    def SiblingDepositAndBalanceHandling(self, PreValue):
        if PreValue == None:
            print(f"All Fees paid for session {session}")
        elif PreValue[3]==None:
            DepositOnMongo(self.name, self.standard, PreValue[0])
            admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[1]}})
            admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":0}})
            leftAmount = PreValue[2]-PreValue[0]
            print(f"Amount to Return {leftAmount}")
        else:
            # option = NormaliseText(input("[F]ull Payment\n[P]artial Payment\n:- "))
            option = NormaliseText(input(f"[F]ull Payment {PreValue[2]}\n[P]artial Payment {PreValue[3]}\n:- "))
            if option == 'p':
                DepositOnMongo(self.name, self.standard, PreValue[3])
                balanceAmount = PreValue[1]-PreValue[3]
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":balanceAmount}})
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[2]}})
            else:
                DepositOnMongo(self.name, self.standard, PreValue[0])
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Paid Month":PreValue[2]}})
                admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$set":{"Balance":0}})
                if PreValue[3]>PreValue[0]:
                    return PreValue[3]-PreValue[0]

    def SiblingVerification(self):
        data = admission.find_one({"Name": self.name,"Class":self.standard})
        SiblingObject = SiblingClass(data["Father Name"], data["Mother Name"], data["Village"])
        response = SiblingObject.CheckSibling()
        if response == None:
            self.UpdateFeePreText()
        else:
            CollectiveDeposit = int(input("Enter the total deposit amount: "))
            Values = {}
            otherSibling = 0
            for key in response:
                # key = name, response[key] = class
                self.name = key
                self.standard = response[key]
                updateInfo = self.SiblingUpdateFeePreText(CollectiveDeposit,otherSibling)
                if updateInfo == None:
                    pass
                elif updateInfo[3] == None:
                    otherSibling = otherSibling+updateInfo[2]
                else:
                    otherSibling = otherSibling+updateInfo[3]
                Values.update({self.name:updateInfo})
                ExtraMoney = self.SiblingDepositAndBalanceHandling(updateInfo)
                if ExtraMoney != None:
                    CollectiveDeposit = CollectiveDeposit+ExtraMoney
            print(f"{Values}")
            if CollectiveDeposit==otherSibling:
                pass
            else:
                print(f"Left Amount: {CollectiveDeposit-otherSibling}")
        
class DeleteData:
    def __init__(self, name, standard):
        self.name = name
        self.standard = standard
    
    def DeleteStudent(self):
        deleted = admission.find_one_and_delete({"Name":self.name,"Class":self.standard})
        print(deleted)
    
    def FieldDeletion(self):
        Field = []
        FieldCaption = []

        RawData = admission.find_one({"Name":self.name,"Class":self.standard})

        for keys in RawData:
            # print(f"{numbering}. {keys}")
            Field.append(keys)
            FieldCaption.append(keys)
            
            if type(RawData[keys]) == type({}):
                for i in RawData[keys]:
                    temp = RawData[keys]
                    def RecursiveIternation(toIternate, *persistingValue):
                        for key in toIternate:
                            if not persistingValue:
                                # print(f"{keys}.{key}")
                                Field.append(key)
                                FieldCaption.append(f"{keys}.{key}")
                            else:
                                for i in persistingValue:
                                    # print(f"{keys}.{i}.{key}")
                                    Field.append(key)
                                    FieldCaption.append(f"{keys}.{i}.{key}")
                            IterableObject = toIternate
                            # print(IterableObject[key])
                            if type(IterableObject[key]) == type({}):
                                return RecursiveIternation(IterableObject[key],key)
                    RecursiveIternation({i:temp[i]})

            for ind,i in enumerate(range(len(Field))):
                print(f"{ind+1}. {Field[i]}")

        choose = input("Enter the Serial No of the field to Delete\n: ")
        index = FieldCaption[(int(choose))-1]
        admission.find_one_and_update({"Name":self.name,"Class":self.standard},{"$unset":{index:""}})