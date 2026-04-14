import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
client = MongoClient(os.getenv('mongo_db'))
db = client['Management-database']
freightVillages = db['FreightVillages']
admission = db['admission']

normalMonth = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
schoolMonth = ["Apr","May","June","July","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

monthNames = [None, 'Apr','May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']

def currentDate():
    date = f"{time.localtime().tm_mday}/{time.localtime().tm_mon}/{time.localtime().tm_year}"
    return date

def letterIncrement(value):
    match len(value):
        case 1:
            return f"0{value}"
        case _:
            return value

def checkStudentType(student_type):
    if student_type == 'new':
        current = time.localtime()

        currentMonNum = current.tm_mon - 1
# This is a testing line used for months but by default it will be the current month using time module
        # currentMonNum = 5

        currentMonLet = normalMonth[currentMonNum]

        schoolMonthNum = schoolMonth.index(currentMonLet)
        print(schoolMonth[schoolMonthNum])
        print(schoolMonthNum)
        # How many months left for them to pay
        return [len(schoolMonth)-schoolMonthNum, schoolMonthNum]
    else:
        return [12, 0]
    
def monthIntext(number):
    Month = monthNames[number]
    return Month

def NormaliseText(text):
    noSpace = text.strip()
    smallLetter = noSpace.lower()

    return smallLetter

def CapitalizeText(text):
    if type(text) != type("str"):
        return text
    capital = text.capitalize()
    return capital

def Fright(fright, *village):
    if fright == "t":
        allVillage = freightVillages.find({})
        for i in allVillage:
            for ind, mykey in enumerate(i.keys()):
                if ind==1:
                    if mykey==village[0]:
                        return i[f"{mykey}"]
    else:
        return None


def DepositOnMongo(ID, DepoAmount, Manualdate=None):
    response = admission.find_one({"_id":ID})
    date = currentDate()
    try:
        PreviousDeposit = response["Deposit"]
        tempDict = {}
        finalDate = date if Manualdate==None else Manualdate
        tempkeyList = []
        matched = 0

        for ind,key in enumerate(PreviousDeposit):
            tempkeyList.append(key[0:-2])
            tempDict.update({key:PreviousDeposit[key]})

        for i in tempkeyList:
            matched=matched+1
        tempDict.update({f"{finalDate}-{letterIncrement(str(matched+1))}":DepoAmount})

        admission.find_one_and_update({"_id":ID},{"$set": {"Deposit": tempDict}})
        return tempDict
    except:
        result = admission.find_one_and_update({"_id":ID},{"$set": {"Deposit": {f"{date}-01":DepoAmount}}})
        return result

def FetchPreviousDeposit(ID):
    TempObject = admission.find_one({"_id":ID})
    totalDeposit = 0
    try:
        fetched = TempObject['Deposit']
        for keys in fetched:
            totalDeposit = totalDeposit+fetched[keys]
        return totalDeposit
    except:
        return 0
    
def FetchBalance(ID):
    TempObject = admission.find_one({"_id":ID})
    try:
        fetched = TempObject['Balance']
        return fetched
    except:
        return 0

def FetchPaidMonth(ID):
    TempObj = admission.find_one({"_id":ID})
    paidMonth = TempObj['Paid Month']
    return paidMonth

def FetchFreight(ID):
    TempObj = admission.find_one({"_id":ID})
    Freight = None
    try:
        Freight = TempObj['Freight']
    except:
        Freight = 0
    return Freight










