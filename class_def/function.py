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

def parseName(firstLine):
		name = re.findall("(?<=@).*(?=\()", firstLine)[0];
		return name;

def parseArgs(firstLine):
	argsStr = re.findall("(?=\().*(?<=\))", firstLine)[0];
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