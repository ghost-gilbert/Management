import time

normalMonth = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
schoolMonth = ["Apr","May","June","July","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

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
    Month = schoolMonth[number]
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


