from flask import Flask, render_template, request, jsonify, redirect
from main import ShowDetail, Entry_Function, Find_Function, Delete_Cell_Function, Delete_Student_Function, CheckFee_Function, UpdateFee_Function, Partial_UpdateFee_Function, create_FeeStructure_Function, delete_FeeStructure_Function, fetchBookStructure, createBookStructure_Function,deleteBookStructure_Function
from feeStruct import DeleteData, fetchFeeStructure, setFright, getFright, delFright
from siblings import giveSibling
from studentType import NormaliseText, CapitalizeText, FetchPaidMonth, FetchBalance
from supplementaryFunctions import MCDTH
import json
from bson.objectid import ObjectId
from fileHandeling import modifyName, saveCertificate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

msgKeyPoint = ['success', 'error', 'message']
# {"Data Feeded Successfully":"success","No Data Found":"error","The system wants to tell something":"message"}
wholeMsg = ['Data Feeded Successfully','No Data Found','The system wants to tell something']

@app.route("/")
def Dashboard():
    runShowDetail = ShowDetail()
    # heading = runShowDetail[0]
    values = runShowDetail[1]
    # heading = ["Student Name","Father Name","Mother Name","Address"]
    # values = {"Name":"Kumar Harsh","Father Name":"Avadhesh","Mother Name":"Malvika","Address":"Karah Pithihiya"}
    return render_template('datatable.html', ValueDict = values)

@app.route("/reload")
def reload():    
    runShowDetail = ShowDetail()
    # heading = runShowDetail[0]
    values = runShowDetail[1]
    # heading = ["Student Name","Father Name","Mother Name","Address"]
    # values = {"Name":"Kumar Harsh","Father Name":"Avadhesh","Mother Name":"Malvika","Address":"Karah Pithihiya"}
    return values

# @app.route("/Registration", methods=['POST'])
@app.route("/", methods=['POST'])
def FindStudent():
    formData= request.form
    RequiredDataList = []
    for i in formData:
        RequiredDataList.append(formData[i])
    print(RequiredDataList)
    values = Find_Function(RequiredDataList[0],int(RequiredDataList[1]))
    print(values)
    # return render_template("datatable.html",ValueDict = Data)
    return render_template('datatable.html', ValueDict = values)

@app.route("/Registration", methods=['GET','POST'])
def Register():
    return render_template('entry.html')

@app.route("/accept-form", methods=['GET','POST'])
def acceptform():
    registrationform = request.form
    Entry_Function(registrationform)
    return redirect('/')

@app.route("/files", methods=['GET','POST'])
def fileVisiting():
    ID = request.args.get('id')
    return render_template('uploadFiles.html', uniqueId=ID)

@app.route("/file-upload", methods=['GET','POST'])
def fileUpload():
    formData = request.form
    fileData = request.files['file']
    # for i in formData:
        # modifyName()
    print(formData)
    print(fileData)
    return {"result": {"File Sucessfully Uploaded":"success"}}

@app.route("/pay", methods=['GET','POST'])
def feeFigure():
    name = request.args.get("name")
    std = request.args.get("class")
    stringID = request.args.get("ID")
    ID = ObjectId(stringID)

    tempCont = {}
    data = giveSibling(ID)
    print(data)
    tempCont.update({"sibs":data})
    tempCont.update({"Name":name,"Class":std})

    monthNames = [None, 'Apr','May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']

    month = FetchPaidMonth(ID)
    balance = FetchBalance(ID)

    print(month, balance)
    print(month!=12)
    print(balance!=0)

    NamedMonth = {}

    while month!=12:
        month = month+1
        NamedMonth.update({month:monthNames[month]})
    else:
        if balance != 0:
            NamedMonth.update({month:monthNames[month]})


    tempCont.update({'payingMonths':NamedMonth})
    tempCont.update({'userID':str(ID)})

    print(tempCont)
    return render_template('checkfee.html', siblingsDict=tempCont)

@app.route("/month", methods=['GET','POST'])
def monthDataFetch():
    data = request.get_json()
    ID = ObjectId(data['ID'])
    details = CheckFee_Function(ID, int(data['fetchNo']))
    return jsonify(details)

