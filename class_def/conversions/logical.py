import re
from helpers import subleq
from helpers import next_subleq
from helpers import clear

def icmpParseArgs(argStr):
	args = [];

	args.append(re.findall("\s*\w*(?=\s)",argStr)[0].strip()); #comparison type
	args.append(re.findall("(?<=i32\s)[^,]*(?=,)",argStr)[0].strip()); #first operand
	args.append(re.findall("(?<=,\s)[^,]*",argStr)[0].strip()); #second operand

	return args;

def icmp(instr, assem):
	operations[instr.args[0]](instr,assem);

def equal(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	notPos = assem.getNextReserved("notPos");
	done = assem.getNextReserved("done");
	eq = assem.getNextReserved("eq");

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq(a,result));
	assem.progMem.append(subleq(b,result,notPos));
	assem.progMem.append(subleq(result,result,done));
	assem.progMem.append(subleq(notPos + ": " + t0,t0,"NEXT"));
	assem.progMem.append(subleq(t0,result,eq));
	assem.progMem.append(subleq(result,result,done));
	assem.progMem.append(subleq(eq + ": one",result,"NEXT"));
	assem.progMem.append(subleq(done + ": " + t0,t0,"NEXT"));

	assem.dataMem["one"] = 1;

def notEqual(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq(a,result));
	assem.progMem.append(next_subleq(b,result));

def sGreater(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	less = assem.getNextReserved("less");
	done = assem.getNextReserved("done");


	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(a,t0));
	assem.progMem.append(next_subleq(t0,result));
	assem.progMem.append(subleq(b,result,less));
	assem.progMem.append(subleq(result,result,done));
	assem.progMem.append(next_subleq(less + ": " + result, result));
	assem.progMem.append(next_subleq("one",result));
	assem.progMem.append(next_subleq(done + ": " + t0,t0));

	if "one" not in assem.dataMem:
		assem.dataMem["one"] = 1;

def sGreaterEq(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	negOne = assem.getNextReserved("negOne");
	less = assem.getNextReserved("less");
	done = assem.getNextReserved("done");

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq("negOne",result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(a,t0));
	assem.progMem.append(next_subleq(t0,result));
	assem.progMem.append(subleq(b,result,less));
	assem.progMem.append(subleq(t1,t1,));
	assem.progMem.append(next_subleq(less + ": " + result,result));
	assem.progMem.append(next_subleq(done + ": " + t0,t0));

	if "negOne" not in assem.dataMem:
		assem.dataMem["negOne"] = -1;

def sLess(instr,assem):
	#subtract a - b
	#if positive return 0
	#else flip result

	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	notPos = assem.getNextReserved("notPos");
	done = assem.getNextReserved("done");

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq(b,result));
	assem.progMem.append(subleq(a,result,notPos));
	assem.progMem.append(subleq(result,result,done));
	assem.progMem.append(next_subleq(notPos + ": " + t0,t0));
	assem.progMem.append(next_subleq(done + ": " + t0,result));

def sLessEq(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	less = assem.getNextReserved("less");
	done = assem.getNextReserved("done");

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq("negOne",result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(b,t0));
	assem.progMem.append(next_subleq(t0,c));
	assem.progMem.append(subleq(a,result,less));
	assem.progMem.append(subleq(t1,t1,done));
	assem.progMem.append(next_subleq(less + ": " + result,result));
	assem.progMem.append(next_subleq(done + ": " + t0,t0));

	if "negOne" not in assem.dataMem:
		assem.dataMem[negOne] = -1;

operations = {
	"eq" : equal,
	"ne" : notEqual,
	"sgt" : sGreater,
	"sge" : sGreaterEq,
	"slt" : sLess,
	"ste" : sLessEq
}