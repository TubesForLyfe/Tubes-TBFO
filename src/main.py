#Program Utama Compiler#
from converter import CFGfromTXT, CFGtoCNF, displayGrammar, turntoCNF
from CYK import CYK
import sys
import re

mkey = {"if" : "a", "elif" : "b", "else" : "c", "for" : "d", "in" : "e", "while" : "f", "continue" : "g", "pass" : "h", "break" : "i", "class" : "j", "def" : "k", "return" : "l", "as" : "m", "import" : "n", "from" : "o", "raise" : "p", "and" : "q", "or" : "r", "not" : "s", "is" : "t", "True" : "u", "False" : "v", "None" : "w", "with" : "A"}

def processInput(inp):
    global key

    match = []
    newInp = ""

    while inp:
        x = re.search("[A-Za-z_][A-Za-z0-9_]*",inp)
        if x != None:
            newInp += inp[:x.span()[0]]
            if x.group() not in mkey:
                newInp += "x"
            else:
                newInp += mkey[x.group()]
            inp = inp[x.span()[1]:]
        else:
            newInp += inp
            inp = ""
    
    newInp = re.sub("[0-9]+[A-Za-z_]+","R",newInp)
    newInp = re.sub("[0-9]+","y",newInp)
    newInp = re.sub("#.*","",newInp)
    mltstr = re.findall(r'([\'\"])\1\1(.*?)\1{3}',newInp,re.DOTALL)
    
    for i in range(len(mltstr)):
        multi = mltstr[i][0]*3 + mltstr[i][1] + mltstr[i][0]*3
        newInp = newInp.replace(multi, "z\n" * mltstr[i][1].count("\n"))

    str = re.findall(r'([\'\"])(.*?)\1{1}', newInp, re.DOTALL)
    for i in range(len(str)):
        one = str[i][0] + str[i][1] + str[i][0]
        newInp = newInp.replace(one, "z")

    newInp = newInp.replace(" ","")
    newInp = re.sub("[xyz]{1}:[xyz]{1},","",newInp)
    return (newInp + '\n')

def fileReader(path):
    with open(path, "r") as f:
        content = f.read()
    return content

def nameError(inp):
    newInp = ""
    while inp:
        x = re.search("[0-9]+[A-Za-z_]+", inp)
        if x != None:
            newInp += inp[:x.span()[0]] + x.group()
            inp  = inp[x.span()[1]:]
        else:
            newInp += inp
            inp = ""
    return (newInp)

def startCompiler():
    print("================= SELAMAT DATANG DI PYTHON COMPILER===================================")

if __name__ == "__main__":

    startCompiler()

    #input grammar
    CFG = CFGfromTXT("grammar.txt")
    CNF = CFGtoCNF(CFG)


    #input file
    if (len(sys.argv) < 2):
        filePathInput = "inputAcc.py"
    else:
        filePathInput = sys.argv[1]
    
    try:
        inp = fileReader(filePathInput)
    except Exception as e:
        print("Error: "+ str(e))
        print("Terminating program...\n")
        exit(0)
    
    inpHighlighted = nameError(inp)
    source = inp

    inp = processInput(inp)
    

    print("Compiling " + str(filePathInput) + "...\n")
    print("Waiting for your verdict...\n")

    print("=================== Source Code ================")
    for i, line in enumerate(inpHighlighted.split("\n")):
        idx = f" {i + 1} | " if len(str(i+1)) == 1 else\
              f" {i + 1} | " if len(str(i+1)) == 2 else\
              f"{i+1} | "
        print(idx + line)

    print("\n============================== Verdict =======================\n")
    if (len(inp) == 0):
        print("Accepted")
        print("\n============================================================")
        exit(0)
    
    CYK(inp, CNF, source)
    print("\n================================================================")


