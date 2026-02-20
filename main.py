# Names:
# Mackenzie Johnson
# Christian Rodriguez
#

import re

#Token Defenitions
keywords = [r"(if)\s", r"(else)\s", r"(int)\s", r"(float)\s"]
integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
operators = ["=", "+", ">", "*"]
seperators = ["(", ")", ":", "\"", ";"]

# TinyPie function
def CutOneLineTokens(s):
	print("Test input string:", s)

	#Validate only 1 keyword
	keywordCount = 0
	for i in keywords:
		count = len(re.findall(i,s))
		keywordCount += count
		if keywordCount > 1:
			print("Invalid Syntax: Multiple Keywords")
			return

	# store tokens
	key = ""
	operatorToken = []
	seperatorToken = []
	identifierToken = []
	intToken = []
	floatToken = []
	strToken = []

	# Removes the keyword found in line
	for k in keywords:
		m = re.search(k, s) # look for a match
		if m:
			key = m.group(1)
			s = re.sub(k, "", s)

	# Error detection if no keywords are found
	if (key == ""):
		print("Invalid Syntax: No Keywords Found")
		return

	print("key:", key)

# start of main area
str1 = "int A1=5"
str2 = "float BBB2 =1034.2"
str3 = "float cresult = A1 +BBB2 * BBB2"
str4 = "if (cresult >10):"
str5 = "     print(“TinyPie   “)"

strs = [str1, str2, str3, str4, str5]

for s in strs:
	CutOneLineTokens(s)


