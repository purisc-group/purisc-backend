from helpers import next_subleq as subleq
from helpers import clear
import re

def add(instr, assem):
	arg1 = instr.args[0];
	arg2 = instr.args[1];
	result = instr.result;

	t0 = "t" + str(assem.stackCount);
	assem.stackCount +=1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount +=1;

	#check for literals
	if re.match("\d+",arg1):
		print arg1
		if arg1 not in assem.dataMem:
			assem.dataMem[arg1] = arg1;

	if re.match("\d+",arg2):
		print arg2
		if arg2 not in assem.dataMem:
			assem.dataMem[arg2] = arg2;

	assem.progMem.append(subleq(result,result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(subleq(arg1,result));
	assem.progMem.append(clear(t1));
	assem.progMem.append(subleq(t1,result));
	assem.progMem.append(subleq(arg2,result));

def sub(instr, assem):
	arg1 = instr.args[0];
	arg2 = instr.args[1];
	result = instr.result;

	assem.progMem.append(clear(result))
	assem.progMem.append(subleq(arg2, result));
	assem.progMem.append(subleq(arg1, result));

def parseArgs(argStr):
	key = "i32";
	index = argStr.find(key);
	argStr = argStr[index+len(key):];
	[arg1,arg2] = argStr.split(",");

	return arg1.strip(),arg2.strip();