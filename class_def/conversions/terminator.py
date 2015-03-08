import re
from helpers import subleq
from helpers import next_subleq

def branchParseArgs(argStr):
	args = [];
	condition = re.findall("(?<=i1\s)[^,]*(?=,)",argStr);

	if len(condition) > 0:
		args.append(condition[0]);
		args.append(re.findall("(?<=label\s)[^,]*(?=,)",argStr)[0]);
		args.append(re.findall("(?<=label\s)[^,]*$",argStr)[0]);

	else:
		args.append(re.findall("(?<=label\s).*",argStr)[0])

	return args

def branch(instr, assem):
#branch can take two forms: unconditional branch and a conditional branch
	t0 = "t" + str(assem.stackCount);
	assem.stackCount += 1;
	t1 = "t" + str(assem.stackCount);
	assem.stackCount += 1;

	if len(instr.args) == 1:
		#unconditional branch, the argument is actually a label
		assem.progMem.append(subleq(t0,t0,instr.args[0]));

	else:
		#conditional branch
		a = instr.args[0];
		b = instr.args[1];
		c = instr.args[2];
		assem.progMem.append(next_subleq(t0,t0));
		assem.progMem.append(subleq(a,t0,"notPos"));
		assem.progMem.append(subleq(t0,t0,b));
		assem.progMem.append(next_subleq("notPos: " + t1,t1));
		assem.progMem.append(subleq(t1,t0,c));
		assem.progMem.append(subleq(t1,t1,b));

def labelParseArgs(argStr):
	label = re.findall("\d+",argStr)[0];
	return ["%" + str(label)]

def label(instr, assem):
	assem.progMem.append(instr.args[0] + ":");