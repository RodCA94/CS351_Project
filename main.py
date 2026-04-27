# Names:
# Mackenzie Johnson
# Christian Rodriguez
# Andrew Muller

import re
from asyncio.windows_events import NULL
from tkinter import *

#GUI Line
currentLineNumber = 0
initialClick = False
lines = []

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

####### PHASE 1 Commented out ################
# str1 = "int A1=5"
# str2 = "float BBB2 =1034.2"
# str3 = "float cresult = A1 +BBB2 * BBB2"
# str4 = "if (cresult >10):"
# str5 = "     print(\"TinyPie   \")"

# strs = [str1, str2, str3, str4, str5]

# for s in strs:
#	token = CutOneLineTokens(s)
#	print("[" +", ".join(token) + "]")
###############################################

# Parser Code
parseTokens = []
inToken = ("empty", "empty")
parseOutput = []


def convertTokens(tokenList):
    result = []

    for t in tokenList:
        t = t.strip()

        if t.startswith("<") and t.endswith(">"):
            t = t[1:-1]

        parts = t.split(",", 1)

        if len(parts) == 2:
            result.append((parts[0].strip(), parts[1].strip()))

    return result


def accept_token():
    global inToken, parseTokens, parseOutput

    parseOutput.append("     accept token from the list:" + inToken[1])

    if len(parseTokens) > 0:
        inToken = parseTokens.pop(0)
    else:
        inToken = ("empty", "empty")


def math_exp():
    global inToken, parseOutput

    parseOutput.append("\n----parent node math_exp, finding children nodes:")
    parseOutput.append("child node (internal): multi")
    multi()

    if inToken[1] == "+":
        parseOutput.append("child node (token):+")
        accept_token()

        parseOutput.append("child node (internal): math_exp")
        math_exp()


def multi():
    global inToken, parseOutput

    parseOutput.append("\n----parent node multi, finding children nodes:")

    if inToken[0] == "int":
        parseOutput.append("child node (internal): int")
        parseOutput.append("   int has child node (token):" + inToken[1])
        accept_token()

    elif inToken[0] == "float":
        parseOutput.append("child node (internal): float")
        parseOutput.append("   float has child node (token):" + inToken[1])
        accept_token()

    else:
        parseOutput.append("ERROR: multi expects int or float")
        return

    if inToken[1] == "*":
        parseOutput.append("child node (token):*")
        accept_token()

        parseOutput.append("child node (internal): multi")
        multi()