@app.route("/payment", methods=['GET','POST'])
def fullPayment():
    data = request.get_json()
    userID = ObjectId(data['ID'])
    print(f"Data: {data}")
    print(f"USER ID: {userID}")
    if userID == "None":
        return jsonify({"No Data Found":"error"})

    serverReturned = UpdateFee_Function(userID, data['paidMonthtxt'])
    print(serverReturned)

    finalMessage = {}
    for i in serverReturned:
        index = msgKeyPoint.index(i)
        finalMessage.update({wholeMsg[index]:msgKeyPoint[index]})
    return jsonify({"result":finalMessage})
    # return jsonify({"result":"Successful"})
    # return jsonify({"result":{"Data Feeded Successfully":"success","No Data Found":"error","The system wants to tell something":"message"}})

@app.route("/partialPayment", methods=['GET','POST'])
def partialPayment():
    data = request.get_json()
    print("I am called Partial Payment")
    userID = ObjectId(data['ID'])
    amount = data['Amount']
    print(userID)
    serverReturned = Partial_UpdateFee_Function(userID, data['paidMonthtxt'], int(amount))
    print(serverReturned)

    finalMessage = {}
    for i in serverReturned:
        index = msgKeyPoint.index(i)
        finalMessage.update({wholeMsg[index]:msgKeyPoint[index]})
    return jsonify({"result":finalMessage})
    # return jsonify({"result":{wholeMsg[0]:msgKeyPoint[0]}})

@app.route("/feeStructure", methods=['GET','POST'])
def feeStructure():
    return render_template('feeStructure.html')

@app.route("/createFeeStructure", methods=['GET','POST'])
def createFeeStructure():
    data = request.get_json()
    std = data['class']
    newData = create_FeeStructure_Function(std, CapitalizeText(data['feeName']), int(data['feeAmount']), data['feeType'])
    return jsonify({"result": {"success":"The Fee Structure Has been Inserted"}})

@app.route("/deleteFeeStructure", methods=['GET','POST'])
def deleteFeeStructure():
    data = request.get_json()
    print(data)
    newData = delete_FeeStructure_Function(data['std'])
    return jsonify({"result": {"success":"The Fee Structure Has been Deleted"}})

@app.route("/fetchFeeStructure", methods=['GET','POST'])
def getFeeStructure():
    getData = fetchFeeStructure()
    return jsonify({"result": getData})

@app.route("/bookcharge", methods=['GET','POST'])
def bookCharge():
    return render_template('bookcharge.html')

@app.route("/createbookCharge", methods=['GET','POST'])
def createBookCharge():
    data = request.get_json()
    std = data['class']
    newData = createBookStructure_Function(std, int(data['feeAmount']))
    return jsonify({"result": {"success":"The Fee Structure Has been Inserted"}})

@app.route("/deletebookCharge", methods=['GET','POST'])
def deleteBookCharge():
    data = request.get_json()
    print(data)
    newData = deleteBookStructure_Function(data['std'])
    return jsonify({"result": {"success":"The Fee Structure Has been Deleted"}})

@app.route("/fetchbookCharge", methods=['GET','POST'])
def getBookCharge():
    getData = fetchBookStructure()
    return jsonify({"result": getData})
    
@app.route("/buscharge", methods=['GET','POST'])
def busCharge():
    return render_template('buscharge.html')

@app.route("/createbusCharge", methods=['GET','POST'])
def createBusCharge():
    data = request.get_json()
    addr = data['village']
    newData = setFright(NormaliseText(addr), int(data['feeAmount']))
    return jsonify({"result": {"success":"The Fee Structure Has been Inserted"}})

@app.route("/deletebusCharge", methods=['GET','POST'])
def deleteBusCharge():
    data = request.get_json()
    objectConversion = ObjectId(data['objID'])
    newData = delFright(objectConversion)
    return jsonify({"result": {"success":"The Fee Structure Has been Deleted"}})

@app.route("/fetchbusCharge", methods=['GET','POST'])
def getBusCharge():
    getData = getFright()
    return jsonify({"result": getData})

@app.route("/studentPanel", methods=['GET','POST'])
def studentInformation():
    data = request.get_json()
    return "Hellio Mate"

@app.route("/delete/cell", methods=['GET','POST'])
def deleteCell():
    data = request.get_json()
    print(data)
    Delete_Cell_Function(data['name'],data['std'],data['key'])
    return "Field Successfully Deleted"

@app.route("/delete/student", methods=['GET','POST'])
def deleteStudent():
    data = request.get_json()
    print(data)
    Delete_Student_Function(data['name'],data['std'])
    return "Student Successfully Deleted"

@app.route("/settings", methods=['GET','POST'])
def settings():
    return render_template('settings.html')

app.run(debug=True)