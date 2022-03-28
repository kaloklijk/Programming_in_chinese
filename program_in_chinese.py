'''
This program is a programming language using chinese characters and will simply be translated
into python for running the code. Designed by Li Ka Lok, Jack
'''

## Import the required Dependencies
from queue import Empty
import sys
import os
from textwrap import dedent
import numpy as np

# a variables for handling indentation for looping in python
loops = 0
def correct(s):
    '''
    for translating the chinese programming language into python
    '''
    global loops
    # extra variables for indentation for loopings
    count = 0
    # for ending a loop
    if s == "":
        if loops > 0:
            loops = loops-1
        s = "\n"
        return s
    # for fixing s for the orrection
    if len(s) < 2:
        s = s+"  "
    # intially dedent all whitespaces in s
    s = dedent(s)
    # print function with varialbes in {}, format: 說a={a}, print(f"a={a}")
    if s[0] == "說":
        s = "print(f\""+s[1:]+"\")"
    # if function, : is automatically generated = means ==, format: 如果 a => if a:
    if s[0]+s[1] == "如果":
        loops = loops+1
        count = 1
        s = "if "+s[2:]
        if s[-1] != ":":
            s = s+":"
        for i, char in enumerate(s):
            if char=="=":
                if s[i-1] != "!" and s[i-1] != ">" and s[i-1] != "<" and s[i-1] != "=":
                    s = s[:i]+"="+s[i:]
    # for loops, one can choose a specific variable, format: 從a到b(選i) => i from a to b
    if s[0] == "從":
        loops = loops+1
        count = 1
        variables = "i"
        if s[-1] == ":":
            s = s[:-1]
        s.replace(" ", "")
        for i, char in enumerate(s):
            if char == "選":
                variables = s[i+1:]
                s = s[:i]
        for i, char in enumerate(s):
            if char == "到":
                a = int(s[1:i])
                b = int(s[i+1:])
        s = f"for {variables} in np.arange({a}, {b}):"
    # while loops, format: 每當 a => while a:    ,  無限loop => while True:
    if s[0]+s[1] == "每當":
        loops = loops+1
        count = 1
        s = "while "+s[2:]
        if s[-1] != ":":
            s = s+":"
        for i, char in enumerate(s):
            if char=="=":
                if s[i-1] != "!" and s[i-1] != ">" and s[i-1] != "<" and s[i-1] != "=":
                    s = s[:i]+"="+s[i:]
    if s[:6] == "無限loop":
        loops = loops+1
        count = 1
        s = "while True:"
    # break, continue
    if s[0]+s[1] == "中斷":
        s = "break"
    if s[0]+s[1] == "繼續":
        s = "continue"
    # class
    if s[0]+s[1] == "範疇":
        loops = loops + 1
        count = 1
        s = "class " + s[2:]
        if s[-1] != ":":
            s = s+":"
    # def
    if s[0]+s[1] == "定義":
        loops = loops + 1
        count = 1
        s = "def " + s[2:]
        if s[-1] != ":":
            s = s+":"
    # bracket
    if s[-1] == "{":
        loops = loops + 1
        count = 1
    if s[0] == "}":
        if loops > 0:
            loops = loops - 1
    ## automatically indentation within loopings, can end the loop using 完
    for i in np.arange(count, loops):
        s = "    "+s
    ## automatically go to the next line
    s = s+"\n"
    ## return input s
    return s

def translation(s):
    '''
    this function is for translating the coding string from english into chinese
    '''
    # if
    s.replace("if", "如果")
    # def
    s.replace("def", "定義")
    # break
    s.replace("break", "中斷")
    # continue
    s.replace("continue", "繼續")
    # while
    s.replace("while ", "每當")
    # in
    s.replace(" in ", "從")
    # class
    s.replace("class ", "範疇")
    # True/False
    s.replace("True", "對")
    s.replace("False", "錯")
    # import
    s.replace("import", "匯入")
    ## 
    for i, string in enumerate(s):
        l = len(s)

        # for
        if i+4<l:
            if s[i]+s[i+1]+s[i+2] == "for":
                s = s[:i]+"選"+s[i+3:]
        
            if s[i:i+13] == "in np.arange(" or s[i:i+9] == "in range(":
                s = s[:i]+"從"+s[i+13:]
                for j, stri in enumerate(s[i:]):
                    if s[j] == ")":
                        s = s[:j]+s[j+1:]
                    if s[j] == ",":
                        s = s[:j]+"到"+s[j+1:]
                    if s[j] == ")":
                        s = s[:j]+s[j+1:]
        # print
        if "print(" in s:
            s.replace("print(\"", "說")
            s.replace("print(f\"", "說")
            s.replace("\")", "")
    return s
        
filename = input("please input the file name\n")
if filename[-3:] != ".py":
    filename = filename+".py"
with open(filename, "w+") as f:
    f.write("import sys\n")
    f.write("import matplotlib as plt\n")
    f.write("import numpy as np\n")
    f.write("import scipy as sp\n")
    while True:
        s = input(">> ")
        if s == "開始":
            f.seek(0)
            exec(open(filename).read())
            continue
        if s == "翻譯":
            f.seek(0)
            while True:
                # get line by line
                line = f.readline()
                if not line:
                    break
                line = translation(str(line))
                print(line)
            continue
        s = correct(s)
        print(s)
        f.write(s)

