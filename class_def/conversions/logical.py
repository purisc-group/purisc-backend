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
	t0 = "t" + assem.stackCount;
	assem.stackCount += 1;

	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq(a,result));
	assem.progMem.append(subleq(b,result,"notPos"));
	assem.progMem.append(subleq(result,result,"done"));
	assem.progMem.append(subleq("notPost " + t0,t0,"NEXT"));
	assem.progMem.append(subleq(t0,result,"eq"));
	assem.progMem.append(subleq(result,result,"done"));
	assem.progMem.append(subleq("eq: " + str(1),result,"NEXT"));
	assem.progMem.append(subleq("done: " + t0,t0,NEXT));

def notEqual(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + assem.stackCount;
	assem.stackCount += 1;

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

	if "%" not in a and "@" not in a:
		print a
		aOld = a;
		a = "L" + str(a);
		if a not in assem.dataMem:
			assem.dataMem[a] = aOld;

	if "%" not in b and "@" not in b:
		print b
		aOld = b;
		b = "L" + str(b);
		if b not in assem.dataMem:
			assem.dataMem[b] = aOld;


	assem.progMem.append(clear(result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(a,t0));
	assem.progMem.append(next_subleq(t0,result));
	assem.progMem.append(subleq(b,result,"less"));
	assem.progMem.append(subleq(result,result,"done"));
	assem.progMem.append(next_subleq("less: " + result, result));
	assem.progMem.append(next_subleq("one",result));
	assem.progMem.append(next_subleq("done: " + t0,t0));

	print "here"
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

	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq("negOne",result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(a,t0));
	assem.progMem.append(next_subleq(t0,c));
	assem.progMem.append(subleq(b,result,"less"));
	assem.progMem.append(subleq(t1,t1,"done"));
	assem.progMem.append(next_subleq("less: " + result,result));
	assem.progMem.append(next_subleq("done: " + t0,t0));

	if "negOne" not in assem.dataMem:
		assem.dataMem[negOne] = -1;

def sLess(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	assem.progMem.append(clear(result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(b,t0));
	assem.progMem.append(next_subleq(t0,result));
	assem.progMem.append(subleq(a,result,"less"));
	assem.progMem.append(subleq(t1,t1,"done"));
	assem.progMem.append(next_subleq("less: " + result, result));
	assem.progMem.append(next_subleq("done: " + t0,t0));

def sLessEq(instr,assem):
	result = instr.result;
	a = instr.args[1];
	b = instr.args[2];
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	assem.progMem.append(clear(result));
	assem.progMem.append(next_subleq("negOne",result));
	assem.progMem.append(clear(t0));
	assem.progMem.append(next_subleq(b,t0));
	assem.progMem.append(next_subleq(t0,c));
	assem.progMem.append(subleq(a,result,"less"));
	assem.progMem.append(subleq(t1,t1,"done"));
	assem.progMem.append(next_subleq("less: " + result,result));
	assem.progMem.append(next_subleq("done: " + t0,t0));

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