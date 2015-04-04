import re

class Argument:

    def __init__(self, argStr):
        if argStr != "()" and argStr != '':
            raw = argStr.split();
            print argStr
            self.name = raw[-1]; #always the last string
            self.argType = raw[0];
            self.attrs = raw[1:-1]; #middle stuff is the attributes
        else:
            self.argType = "void";
            self.name = "";
            self.attrs = [];
