# Names:
# Mackenzie Johnson
# Christian Rodriguez
#

import re

#Token Defenitions
keywords = {"if", "else", "int", "float)"}

#Build regress match
frontSpace = re.compile(r"^\s+")
identifiers = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
integers = re.compile(r"^\d+")
floats = re.compile(r"^\d+\.\d+")
stringLit = re.compile(r'^"[^"\n]*"')

operators = ["=", "+", ">", "*"]
seperators = ["(", ")", ":", ";"]

# TinyPie function
def CutOneLineTokens(s):
	print("Test input string:", s)

	token = []

	while s:
		# starts by removing all white space at the front of the string
		m = frontSpace.match(s)
		if m:
			s = s[m.end():]
			continue
		print(s)



# start of main area
str1 = "int A1=5"
str2 = "float BBB2 =1034.2"
str3 = "float cresult = A1 +BBB2 * BBB2"
str4 = "if (cresult >10):"
str5 = "     print(“TinyPie   “)"

strs = [str1, str2, str3, str4, str5]

for s in strs:
	CutOneLineTokens(s)


