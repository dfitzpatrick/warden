import os
import re
import warden
import warden.util
from warden.globals import InvalidMarketException
from warden.config import Directories


def Market_List():
    __, markets, __ = os.walk(Directories.config + "\\sessions").next()
    return [Market(m) for m in markets]

def Seq_to_Market_List(seq):
    markets = []
    for o in seq:
        m = Market(o)
        markets.append(m)
    return markets


def Prompt_Markets():
    markets = Market_List()
    if len(markets) == 1:
        return markets
        
    while 1:
        marketList = [m for m in markets
                      if raw_input("Include Market %s? (y/n): " 
                      % m.name).lower() == 'y']
        if len(marketList) < 1:
            print "*** Error: You must select at least one market."
        else:
            return marketList


class Store():
    def __init__(self, number, sessionName):
        self.number = number
        self.session_name = sessionName.split('.')[0]
        self.report_data = ""
        
class Market():
    def __init__(self, name):
        path = "%s\\sessions\\%s" % (Directories.config, name)
        if not os.path.exists(path):
            raise warden.globals.InvalidMarketException("No market found by " + name)
        self.name = name
        self.path = path
        self.stores = self.Store_List()
        self.report_range = ""
    
    def Store_List(self):
        if os.path.exists(self.path):
            return [Store(s, filename) for filename in os.listdir(self.path)
                      for s in re.split('\s|\.', filename)
                      if s.isdigit()] 

    def Report_Open(self, filename, should_handle=None):
        check_dates = ""
        errors = None
        dates = None
        for s in self.stores:
            try:
                with open("%s\\%s\\%s" % \
                    (Directories.storeFiles, s.number, filename)) as report:
                    data = warden.util.Remove_RTF(report.read())
                    dates = re.search(r'^.*\d{2}/\d{2}/\d{4}\s-\s\d{2}/\d{2}/\d{4}.*$',
                                      data, flags=re.MULTILINE)
                    if check_dates == "": #First iteration
                        check_dates = dates.group(0).strip()
                    if not dates.group(0).strip() == check_dates:
                        raise ReportRangeError("Report Ranges inconsistant.")
                    s.report_data = data
            except (IOError, warden.globals.ReportRangeError) as e:
                self.report_data = ""
                if not should_handle:
                    raise Exception(e)
                else:
                    print "*** Error:"
                    print "We noticed not all stores in", self.name, \
                          "have the report properly pulled or the data is", \
                          "not for the same range of dates."
                    choice = raw_input("Would you like to pull the report " + \
                                       "now? (y/n): ")
                    if choice.lower() == 'y':
                        scrt = Get_SecureCRT_Proc()
                        if scrt:
                            scrt.kill() #Close the program
                        if dates:
                            dates = dates.group(0).strip().split('-')
                            d_choice = raw_input("Use range " + dates[0] + \
                                "through " + dates[1] + "? (y/n): ")
                            if d_choice.lower() == 'y':
                                s1, s2, s3 = dates[0].strip().split('/')
                                e1, e2, e3 = dates[1].strip().split('/')
                                d_range = [s1 + s2 + s3, e1 + e2 + e3]
                                GetRangeFromTxt("range.txt", d_range)
                                Report_Pull(filename, self)
                                return self.Report_Open(filename, should_handle)
                            else:
                                d0 = raw_input("Enter Beginning Date " + \
                                                "mmddyyyyy: ")
                                d1 = raw_input("Enter Ending Date " + \
                                                "mmddyyyyy: ")
                                GetRangeFromTxt("range.txt", [d0, d1])
                                Report_Pull(filename, self)
                                return self.Report_Open(filename, should_handle)
                        else:
                            d0 = raw_input("Enter Beginning Date " + \
                                                "mmddyyyyy: ")
                            d1 = raw_input("Enter Ending Date " + \
                                            "mmddyyyyy: ")
                            GetRangeFromTxt("range.txt", [d0, d1])
                            Report_Pull(filename, self)
                            return self.Report_Open(filename, should_handle)

        self.report_range = check_dates

    
    def Update_Auto_Session(self):
        original_file = "%s\\Global.ini" % Directories.config
        temporary_write_file = "%s\\new.ini" % Directories.config
        with open(original_file, "r") as infile, \
             open(temporary_write_file, "wt") as outfile:
             for line in infile:
                if "S:\"Auto Session Name\"" in line:
                    str_stores = ""
                    for store in self.stores:
                        str_stores += "%s\\%s:" \
                                        % (self.name, store.session_name)
                    str_stores = str_stores[:-1] #Remove trailing :
                    outfile.write("S:\"Auto Session Name\"=%s\n" % str_stores)
                else:
                    outfile.write(line)
        original_file_backup = "%s\\Global.ini.bak" % Directories.backup
        if os.path.exists(original_file_backup):
            os.remove(original_file_backup)
        
        os.rename(original_file, original_file_backup)
        os.rename(temporary_write_file, original_file)

    def Update_Login_Script(self, script):
        
        market_sessions = "%s\\sessions\\%s" % (Directories.config, self.name)
        for filename in os.listdir(market_sessions):
            original_file = "%s\\%s" % (market_sessions, filename)
            temporary_write_file = "%s\\new.ini" % market_sessions 
            
            with open(original_file, "r") as infile, \
                 open(temporary_write_file, "w") as outfile:
                for line in infile:
                    if "S:\"Script Filename\"" in line:
                        outfile.write("S:\"Script Filename\"=%s\\%s %s\n"
                            % (Directories.scripts, script.file_path,
                                script.argument))
                    else:
                        outfile.write(line)
            original_file_backup = "%s\\%s.bak" \
                                    % (Directories.backup, filename)

            if os.path.exists(original_file_backup):
                os.remove(original_file_backup)

            os.rename(original_file, original_file_backup)
            os.rename(temporary_write_file, original_file)
