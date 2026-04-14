# class convert str to int if it is not NUR, LKG, UKG, data type, 
# multipleClassDataTypeHandler = MCDTH
lowerPrimary = ['NUR', 'LKG', 'UKG']
def MCDTH(standard):
    try:
        return standard.upper()
    except:
        return int(standard)
