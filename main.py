# Names:
# Mackenzie Johnson
# Christian Rodriguez
# Andrew Muller

import re
from tkinter import *

#GUI Line
currentLineNumber = 0

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


# GUI def
def processLine():
	global currentLineNumber

	text = sourceBox.get("1.0", END)
	lines = text.splitlines()

	if currentLineNumber < len(lines):
		line = lines[currentLineNumber]
		# writes to outputBox then makes read only again
		outputBox.config(state="normal")
		outputBox.insert(END, line + "\n")
		outputBox.config(state="disabled")

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
root.geometry("1000x500")
root.title("Lexical Analyzer for TinyPie")

# labels
inputLabel = Label(root, text="Source Code Input:")
inputLabel.place(x=50, y=50)
resultLabel = Label(root, text="Lexical Analyzed Result:")
resultLabel.place(x=550, y=50)
lineLabel = Label(root, text="Current Processing Line:")
lineLabel.place(x=50, y=380)
currentLine = Label(root, text="0", relief="solid", width=5)
currentLine.place(x=195, y=380)

# buttons
quitButton = Button(root, text="Quit", command=exitWindow, bg = "red")
quitButton.place(x=700, y=420, width=80)
nextLineButton = Button(root, text="Next Line",command=processLine, bg="green")
nextLineButton.place(x=155, y=420, width=80)

# text box
sourceBox = Text(root, height=18, width=40, padx=10)
sourceBox.place(x=60, y=80)
sourceBox.bind("<KeyRelease>", updateLineNumbers)

#line numbers
lineNumbers = Text(root, width=2, height=18, state="disabled")
lineNumbers.place(x=50, y=80)

# outputBox is read only
outputBox = Text(root, height=18, width=40,state="disabled")
outputBox.place(x=550, y=80)

# run GUI
root.mainloop()