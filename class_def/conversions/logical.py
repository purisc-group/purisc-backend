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
	c = instr.result;
	a = instr.args[1];
	b = instr.args[2];

        t0 = assem.getNextTemp();

        done = assem.getNextReserved("done");
        aLE = assem.getNextReserved("aLE");
        true = assem.getNextReserved("true");

	#check for literal operands and add them to the datamemory if necessary
	literalPattern = re.compile("-?\d+");
	if literalPattern.match(a):
		if a not in assem.dataMem:
			assem.dataMem[a] = int(a);

	if literalPattern.match(b):
		if b not in assem.dataMem:
			assem.dataMem[b] = int(b);

	assem.progMem.append("\n// " + instr.raw);
        assem.subleq(c,c,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(t0,c,"NEXT");
        assem.subleq(b,c,aLE);
        assem.subleq(c,c,done);
        assem.subleq(aLE + ":" + t0,t0,"NEXT");
        assem.subleq(c,t0,true);
        assem.subleq(c,c,done);
        assem.subleq(true + ":" + "-1",c,"NEXT");
        assem.subleq(done + ":" + t0,t0,"NEXT"); #dummy

	assem.dataMem[-1] = -1;

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
        assem.subleq(result,result,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(t0,result,"NEXT");
        assem.subleq(b,result,"NEXT");

def sGreater(instr,assem):
	c = instr.result;
	a = instr.args[1];
	b = instr.args[2];

        t0 = assem.getNextTemp();

        false = assem.getNextReserved("false");
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
        assem.subleq(c,c,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(t0,c,"NEXT");
        assem.subleq(b,c,false);
        assem.subleq(t0,t0,done);
        assem.subleq(false + ":" + c,c,done);
        assem.subleq(done + ":" + t0,t0,"NEXT");

def sGreaterEq(instr,assem):
	c = instr.result;
	a = instr.args[1];
	b = instr.args[2];

        t0 = assem.getNextTemp();

        false = assem.getNextReserved("false");
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
        assem.subleq(c,c,"NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(a,t0,"NEXT");
        assem.subleq(t0,c,"NEXT");
        assem.subleq(-1,c,"NEXT");
        assem.subleq(b,c,false);
        assem.subleq(t0,t0,done);
        assem.subleq(false + ":" + c,c,done);
        assem.subleq(done + ":" + t0,t0,"NEXT");

        assem.dataMem[-1] = -1;

def sLess(instr,assem):
	temp = instr.args[2];
	instr.args[2] = instr.args[1];
        instr.args[1] = temp;

        sGreater(instr,assem);

def sLessEq(instr,assem):
        temp = instr.args[2];
        instr.args[2] = instr.args[1];
        instr.args[1] = temp;

        sGreaterEq(instr,assem);

operations = {
	"eq" : equal,
	"ne" : notEqual,
	"sgt" : sGreater,
	"sge" : sGreaterEq,
	"slt" : sLess,
	"sle" : sLessEq
}
