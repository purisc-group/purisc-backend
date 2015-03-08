def subleq(a, b, c):
	instr = "%s     %s     %s" % (a,b,c);
	return instr;

def next_subleq(a,b):
	return subleq(a,b,"NEXT");

def clear(a):
	return subleq(a,a,"NEXT");