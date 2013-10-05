version = "0.1 BETA"

def Enum(**enums):
	print "Deprecated Enum!"
	return enum(**enums)
def enum(**enums):
    return type('Enum', (), enums)

class ReportRangeError(Exception):
    pass
class MissingReportError(Exception):
    pass
class MissingScriptError(Exception):
    pass
class RequiresDateRangeArguments(Exception):
    pass
class InvalidMarketException(Exception):
	pass
class InvalidDateFormat(Exception):
	pass
class InvalidConnectionError(Exception):
	pass