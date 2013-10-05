import psutil
import os
import webbrowser
from win32com.client import Dispatch
from time import sleep
from warden.config import Directories
import re
import socket
from functools import wraps

def retry(max_tries, exceptions=(Exception,), delay=0):  
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries = range(max_tries)
            tries.reverse()
            for tries_remaining in tries:
                try:
                    print "in attempt", tries_remaining
                    sleep(delay)
                    return func(*args, **kwargs)
                except exceptions, e:
                    if tries_remaining == 0:
                        raise
                else:
                    break
        return wrapper
    return decorator

def _get_proc(proc_name):
    for p in psutil.get_process_list():
        if p.name.lower() == proc_name.lower():
            return p

@retry(10, exceptions=socket.timeout, delay=5)
def _wait_for_proc_load(proc_name):
    if not _get_proc(proc_name):
        raise Exception("Expected process did not start correctly.")


@retry(3, exceptions=socket.timeout)
def retry_connection_active(market):
    return _connection_active(market)

def _connection_active(market):
    s = socket.socket()
    ip = _session_ip(market.name, market.stores[0].session_name)
    try:
        s.settimeout(3)
        s.connect((ip, 22))
        return len(s.recv(1024)) > 0
    
    finally:
        s.close()
        #return False

def _wait_for_nc_connect(ip, attempts=0, max_attempts=10):
    s = socket.socket()
    try:
        s.settimeout(3)
        s.connect((ip, 22))
        if len(s.recv(1024)) > 0:
            return True
    except socket.timeout:
        s.close()
        if attempts > max_attempts:
            return False
        else:
            return _wait_for_nc_connect(ip, attempts=attempts + 1)
    return True


def _Get_SecureCRT_Proc():
    for p in psutil.get_process_list():
        if p.name.lower() == "securecrt.exe": return p
    return None
def _Get_NetworkConnect_Proc():
    for p in psutil.get_process_list():
        if p.name == "dsNetworkConnect.exe": return p
    return None

def _EmulateLogin(username, browser=None):

    
    ie = browser if browser else Dispatch("InternetExplorer.Application")
    ie.Visible = 1
    ie.Navigate("https://pjfc.papajohns.com/")

    while ie.ReadyState != 4: sleep(1) #Load the page fully
    doc = ie.Document
    while doc.readyState != "complete": sleep(1) #Load the document
    if doc.forms[0].name == "frmBrowse": #User was signed in already
        ie.Navigate("https://pjfc.papajohns.com/dana-na/auth/logout.cgi")
        while ie.ReadyState != 4: sleep(1) #Load the page fully
        doc = ie.Document
        while doc.readyState != "complete": sleep(1)
        ie.Navigate("https://pjfc.papajohns.com")

        while ie.ReadyState != 4: sleep(1) #Load the page fully
        doc = ie.Document
        while doc.readyState != "complete": sleep(1) #Load the document
   

    doc.forms[0].Elements[1].click()

    while ie.ReadyState != 4: sleep(1) #Load the page fully
    doc = ie.Document
    while doc.readyState != "complete": sleep(1) #Load the document
#for e in doc.forms[0].Elements:
    #   print e
    doc.forms[0].username.value = username
    doc.forms[0].password.value = "papajohns"

    doc.forms[0].submit()
    while ie.ReadyState != 4: sleep(1) #Load the page fully
    doc = ie.Document
    while doc.readyState != "complete": sleep(1) #Load the document

    print "form name is: ", doc.forms[0].name
    if doc.forms[0].name == "frmConfirmation":
        print "In confirmation..."
        for f in doc.forms:
            print f

        doc.forms[0].Elements[0].click()
        while doc.readyState != "complete": sleep(1)
        

def valid_connection(market):
    return Valid_Connection(market) #until I fix all files

def Valid_Connection(market):
    if _get_proc("dsNetworkConnect.exe"):
        ip = _session_ip(market.name, market.stores[0].session_name)
        return _wait_for_nc_connect(ip, 999) #only checks connection once
    else:
        return False

def _session_ip(market_name, session_name):
    with open("%s\sessions\%s\%s.ini" 
            % (Directories.config, market_name, session_name), 'r') as f:
        for line in f:
            if "Hostname" in line:
                return line.split('=')[1].strip()

def _get_pjfc_username(market):
    try:
        with open("%s\sessions\%s\pjfcusername.txt"
            % (Directories.config, market.name)) as username:
            return username.readline().strip()
    except IOError:
        return raw_input("Enter Megapath username: ")

def Establish_VPN_Connection(market):
    #Get atleast 2 ip addresses to ping from the market to test for connection
    
    ip = _session_ip(market.name, market.stores[0].session_name)
    username = _get_pjfc_username(market)
   
    print "Using PJFC Username: %s" % username
    ie = _get_window()
    if ie:
        print "Found login instance. Attempting to gracefully exit."
        ie.Navigate("https://pjfc.papajohns.com/dana-na/auth/logout.cgi")
        while ie.ReadyState != 4: sleep(1)        
    nc = _get_proc("dsNetworkConnect.exe")
    if nc:
        print "Restarting Network Connect Process..."
        nc.kill()
        nc = None
    else:
        print "NC Gracefully exited."

    _EmulateLogin(username, browser=ie)
    _wait_for_proc_load("dsNetworkConnect.exe")

    print "Network Connect Process running..."
    print "Looking for connection..."
    #return _retry_connection_active(market)
    return _wait_for_nc_connect(ip)
   

def _get_window():
    shellwindows_guid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
    for sw in Dispatch(shellwindows_guid):
        if sw.LocationName.strip() == "Papa Johns Remote Access - Home":
            return sw