import os
from PIL import Image
from io import BytesIO

homeDirectory = os.path.expanduser('~')

try:
    os.mkdir(f"{homeDirectory}/Documents/School Data/income-certificate")
    os.mkdir(f"{homeDirectory}/Documents/School Data/caste-certificate")
    os.mkdir(f"{homeDirectory}/Documents/School Data/domicile-certificate")
except:
    pass

def modifyName(oldName, newName):
    nameArray = oldName.split('.')
    return f"newName.{nameArray[-1]}"


def saveCertificate(fileStorage, location,fileName):
    fileLocation = f"{homeDirectory}/Documents/School Data/{location}/{fileName}"
    fileStorage.save(fileLocation)

