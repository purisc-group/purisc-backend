from helpers import next_subleq as subleq
from helpers import clear

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
	
	assem.progMem.append(clear(arg2));
	assem.progMem.append(subleq(arg1,arg2));

def load(instr, assem):
	arg1 = instr.args[0];
	result = instr.result;

	assem.progMem.append(clear(result));
	assem.progMem.append(subleq(arg1,result));