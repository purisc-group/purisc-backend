import conversions.arithmetic as arithmetic
import conversions.memAccess as mem
import conversions.terminator as term
import conversions.logical as logical

class Instruction:

	def __init__(self,instrStr):
		#print instrStr
		self.result = parseResult(instrStr);
		self.args = "";
		self.generateSubleq = voidAction;

		for tupple in instrTypes:
			if tupple[0] in instrStr:
				index = instrStr.find(tupple[0]) + len(tupple[0]);
				self.args = tupple[1](instrStr[index:]);
				self.generateSubleq = tupple[2];
				self.raw = instrStr;
				break;


def parseResult(instrStr):
	equalsIndex = instrStr.find("=");
	if equalsIndex != -1:
		return instrStr[:equalsIndex].strip();
	else:
		return "";

def voidAction(instr,assem):
	return;

def voidParser(args):
	return "";

instrTypes = [
	("alloca", mem.allocateParseArgs, mem.allocate),
	("add", arithmetic.parseArgs, arithmetic.add),
	("sub", arithmetic.parseArgs, arithmetic.sub),
	("store", mem.storeParseArgs, mem.store),
	("load", mem.loadParseArgs, mem.load),
	("bitcase", voidParser, voidAction),
	("sext", mem.sextParseArgs, mem.sext),
	("br", term.branchParseArgs, term.branch),
	("icmp", logical.icmpParseArgs, logical.icmp),
	("; <label>:", term.labelParseArgs, term.label),
	("ret", term.returnParseArgs, term.returnF),
	("getelementptr", mem.ptrMathParseArgs, mem.ptrMath),
	("mul", arithmetic.parseArgs, arithmetic.mul)
]