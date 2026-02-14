# Names:
# Mackenzie Johnson
# Christian Rodriguez
#

#import re # regex import

# token definition
#put NamedTuple inside token
class Token():
	type: str
	value: str

# TinyPie function
def TinyPie(string1):
	keywords: {"if"}	#type defintions here
	integers: {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
	operator: {"*"}
	seperator: {")"}

# start of main area
str1 = "int A1 = 5"
str2 = "float BBB2 =1034.2"
str3 = "float cresult = A1 +BBB2 * BBB2"
str4 = "if (cresult >10):"
str5 = "     print(“TinyPie   “)"