def exp():
    global inToken, parseOutput

    parseOutput.append("\n----parent node exp, finding children nodes:")

    if inToken[1] == "float":
        parseOutput.append("child node (token):float")
        accept_token()
    else:
        parseOutput.append("ERROR: math line should start with keyword float")
        return

    if inToken[0] == "id":
        parseOutput.append("child node (internal): identifier")
        parseOutput.append("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        parseOutput.append("ERROR: expected identifier after float")
        return

    if inToken[1] == "=":
        parseOutput.append("child node (token):=")
        accept_token()
    else:
        parseOutput.append("ERROR: expected = after identifier")
        return

    parseOutput.append("child node (internal): math_exp")
    math_exp()

    if inToken[1] == ";":
        parseOutput.append("child node (token):;")
        parseOutput.append("\nparse tree building success!")
    else:
        parseOutput.append("ERROR: expected ; at end of math line")


def if_exp():
    global inToken, parseOutput

    parseOutput.append("\n----parent node if_exp, finding children nodes:")

    if inToken[1] == "if":
        parseOutput.append("child node (token):if")
        accept_token()
    else:
        parseOutput.append("ERROR: expected if")
        return

    if inToken[1] == "(":
        parseOutput.append("child node (token):(")
        accept_token()
    else:
        parseOutput.append("ERROR: expected (")
        return

    parseOutput.append("child node (internal): comparison_exp")
    comparison_exp()

    if inToken[1] == ")":
        parseOutput.append("child node (token):)")
        accept_token()
    else:
        parseOutput.append("ERROR: expected )")
        return

    if inToken[1] == ":":
        parseOutput.append("child node (token)::")
        accept_token()
        parseOutput.append("\nparse tree building success!")
    else:
        parseOutput.append("ERROR: expected :")


def comparison_exp():
    global inToken, parseOutput

    parseOutput.append("\n----parent node comparison_exp, finding children nodes:")

    if inToken[0] == "id":
        parseOutput.append("child node (internal): identifier")
        parseOutput.append("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        parseOutput.append("ERROR: expected identifier")
        return

    if inToken[1] == ">":
        parseOutput.append("child node (token):>")
        accept_token()
    else:
        parseOutput.append("ERROR: expected >")
        return

    if inToken[0] == "id":
        parseOutput.append("child node (internal): identifier")
        parseOutput.append("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        parseOutput.append("ERROR: expected identifier")


def print_exp():
    global inToken, parseOutput

    parseOutput.append("\n----parent node print_exp, finding children nodes:")

    if inToken[1] == "print":
        parseOutput.append("child node (token):print")
        accept_token()
    else:
        parseOutput.append("ERROR: expected print")
        return

    if inToken[1] == "(":
        parseOutput.append("child node (token):(")
        accept_token()
    else:
        parseOutput.append("ERROR: expected (")
        return

    if inToken[0] == "str":
        parseOutput.append("child node (internal): string")
        parseOutput.append("   string has child node (token):" + inToken[1])
        accept_token()
    else:
        parseOutput.append("ERROR: expected string")
        return

    if inToken[1] == ")":
        parseOutput.append("child node (token):)")
        accept_token()
    else:
        parseOutput.append("ERROR: expected )")
        return

    if inToken[1] == ";":
        parseOutput.append("child node (token):;")
        parseOutput.append("\nparse tree building success!")
    else:
        parseOutput.append("ERROR: expected ;")


def parser(tokenList, lineNumber):
    global parseTokens, inToken, parseOutput

    parseOutput = []
    parseTokens = convertTokens(tokenList)

    if len(parseTokens) == 0:
        return ""

    inToken = parseTokens.pop(0)

    parseOutput.append("#### Parse tree for line " + str(lineNumber) + " ####")

    if lineNumber == 1 or lineNumber == 2:
        exp()
    elif lineNumber == 3:
        if_exp()
    elif lineNumber == 4:
        print_exp()
    else:
        parseOutput.append("ERROR: This assignment only expects 4 lines.")

    return "\n".join(parseOutput)

# GUI def
def processLine():
	global currentLineNumber, initialClick, lines
	output = []

	if not initialClick:
		text = sourceBox.get("1.0", END)
		lines = text.splitlines()
		initialClick = True
	# indents new processing line
	else:
		tokenBox.config(state="normal")
		tokenBox.insert(END, "\n")
		tokenBox.config(state="disabled")

	if currentLineNumber < len(lines):
		line = lines[currentLineNumber]
		# writes to outputBox then makes read only again
		output = CutOneLineTokens(line)
		tokenBox.config(state="normal")
		tokenBox.insert(END, "\n".join(output))
		tokenBox.insert(END, "\n")
		tokenBox.config(state="disabled")

		parseResult = parser(output, currentLineNumber + 1)
		parseBox.config(state="normal")
		parseBox.insert(END, parseResult + "\n\n")
		parseBox.config(state="disabled")

		# call to highlight line
		highlightLine()

		# update processing line
		currentLine.config(text=str(currentLineNumber + 1))
		currentLineNumber += 1


#update line numbers function
def updateLineNumbers(event=None):
	# Count lines in sourceBox
	text = sourceBox.get("1.0", END)
	lines = text.count("\n")  # number of lines

	# Build the numbering text
	nums = "\n".join(str(i) for i in range(1, lines + 1))

	# Update the lineNumbers widget
	lineNumbers.config(state="normal")
	lineNumbers.delete("1.0", END)
	lineNumbers.insert("1.0", nums)
	lineNumbers.config(state="disabled")


# function to highlight each line
def highlightLine():
	global currentLineNumber

	sourceBox.tag_remove("highlight", "1.0", END)

	line_index = f"{currentLineNumber + 1}.0"
	line_end = f"{currentLineNumber + 1}.end"

	sourceBox.tag_add("highlight", line_index, line_end)
	sourceBox.tag_config("highlight", background="yellow")


def exitWindow():
	root.destroy()

# start of GUI
root = Tk()
root.geometry("1200x500")
root.title("Lexical Analyzer for TinyPie")

# labels
inputLabel = Label(root, text="Source Code Input:")
inputLabel.place(x=50, y=50)
tokenLabel = Label(root, text="Tokens:")
tokenLabel.place(x=420, y=50)
parseLabel = Label(root, text="Parse Tree:")
parseLabel.place(x=760, y=50)
lineLabel = Label(root, text="Current Processing Line:")
lineLabel.place(x=50, y=380)
currentLine = Label(root, text="0", relief="solid", width=5)
currentLine.place(x=195, y=380)

# buttons
quitButton = Button(root, text="Quit", command=exitWindow, bg = "red")
quitButton.place(x=950, y=420, width=80)
nextLineButton = Button(root, text="Next Line",command=processLine, bg="green")
nextLineButton.place(x=155, y=420, width=80)

# text box
sourceBox = Text(root, height=18, width=40, padx=10)
sourceBox.place(x=60, y=80)
sourceBox.bind("<KeyRelease>", updateLineNumbers)

#line numbers
lineNumbers = Text(root, width=2, height=18, state="disabled")
lineNumbers.place(x=50, y=80)

# Tokens box
tokenBox = Text(root, height=18, width=40,state="disabled")
tokenBox.place(x=415, y=80)

# Parse Tree box
parseBox = Text(root, height=18, width=54,state="disabled")
parseBox.place(x=750, y=80)

# run GUI
root.mainloop()