import time
from pymongo import MongoClient

client = MongoClient('mongodb+srv://khc07979_db_user:5Ld8806ZCHOuayLp@claust.3gj3ip7.mongodb.net/?appName=Claust')
db = client['Management-database']
freightVillages = db['FreightVillages']
admission = db['admission']

normalMonth = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
schoolMonth = ["Apr","May","June","July","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

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

        # currentMonNum = current.tm_mon - 1
# This is a testing line used for months but by default it will be the current month using time module
        currentMonNum = 5

        currentMonLet = normalMonth[currentMonNum]

        schoolMonthNum = schoolMonth.index(currentMonLet)
        print(schoolMonth[schoolMonthNum])
        print(schoolMonthNum)
        # How many months left for them to pay
        return [len(schoolMonth)-schoolMonthNum, schoolMonthNum]
    else:
        return [12, 0]
    
def monthIntext(number):
    Month = schoolMonth[number-1]
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

def DepositOnMongo(name, standard, DepoAmount, Manualdate=None):
    response = admission.find_one({"Name":name,"Class":standard})
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

        admission.find_one_and_update({"Name":name,"Class":standard},{"$set": {"Deposit": tempDict}})
        return tempDict
    except:
        result = admission.find_one_and_update({"Name":name,"Class":standard},{"$set": {"Deposit": {f"{date}-01":DepoAmount}}})
        return result

def FetchPreviousDeposit(name, standard):
    TempObject = admission.find_one({"Name":name,"Class":standard})
    totalDeposit = 0
    try:
        fetched = TempObject['Deposit']
        for keys in fetched:
            totalDeposit = totalDeposit+fetched[keys]
        return totalDeposit
    except:
        return 0
    
def FetchBalance(name, standard):
    TempObject = admission.find_one({"Name":name,"Class":standard})
    totalBalance = 0
    try:
        fetched = TempObject['Balance']
        for keys in fetched:
            totalBalance = totalBalance+fetched[keys]
        return totalBalance
    except:
        return 0
    
def FetchPaidMonth(name, standard):
    TempObj = admission.find_one({"Name":name,"Class":standard})
    paidMonth = TempObj['Paid Month']
    return paidMonth









