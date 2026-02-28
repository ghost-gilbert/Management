from pymongo import MongoClient
from feeStruct import getFeeDetail, feeStructure, setbookfee, getWholeDetail, typeOfFee,DelFeeStruct, fetchFeeStructure, fetchBookFee, DelBookFee
from studentType import checkStudentType, NormaliseText, CapitalizeText, monthIntext

schoolMonth = ["Apr","May","June","July","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

def heart():
    client = MongoClient('mongodb+srv://khc07979_db_user:5Ld8806ZCHOuayLp@claust.3gj3ip7.mongodb.net/?appName=Claust')

    db = client['Management-database']
    collection = db['admission']

    def insertDocs(data, feeDetail, paidmonth):
        document = {"Name":f"{data[0]}", "Father Name":f"{data[1]}","MotherName":f"{data[2]}", "Village":f"{data[3]}", "Date of Birth":f"{data[4]}", "Mobile No.":f"{data[5]}", "Aadhar No.":f"{data[6]}", "Pen":f"{data[7]}", "Student Type":f"{data[8]}", "Class":data[9], "Fee Detail":feeDetail, "Paid Month":paidmonth}
        # document = {"name":"Ghost", "class":"High School"}
        # document = {"name":"Kumar Harsh", "class":"Intermediate"}
        insert_doc = collection.insert_one(document)

        print(f"inserted {insert_doc.inserted_id}")

    def Entry():
        Name = NormaliseText(input("Student Name: "))
        FatherName = NormaliseText(input("Father Name: "))
        MotherName = NormaliseText(input("Mother Name: "))
        Village = NormaliseText(input("Address: "))
        dob = input("Date of Birth(dd/mm/yyyy): ")
        MobileNo = NormaliseText(input("Mobile No: "))
        Aadhar = input("Aadhar No: ")
        Pen = input("PEN no: ")
        standard = int(input("Class: "))
        studentType = NormaliseText(input("Student Type(NEW or OLD): "))
        return [Name, FatherName,MotherName, Village, dob, MobileNo, Aadhar, Pen, studentType, standard]
        # , MotherName, Village, dob, MobileNo, Aadhar, Pen

    # , name, father_name, mother_name, village, dob, mobile_no, aadhar, pen_no, standard

    class WritePersonalData:
        def __init__(self,data):
            self.data = data
            # self.name = "Kumar Harsh"
            # self.father_name = data[1]
            # self.father_name = "Double Chicken"
            # self.mother_name = mother_name
            # self.village = village
            # self.dob = dob
            # self.mobile_no = mobile_no
            # self.aadhar = aadhar
            # self.pen_no = pen_no
            self.standard = data[9]
            self.studentType = data[8]


        def AdmissionForm(self):
            # detail get's the fee detail and book charge according to standard
            detail = getFeeDetail(int(self.standard))
            paidmonth = checkStudentType(self.studentType)
            insertDocs(self.data, detail, paidmonth[1])
            print(detail)
            # print(type(detail))
            

    # Printing the Options and Taking Input
    # print("Choose what to do:\n1 for Entry\n2 for Find\n3 for Check Fees\n4 for Update Fee Month\n0 for Managing Fee Structure\n-1 for Adding Classwise book Fee")
    print("\r-----------------------------------------------------------------------------------")
    print("  |1|\t |2|\t   |3|\t\t|4|\t\t   |0|\t\t\t|-1|")
    print("|Entry| |Find| |Check Fee| |Update Fee| |Managing Fee Structure| |Adding Book Fee|")
    print("-----------------------------------------------------------------------------------")
    option = input("Choosed Option: ")

    # Inserting Fee Structure
    def FeeStruct():
        feeInserted = feeStructure()
        print(feeInserted)

    # data Entry and Object Definition for form Filling
    if option == '1':
        data = Entry()
        obj1 = WritePersonalData(data)
        obj1.AdmissionForm()
    elif option == '2':
        detail = getWholeDetail(NormaliseText(input("Student Name: ")),int(input("Class: ")))
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
                    # print(i)
                    # print(feeDetail[i])
                    # print(type(feeDetail[i]))
                    if type(feeDetail[i])==type(feeDetail):
                        for j in feeDetail[i]:
                            print(f"'   '--> {j}: {feeDetail[i][j]}")
                continue
            print(f"'--> {i}: {CapitalizeText(detail[i])}")
            if i == 'Paid Month':
                print(f"   '-->{monthIntext(detail[i])} Month Fees Paid")

        
    elif option == '3':
        fetchNo = int(input("How many months of fee you want to fetch\n: "))
        FeeObject = typeOfFee()
        if fetchNo == 1:
            showFee = FeeObject.oneMonth(NormaliseText(input("Name: ")),int(input("Class: ")))
            print(showFee)
        if fetchNo != 1:
            showFee = FeeObject.customMonth(NormaliseText(input("Name: ")),int(input("Class: ")),fetchNo)
            print(showFee)
    elif option == '4':
        pass

    elif option == '0':
        options = input("1 For Creating Structure\n2 For Deleting Structure: ")
        if options == "1":
            FeeStruct()
        elif options == "2":
            print("Avalible Fee Structures")
            fetchFeeStructure()
            DeletedOne = DelFeeStruct(input("Which Fee Structure(Ex. 6-8, 1-5 etc.): "))
            print(DeletedOne)
            
    elif option == '-1':
        options = input("1 For Creating Book Fee\n2 For Deleting Book Fee: ")
        if options == "1":
            standard = int(input("Enter Class: "))
            fed = setbookfee(standard)
            print(fed)
        elif options == "2":
            print("Avalible Book Fee Class")
            fetchBookFee()
            DeletedOne = DelBookFee(int(input("Which class Book Fee: ")))
            print(DeletedOne)
    elif option == 'exit':
        print("Good Luck!")
        return None

    return heart()



            




