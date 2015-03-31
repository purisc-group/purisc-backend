import re
from argument import Argument
from instruction import Instruction

class Function:

    def __init__(self, funcStr):
        endFirstLine = funcStr.index("\n");
        #funcStr[0:endFirstLine]
        self.name = parseName(funcStr[0:endFirstLine]);
        self.args = parseArgs(funcStr[:endFirstLine]);
        self.instructions = parseInstr(funcStr[endFirstLine+1:]);

    def allocateParamMemory(self,assem):
        for argument in self.args:
            globalScope = False;
            for attr in argument.attrs:
                if re.match("addrspace\(\d+\)\*",attr):
                    globalScope = True;
                    break;
            
            if globalScope:
                assem.dataMem[argument.name] = "@_" + argument.name[1:]; #remove the % or @ identifier llvm adds
            else:
                assem.dataMem[argument.name] = "%_" + argument.name[1:]; #remove the % or @ identifier llvm adds

def parseName(firstLine):
		name = re.findall("(?<=@).*(?=\()", firstLine)[0];
		return name;

def parseArgs(firstLine):
	argsStr = re.findall("(?<=\().*(?=\))", firstLine)[0];
	args = argsStr.split(",");
	arguments = [];

	for arg in args:
		arguments.append(Argument(arg))

	return arguments

def parseInstr(funcStr):
	instrs = [];
	
	for line in funcStr.split("\n"):
		instrs.append(Instruction(line));

	return instrs;

