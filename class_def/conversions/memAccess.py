from helpers import next_subleq as subleq
from helpers import clear
import re
import sys

def allocateParseArgs(argStr):
	args = re.findall("(?<=\[)\s*\d+",argStr);
	ints = [];
	for arg in args:
		if arg != "":
			ints.append(int(arg))

	return ints

def allocate(instr,assem):
	#only need to allocate memory if an array is in the argument
	if len(instr.args) > 0:
		#find the size of the memory to allocate
		size = 1;
		for arg in instr.args:
			size *= arg;

		if size > 0:		
			for i in xrange(size):
				assem.dataMem[instr.result + str(i)] = 0;

			assem.dataMem[instr.result] = "&" + instr.result + "0";

		#arrays of size 0 are allowed in c (trying to mimic gcc behaviour) 
		else:
			assem.dataMem[instr.result] = "&" + instr.result;

def storeParseArgs(argStr):

	arg1Matches = re.findall("(?<=i32)\s+\S+(?=,)|(?<=i64)\s+\S+(?=,)",argStr);
	if len(arg1Matches) != 1:
		print "parse error on " + argStr
		sys.exit(2)

	arg1 = arg1Matches[0];
	if arg1 == "":
		print "parse error on " + argStr
		sys.exit(2);

	arg2Matches = re.findall("(?<=i32\*)\s+[^\s,]+|(?<=i64\*)\s+\[^\s,]+", argStr);
	if len(arg2Matches) != 1:
		print "parse error on " + argStr
		sys.exit(2)

	arg2 = arg2Matches[0];
	if arg2 == "":
		print "parse error on " + argStr
		sys.exit(2);

	return [arg1,arg2];

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
		assem.progMem.append(subleq(zero,zero)); #noop, must be at least 2 instructions between modifying and instruction and executing it

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
	args = re.findall("(?<=\[)\s*\d+",argStr);
	memArgs = [];
	for arg in args:
		if arg != "":
			memArgs.append(int(arg))

	arg1 = re.findall("(?<=\*\s)\S+(?=,)", argStr)[0];
	arg2 = re.findall("(?<=i64\s)\S+", argStr)[0];

	memArgs.append(arg1);
	memArgs.append(arg2);
	return memArgs;

def ptrMath(instr, assem):
	a = instr.args[-2];
	b = instr.args[-1];
	sizeArgs = instr.args[0:len(instr.args)-2]; #data for the size of the structure accessing
	result = instr.result;

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	if len(sizeArgs) > 1:
		print "error - can't handle multidimensional structs just yet...sorry";
		sys.exit(2);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(subleq(a,result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(subleq(t0,result));
	assem.progMem.append(subleq(b,result));

	assem.dataMem[result] = "&" + a; #dummy

def sextParseArgs(argStr):
	arg1 = re.findall("(?<=i32)\s+\S+\s+(?=to)",argStr)[0];

	return [arg1]

def sext(instr, assem):
	a = instr.args[0];
	result = instr.result;

	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq(a,result));