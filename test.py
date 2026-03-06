def setFright():
    finalDictionary = {}
    while True:
        Address = input("Village: ")
        Charge = input("Transport Fees: ")
        if Address == "":
            break
        finalDictionary.update({Address:Charge})
    
    finalDictionary

# 'Fee Detail': {
#     'One Time Fee Detail': {'Computer Charge': '700', 'Accessories': '350', 'Maintainance': '300', 'Admission': '1000'},
#     'Monthly Fee Detail': {'Monthly Fee': '500', 'Freight': '350'},
#     'Book Charge': None
#     }
