import os
scripts = []
categories = {}

def Load_Configuration(seq_script):
	scripts = seq_script
	categories = {s.category for s in scripts}

class Script():
    def __init__(self, file_path, categories="", name="", argument="",
        requires_date_range=False, retrieve_file_name=""):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.categories = categories
        self.name = name
        self.requires_date_range = requires_date_range
        self.range = []
        self.argument = argument #Not yet supported by SecureCRT
        self.retrieve_file_name = retrieve_file_name
