import re
from helpers import subleq
from helpers import next_subleq
from helpers import clear

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
		notPos = assem.getNextReserved("notPos");

		assem.progMem.append("\n// " + instr.raw);
                assem.subleq(t0,t0,"NEXT");
                assem.subleq(-1,t0,"NEXT");
                assem.subleq(a,t0,b);
                assem.subleq(t1,t1,"NEXT");
                assem.subleq(t0,t1,"NEXT");
                assem.subleq(-2,t1,b);
                assem.subleq(t0,t0,c);

                assem.dataMem[-1] = -1;
                assem.dataMem[-2] = -2;

def labelParseArgs(argStr):
    label = re.findall("\d+",argStr)[0];
    return ["%" + str(label)]

def label(instr, assem):
    assem.progMem.append("\n// " + instr.raw);
    assem.progMem.append(instr.args[0] + ":");

def returnParseArgs(argStr):
    arg = re.findall("(?<=i32)\s+\S+|void",argStr)[0];
    if arg == "void":
        arg = "__VOID__";

    return [arg];

def returnF(instr, assem):
    ret = instr.args[0];

    t0 = assem.getNextTemp();

    assem.progMem.append("\n// " + instr.raw)

    if ret != "__VOID__":
        assem.subleq("return", "return", "NEXT");
        assem.subleq(t0,t0,"NEXT");
        assem.subleq(ret,t0,"NEXT");
        assem.subleq(t0,"return","NEXT");
        assem.subleq(t0,t0,"#-1");

def callParseArgs(argStr):
    print argStr
    name = re.findall("(?<=i\d\d)\s+\S+(?=\()",argStr)[0].strip();
    argsRaw = re.findall("(?<=\().*(?=\))",argStr)[0].strip();
    args = argsRaw.split(",");

    for i in range(0,len(args)):
        args[i] = re.sub("i\d\d\s+","",args[i]).strip();

    return [name] + args;


def call(instr, assem):
    name = instr.args[0];
    args = instr.args[1:];

    if not name in builtInFunction:
        print "error - attempting to call non-built in function, don't support functions...yet"
        sys.exit(2);

    builtInFunction[name](instr, assem);

def getGlobalId(instr, assem):
    result = instr.result;
    dim = instr.args[1]; #args[0] contains the function name

    #add the literal to the data memory if necessary
    if re.match("-?\d+",dim.strip()):
        dim = dim.strip();
        assem.dataMem[dim] = dim;

    t0 = assem.getNextTemp();
    t1 = assem.getNextTemp();

    globIds = "glob_ids";
    glob_0 = assem.getNextReserved("glob_0");
    work_dim = "work_dims";
    error = assem.getNextReserved("dim_error");
    finish = assem.getNextReserved("finish");
    continue0 = assem.getNextReserved("continue");
    continue1 = assem.getNextReserved("continue");

    assem.progMem.append("\n// " + instr.raw);
    #check input is between 0 and work_dim() - 1
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(dim,t0,continue0);
    assem.subleq(t0,t0,error);
    assem.subleq(continue0 + ":1",t0,"NEXT");
    assem.subleq(t1,t1,"NEXT");
    assem.subleq(t0,t1,"NEXT");
    assem.subleq(work_dim,t1,continue1);
    assem.subleq(t0,t0,error);

    #get pointer value to the global id you want
    assem.subleq(continue1 + ":" + t0,t0,"NEXT");
    assem.subleq(globIds,t0,"NEXT");
    assem.subleq(dim,t0,"NEXT");  #make t0 = -globIds - dim so we don't have to flip it twice below
    
    #rewrite the instructions with the right global address
    assem.subleq(glob_0,glob_0,"NEXT");
    assem.subleq(t0,glob_0,"NEXT");

    #store the current index value in the result
    assem.subleq(result,result,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(glob_0 + ":#1",t0,"NEXT");
    assem.subleq(t0,result,"NEXT");  
    assem.subleq(t0,t0,finish);

    assem.subleq(error + ":" + result,result,"NEXT"); #return 0 in the case of invalid input ( < 0, > dim-1)
    assem.subleq(finish + ":" + t0,t0,"NEXT");
    
    assem.dataMem["1"] = 1;

def getWorkDim(instr, assem):
    result = instr.result;
    t0 = assem.getNextReserved();

    assem.subleq(result,result,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq("work_dims",t0,"NEXT");
    assem.subleq(t0,result,"NEXT");


builtInFunction = {
        "@get_global_id" : getGlobalId,
        "@get_work_dim" : getWorkDim
}
