from warden.config import Directories
import warden.globals
import os

import re
import argparse

def Enum(**enums):
    return type('Enum', (), enums)

def GetLoginInformation():
    with open ("%s\\login.txt" % (Directories.config)) as login:
        username = login.readline().rstrip('\n')
        password = login.readline().rstrip('\n')
    return (username, password)

def Remove_RTF(buffer):
    buffer = re.sub(r'^\r?\n?$', "", buffer)
    buffer = re.sub(r'\\.*?}', "", buffer)
    buffer = re.sub(r'{.*', "", buffer)
    buffer = re.sub(r'}', "", buffer)
    buffer = re.sub(r'\\.*', "", buffer)
    #Kill the headers
    buffer = re.sub(r'Date.*',"", buffer) #Headers
    #buffer = re.sub(r'^.*(PAPA|Report).*$', "", buffer, flags=re.MULTILINE)
    #buffer = re.sub(r'^.*\d{2}/\d{2}/\d{4}\s-\s\d{2}/\d{2}/\d{4}.*$', "", buffer, flags=re.MULTILINE)
    buffer = re.sub(r'^.*Total.*$', "", buffer)
    buffer = re.sub(r'^[\s]*$', "", buffer) #cleanup buffers
    buffer = re.sub(r'^[0-9|a-z|A-Z]{3,7}\s{7,9}', "", buffer)
    buffer = re.sub(r'^\s{41}', "", buffer) #Trailing whitespace by Total
    buffer = re.sub(r'^\s*$', "", buffer, flags=re.MULTILINE)
    """
    buffer = re.sub(r'^\r?\n?$', "", buffer)
    buffer = re.sub(r'\\.*?}', "", buffer)
    buffer = re.sub(r'{.*', "", buffer)
    buffer = re.sub(r'}', "", buffer)
    buffer = re.sub(r'\\.*', "", buffer)
    """
    return buffer

def DateRange_Args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range", nargs=2,
    help="The date range of the report in format MMDDYYYY ex: 01012013")

    args = parser.parse_args()
    return args

def _warden_date(obj):
    #TODO: Fix this horrible wtf code.
    if not type(obj) is str:
        raise Exception("Not string")
    else:
        if len(obj) != 8:
            raise Exception("Not 8")
        else:
            for c in obj:
                try:
                    c = int(c)
                except:
                    raise Exception("Not Digit")

    return True


def Get_DateRange(args=None):
    #The following code in a multiline string is not supported as SecureCRT
    #does not allow logon script arguments. Here we'll just use a wrapper
    #of GetRangeFromTxt in the meantime.
   #
   #     CURRENTLY UNSUPPORTED IN SECURECRT. 
   # if not args:
   #     args = DateRange_Args()
   # else:

    args = GetRangeFromTxt("range.txt")
    args = [args[0].rstrip('\n'), args[1].rstrip('\n')]
    #
    #for date in args:
       # if not _warden_date(date):
       #     raise warden.globals.InvalidDateFormat(
       #              "Not in correct MMDDYYYY format")
    #return (date[0], date[1])
    return args


def StringFromTxt(file, data=None):
    if (data is None):
        return str(open("%s\\%s" % (Directories.config, file), "r").readline().rstrip('\n'))
    else:
        txt = open(Directories.config + "\\" + file, "wt")
        txt.write(data)
        txt.close()
        return data
def GetRangeFromTxt(file, lst=None):
    if (lst is None):
        val = []
        txt = open(Directories.config + "\\" + file, "r")
        for line in txt:
            val.append(line)
        txt.close()
        return val
    else:
        txt = open(Directories.config + "\\" + file, "wt")
        for line in lst:
            txt.write(str(line) + "\n")
        txt.close()
        return lst