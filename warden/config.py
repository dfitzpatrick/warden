import os

class Directories():
    storeFiles = os.environ['XTALK_STOREFILES'] if os.environ.get('XTALK_STOREFILES') else "s:\\"
    secureCRT = os.environ['XTALK_INSTALLPATH'] if os.environ.get('XTALK_INSTALLPATH') else "c:\\program files\\vandyke software\\securecrt"
    config = os.environ['XTALK_CONFIGPATH'] if os.environ.get('XTALK_CONFIGPATH') else "c:\\vandyke"
    backup = os.environ['XTALK_BACKUPPATH'] if os.environ.get('XTALK_BACKUPPATH') else "c:\\vandyke\\bak"
    scripts = os.environ['XTALK_SCRIPTSPATH'] if os.environ.get('XTALK_SCRIPTSPATH') else "c:\vandyke\\scripts"