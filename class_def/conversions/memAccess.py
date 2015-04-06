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

        params = argStr.split(",");
        arg1 = re.findall("(?<=\s)\S+$",params[0])[0];
        arg2 = re.findall("(?<=\s)\S+$",params[1])[0];
        
        return [arg1,arg2]

def loadParseArgs(argStr):
        return re.findall("(?<=\*\s)\S+(?=,)|(?<=\*\s)\S+(?=$)",argStr)

def store(instr, assem):
	arg1 = instr.args[0];
	arg2 = instr.args[1];

	if "%" not in arg1 and arg1 not in assem.dataMem: #move literal->b
			assem.dataMem[arg1] = int(arg1);

        t0 = assem.getNextTemp();
        t1 = assem.getNextTemp();

	assem.progMem.append("\n// " + instr.raw);

	#check if second argument is a pointer
	if arg2 in assem.dataMem and assem.dataMem[arg2][0] == "&":
		p_0 = assem.getNextReserved("p_");
		p_1 = assem.getNextReserved("p_");
		p_2 = assem.getNextReserved("p_");

		#rewrite the necessary instructions
                assem.subleq(p_0,p_0,"NEXT");
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(arg2,t0,"NEXT");
                assem.subleq(t0,p_0,"NEXT");

                assem.subleq(p_1,p_1,"NEXT");
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(arg2,t1,"NEXT");
                assem.subleq(t0,p_1,"NEXT");

                assem.subleq(p_2,p_2,"NEXT");
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(arg2,t0,"NEXT");
                assem.subleq(t0,p_2,"NEXT");

                assem.subleq(p_0 + ":#1", p_1 + ":#1", "NEXT");
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(arg1,t0,"NEXT");
                assem.subleq(t0, p_2 + ":#1", "NEXT");
	
	else:
                assem.subleq(arg2,arg2,"NEXT");
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(arg1,t0,"NEXT");
                assem.subleq(t0,arg2,"NEXT");

def load(instr, assem):
	arg1 = instr.args[0];
	result = instr.result;

        t0 = assem.getNextTemp();

	assem.progMem.append("\n// " + instr.raw);
	assem.subleq(result,result,"NEXT");
        assem.subleq(t0,t0,"NEXT");
	assem.subleq(arg1,t0,"NEXT");
        assem.subleq(t0,result,"NEXT");

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

        t0 = assem.getNextTemp();

	if len(sizeArgs) > 1:
		print "error - can't handle multidimensional structs just yet...sorry";
		sys.exit(2);

	assem.progMem.append("\n// " + instr.raw);
        assem.subleq(result,result,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(b,t0,"NEXT");
        assem.subleq(t0,result,"NEXT");

        assem.dataMem[result] = "&" + a; #dummy

def sextParseArgs(argStr):
	arg1 = re.findall("(?<=i32)\s+\S+\s+(?=to)",argStr)[0];

	return [arg1]

def sext(instr, assem):
	a = instr.args[0];
	result = instr.result;

        t0 = assem.getNextTemp();

        assem.subleq(result,result,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(t0,result,"NEXT");
