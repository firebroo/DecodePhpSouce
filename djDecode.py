#!/bin/python

import re

class SDDecode():

    def __init__(self):
        self.content = ""
        self.replaceVarList1 = []
        self.replaceVarList2 = []
        self.replaceFunList1 = []
        self.replaceFunList2 = []

    def readFile(self):
        fil = open("space.inc.php")
        content = fil.read()
        fil.close()
        self.content = content

    def decode(self):
        self.readFile()
        self.replace()

    def getContent(self):
        return self.content

    def matchVariable(self):
        m = re.findall("\$[a-zA-Z_\x7f-\xff][0-9a-zA-Z_\x7f-\xff]*", self.content)
        lis = list(set(m))
        for i in lis:
            if i[-1] == "\xa0":
                self.replaceVarList1.append(i)
            else:
                self.replaceVarList2.append(i)

    def matchFunction(self):
        m = re.findall("function\s*([a-zA-Z_\x7f-\xff][0-9a-zA-Z_\x7f-\xff]*)", self.content)
        lis = list(set(m))
        for i in lis:
            if i[-1] == "\xa0":
                self.replaceFunList1.append(i)
            else:
                self.replaceFunList2.append(i)

    def replaceFunction(self):
        dic = {}
        j = "a"
        for i in self.replaceFunList1:
            self.content = re.sub("\\" + i, "func"+str(j), self.content)
            dic[i] = "func"+j
            j = (chr(ord(j) + 1))

        for i in self.replaceFunList2:
            if dic.has_key(i+"\xa0"):
                self.content = re.sub("\\" + i, dic[i+"\xa0"], self.content)
            else:
                self.content = re.sub("\\" + i, "$"+str(j), self.content)
                j = (chr(ord(j) + 1))
                dic[i] = "$"+j


    def replaceVariable(self):
        dic = {}
        j = "a"
        for i in self.replaceVarList1:
            self.content = re.sub("\\" + i, "$"+str(j), self.content)
            dic[i] = "$"+j
            j = (chr(ord(j) + 1))

        for i in self.replaceVarList2:
            if dic.has_key(i+"\xa0"):
                self.content = re.sub("\\" + i, dic[i+"\xa0"], self.content)
            else:
                self.content = re.sub("\\" + i, "$"+str(j), self.content)
                j = (chr(ord(j) + 1))
                dic[i] = "$"+j

    def replace(self):
        self.matchVariable()
        self.replaceVariable()
        self.matchFunction()
        self.replaceFunction()




if __name__ == "__main__":
    sdDecode = SDDecode()
    sdDecode.decode()
    print sdDecode.getContent()
    
