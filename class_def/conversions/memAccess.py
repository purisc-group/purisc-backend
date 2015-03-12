from helpers import next_subleq as subleq
from helpers import clear
import re

def allocateParseArgs(argStr):
	args = re.findall("(?<=\[)\s*\d+",argStr);
	ints = [];
	for arg in args:
		if arg != "":
			ints.append(int(arg))

	return ints

def allocate(instr,assem):
	#only need to allocate memory if an array is in the argument
	if len(instr.args) == 1 and instr.args[0] > 0:
		#allocate a pointer variable to hold the address of the array
		#and allocaate the number of locations equal to the length of the array		
		for i in xrange(instr.args[0]):
			assem.dataMem[instr.result + str(i)] = 0;

		assem.dataMem[instr.result] = "&" + instr.result + "0";

def storeParseArgs(argStr):
	keyword = "i32";

	index1 = argStr.find(keyword) + len(keyword);
	index1End = argStr.find(',');

	index2 = argStr.find("i32*") + 4;
	index2End = argStr.find(',', index2);

	if index2End == -1:
		index2End = len(argStr)

	return argStr[index1:index1End].strip(), argStr[index2:index2End].strip();

def loadParseArgs(argStr):
	keyword = "i32*";

	index = argStr.find(keyword) + len(keyword);

	indexEnd = argStr.find(",");
	if indexEnd == -1:
		indexEnd = len(argStr);
	
	return [argStr[index:indexEnd].strip()];

def store(instr, assem):
	arg1 = instr.args[0];
	arg2 = instr.args[1];

	if "%" not in arg1 and arg1 not in assem.dataMem: #move literal->b
			assem.dataMem[arg1] = int(arg1);

	assem.progMem.append("\n// " + instr.raw);

	#check if second argument is a pointer
	if arg2 in assem.dataMem and assem.dataMem[arg2][0] == "&":
		p_0 = assem.getNextReserved("p_");
		p_1 = assem.getNextReserved("p_");
		p_2 = assem.getNextReserved("p_");

		#rewrite the necessary instructions
		assem.progMem.append(clear(p_0));
		assem.progMem.append(subleq(arg2,p_0));
		assem.progMem.append(clear(p_1));
		assem.progMem.append(subleq(arg2,p_1));
		assem.progMem.append(clear(p_2));
		assem.progMem.append(subleq(arg2,p_2));

		assem.progMem.append(subleq(p_0 + ":#1", p_1 + ":#1"));
		assem.progMem.append(subleq(arg1, p_2 + ":#1"));
	
	else:
		assem.progMem.append(clear(arg2));
		assem.progMem.append(subleq(arg1,arg2));

def load(instr, assem):
	arg1 = instr.args[0];
	result = instr.result;

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(subleq(arg1,result));

def ptrMathParseArgs(argStr):
	arg1 = re.findall("(?<=\*\s)\S+(?=,)", argStr)[0];
	arg2 = re.findall("(?<=i64\s)\S+", argStr)[0];

	return [arg1, arg2];

def ptrMath(instr, assem):
	a = instr.args[0];
	b = instr.args[1];
	result = instr.result;

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(subleq(a,result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(subleq(t0,result));
	assem.progMem.append(subleq(b,result));

	assem.dataMem[result] = "&" + a; #dummy