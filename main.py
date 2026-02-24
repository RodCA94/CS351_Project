# Names:
# Mackenzie Johnson
# Christian Rodriguez
# Andrew Muller

import re

# Token Definitions
keywords = {"if", "else", "int", "float"}

# Build regress match
frontSpace = r"^\s+"
identifiers = r"^[A-Za-z_][A-Za-z0-9_]*"
integers = r"^\d+"
floats = r"^\d+\.\d+"
stringLit = r'^"[^"\n]*"'

# single char match
operators = ["=", "+", ">", "*"]
separators = ["(", ")", ":", ";"]

# TinyPie function
def CutOneLineTokens(s):
	print("Test input string:", s)

	output = []

	while s:
		# starts by removing all white space at the front of the string
		m = re.match(frontSpace, s)
		if m:
			s = s[m.end():]
			continue

		# look for string literals
		m = re.match(stringLit, s)
		if m:
			# add the token to the end of the output
			token = m.group(0)
			output.append(f"<str,{token}>")
			# remove the token from string
			s = s[m.end():]
			continue

		# look for floats first
		m = re.match(floats, s)
		if m:
			token = m.group(0)
			output.append(f"<float,{token}>")
			s = s[m.end():]
			continue

		# then we look for integers
		m = re.match(integers, s)
		if m:
			token = m.group(0)
			output.append(f"<int,{token}>")
			s = s[m.end():]
			continue

		# look for identifiers and check if they are keywords
		m = re.match(identifiers, s)
		if m:
			token = m.group(0)
			# keyword
			if token in keywords:
				output.append(f"<key,{token}>")
			# identifier
			else:
				output.append(f"<id,{token}>")
			s = s[m.end():]
			continue

		# look for operators or seperator, will be single char
		char = s[0]
		# operator
		if char in operators:
			output.append(f"<op,{char}>")
			s = s[1:]
			continue

		# seperator
		if char in separators:
			output.append(f"<sep,{char}>")
			s = s[1:]
			continue

		# if program reaches this line it means there are invalid characters
		return "Invalid character input:", s[0]

	return(output)

# start of main area
str1 = "int A1=5"
str2 = "float BBB2 =1034.2"
str3 = "float cresult = A1 +BBB2 * BBB2"
str4 = "if (cresult >10):"
str5 = "     print(\"TinyPie   \")"

strs = [str1, str2, str3, str4, str5]

for s in strs:
	token = CutOneLineTokens(s)
	print("[" +", ".join(token) + "]")


