import conversions.arithmetic as arithmetic
import conversions.memAccess as mem
import conversions.terminator as term
import conversions.logical as logical
import re

class Instruction:

	def __init__(self,instrStr):
                raw = instrStr.split("=");

                if len(raw) == 2 and instrStr[0] not in ";":
                    self.result = raw[0].strip();
                    rawInstr = raw[1].strip();

                else:
                    self.result = "";
                    rawInstr = raw[0].strip();

		self.args = [];
                self.params = [];
		self.generateSubleq = voidAction;

		for tupple in instrTypes:
			if re.match(tupple[0].strip(),rawInstr):
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
	("mul", arithmetic.parseArgs, arithmetic.mul),
        ("tail call", term.callParseArgs, term.call),
        ("call", term.callParseArgs, term.call),
        ("sdiv", arithmetic.parseArgs, arithmetic.div)
]
