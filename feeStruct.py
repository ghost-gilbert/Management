from pymongo import MongoClient
from studentType import monthIntext

client = MongoClient('mongodb+srv://khc07979_db_user:5Ld8806ZCHOuayLp@claust.3gj3ip7.mongodb.net/?appName=Claust')

# if __name__ == "__main__":
# Database and Collections that are used
db = client['Management-database']
admission = db['admission']
feecollection = db['feeStructure']
bookfeecollection = db['BookFee']

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
def getFeeDetail(standard):
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
class typeOfFee:

    def totalfee(self, name, standard):
        totalOTFD = 0
        totalMFD = 0

        detail = getWholeDetail(name, standard)

        feeDetail = detail['Fee Detail']
        otfd = feeDetail['One Time Fee Detail']
        mfd = feeDetail['Monthly Fee Detail']
        paidmonth = detail['Paid Month']

        for i in otfd:
            totalOTFD = totalOTFD+int(otfd[i])
        for i in mfd:
            totalMFD = totalMFD+int(mfd[i])

        # print((totalMFD*(12-paidmonth))+totalOTFD)

        return [totalMFD, totalOTFD, paidmonth]

    def oneMonth(self, name, standard):
        toTal = self.totalfee(name, standard)
        return f"The total fee of this month is {toTal[0] + toTal[1]}"

    def customMonth(self, name, standard, month):
        toTal = self.totalfee(name, standard)
        return f"--> {month} month = {(toTal[0]*month) + toTal[1]}\n '--> till {monthIntext(toTal[2])}"
    
    def paidMonth_increment(self, name, standard, month):
        increased = admission.update_one({"Name":f"{name}","Class":standard},{"$inc": {"Paid Month":month}})


# tstOBJ = typeOfFee()
# tstOBJ.paidMonth_increment("prag",9,1)

    
