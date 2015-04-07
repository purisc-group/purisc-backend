from helpers import next_subleq
from helpers import subleq
from helpers import clear
import re

def add(instr, assem):
    a = instr.args[0];
    b = instr.args[1];
    c = instr.result;

    t0 = assem.getNextTemp();

    #check for literals
    if re.match("\d+",a):
        if a not in assem.dataMem:
            assem.dataMem[a] = a;

    if re.match("\d+",b):
        if b not in assem.dataMem:
            assem.dataMem[b] = b;

    assem.progMem.append("\n// " + instr.raw);
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(a,t0,"NEXT");
    assem.subleq(b,t0,"NEXT");
    assem.subleq(c,c,"NEXT");
    assem.subleq(t0,c,"NEXT");

def sub(instr, assem):
    a = instr.args[0];
    b = instr.args[1];
    c = instr.result;

    #check for literals
    if re.match("\d+",a):
        if a not in assem.dataMem:
            assem.dataMem[a] = a;

    if re.match("\d+",b):
        if b not in assem.dataMem:
            assem.dataMem[b] = b;

    assem.progMem.append("\n // " + instr.raw);
    assem.subleq(c,c,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(a,t0,"NEXT");
    assem.subleq(t0,c,"NEXT");
    assem.subleq(b,c,"NEXT");

def mul(instr, assem):
    arg1 = instr.args[0];
    arg2 = instr.args[1];
    result = instr.result;

    c = assem.getNextReserved("workingResult"); # will hold the value of the negative answer until it is flipped at the end if necessary
    a = assem.getNextReserved("mul");
    b = assem.getNextReserved("mul");
    flip = assem.getNextReserved("flip");
    i0 = assem.getNextReserved("i");
    operand = assem.getNextReserved("operand");
    power = assem.getNextReserved("power");
    decomp = assem.getNextReserved("decomp");
    decomp_ = assem.getNextReserved("mul_decomp_");
    powers = assem.getNextReserved("powers");
    p_ = "powersOf2_";

    #labels
    flipA = assem.getNextReserved("flipA");
    checkB = assem.getNextReserved("checkB");
    flipB = assem.getNextReserved("flipB");
    continue0 = assem.getNextReserved("continue0_");
    continue1 = assem.getNextReserved("continue1_");
    aLess = assem.getNextReserved("aLess");
    continue2 = assem.getNextReserved("continue2_");
    begin = assem.getNextReserved("begin");
    p_0 = assem.getNextReserved("p_0_");
    d_0 = assem.getNextReserved("d_0_");
    p_1 = assem.getNextReserved("p_1_");
    less = assem.getNextReserved("less");
    test = assem.getNextReserved("test");
    restore = assem.getNextReserved("restore");
    continue3 = assem.getNextReserved("continue3_");
    begin2 = assem.getNextReserved("begin2_");
    d_2 = assem.getNextReserved("d_2_");
    d_3 = assem.getNextReserved("d_3_");
    d_4 = assem.getNextReserved("d_4_");
    add = assem.getNextReserved("add");
    regardless = assem.getNextReserved("regardless");
    flipSign = assem.getNextReserved("flipSign");
    finish = assem.getNextReserved("finish");
    noflipA = assem.getNextReserved("noFlipA");
    noflipB = assem.getNextReserved("noFlipB");

    t0 = assem.getNextTemp();
    t1 = assem.getNextTemp();
    t3 = assem.getNextTemp();
    t4 = assem.getNextTemp();


    assem.progMem.append("\n// " + instr.raw);

    #determine the sign of the result
    assem.subleq(a,a,"NEXT"); #check the sign of A
    assem.subleq(b,b,"NEXT");
    assem.subleq(flip,flip,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(arg1,t0,noflipA);
    assem.subleq(t0,a,"NEXT");
    assem.subleq(1,flip,checkB);
    assem.subleq(noflipA + ":" + arg1,a,"NEXT");

    assem.subleq(checkB + ":" + t0,t0,"NEXT"); #check the sign of B
    assem.subleq(arg2,t0,noflipB);
    assem.subleq(t0,b,"NEXT");
    assem.subleq(-1,flip,"NEXT");
    assem.subleq(t0,t0,continue0);
    assem.subleq(noflipB + ":" + arg2,b,"NEXT");

    #determine the operand
    assem.subleq(continue0 + ":" + operand,operand,"NEXT");
    assem.subleq(power,power,"NEXT");
    assem.subleq(a,b,aLess);
    assem.subleq(a,power,"NEXT");
    assem.subleq(b,operand,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(power,t0,"NEXT");
    assem.subleq(t0,operand,"NEXT");
    assem.subleq(t0,t0,continue1);
    assem.subleq(aLess + ":" + a,operand,"NEXT");
    assem.subleq(b,power,"NEXT");
    assem.subleq(t0,t0,'NEXT');
    assem.subleq(operand,t0,"NEXT");
    assem.subleq(t0,power,"NEXT");

    #decompose the operand into powers of 2
    #maxPower = -1;
    # for i = 30 -> 0
        #if operand - 2^i >= 0
            #powers[i] = 1
            #operand = operand - 2^i
            #maxPower == -1
                #maxPower = i
            #if operand - 2^i == 0:
                #break;

    two_i = assem.getNextReserved("two_i");
    decomp_i = assem.getNextReserved("decomp_i");
    restore = assem.getNextReserved("restore");
    maxPower = assem.getNextReserved("maxPower");
    maxFlag = assem.getNextReserved("maxFlag");
    notMax = assem.getNextReserved("notMax");
    continue2 = assem.getNextReserved("continue2");
    incr0 = assem.getNextReserved("inc");
    loop0 = assem.getNextReserved("loop");
    t4 = assem.getNextTemp();

    assem.dataMem[-2] = -2;
    assem.dataMem[0] = 0;

    #setup loop
    assem.subleq(continue1 + ":" + i0,i0,"NEXT");
    assem.subleq(-30,i0,"NEXT");
    assem.subleq(two_i,two_i,"NEXT");
    assem.subleq("powersOf2_",two_i,"NEXT");
    assem.subleq(30,two_i,"NEXT");
    assem.subleq(decomp_i,decomp_i,"NEXT");
    assem.subleq("mul_decomp_",decomp_i,"NEXT");
    assem.subleq(30,decomp_i,"NEXT");
    assem.subleq(maxPower,maxPower,"NEXT");
    assem.subleq(maxFlag,maxFlag,"NEXT");
    assem.subleq(-2,maxFlag, "NEXT");

    assem.subleq(loop0 + ":" + p_0,p_0,"NEXT");
    assem.subleq(two_i,p_0,"NEXT");
    assem.subleq(d_0,d_0,"NEXT");
    assem.subleq(decomp_i,d_0,"NEXT");
    assem.subleq(p_1,p_1,"NEXT");
    assem.subleq(two_i,p_1,"NEXT");
    assem.subleq(p_0 + ":#1",operand,"NEXT");  #operand = operand - 2^i
    assem.subleq(-1,operand,restore);   #add one to handle zero case
    assem.subleq(1,operand,"NEXT");
    assem.subleq(-1,d_0 + ":#1","NEXT"); #subtract the one
    assem.subleq(1,maxFlag,notMax);
    assem.subleq(i0,maxPower,"NEXT");
    assem.subleq(notMax + ":0",operand,continue2);
    assem.subleq(t0,t0,incr0);
    assem.subleq(restore + ":" + t0,t0,"NEXT");
    assem.subleq(p_1 + ":#1",t0,"NEXT");
    assem.subleq(t0,operand,"NEXT");
    assem.subleq(1,operand,"NEXT");

    #decrement and repeat if necessary
    assem.subleq(incr0 + ":-1",decomp_i,"NEXT");
    assem.subleq(-1,two_i,"NEXT");
    assem.subleq(1,i0,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(i0,t0,loop0);



    #do successive additions of powers of 2
    i1 = assem.getNextReserved("i");
    adder = assem.getNextReserved("adder");
    op = assem.getNextReserved("op");
    loop2 = assem.getNextReserved("loop");
    continue3 = assem.getNextReserved("continue3");
    continueLoop = assem.getNextReserved("contLoop");
    d_3 = assem.getNextReserved("d_3");
    noADD = assem.getNextReserved("noAdd");


    assem.subleq(continue2 + ":" + i1,i1,"NEXT");
    assem.subleq("2938483",t0,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(maxPower,t0,"NEXT")
    assem.subleq(t1,t1,"NEXT");
    assem.subleq(t0,t1,"NEXT");
    assem.subleq(maxPower,maxPower,"NEXT");
    assem.subleq(t1,maxPower,"NEXT");
    assem.subleq(adder,adder,"NEXT");
    assem.subleq(op,op,"NEXT");
    assem.subleq(power,op,"NEXT");
    assem.subleq(op,adder,'NEXT');
    assem.subleq(decomp_i,decomp_i,"NEXT");
    assem.subleq("mul_decomp_",decomp_i,"NEXT");
    assem.subleq(c,c,"NEXT");

    assem.subleq(loop2 + ":" + maxPower,i1,continueLoop);  #for i = 0 -> maxPower
    assem.subleq(t0,t0,continue3);
    assem.subleq(continueLoop + ":" + t0,t0,"NEXT");
    assem.subleq(d_3,d_3,"NEXT");
    assem.subleq(decomp_i,d_3,"NEXT");
    assem.subleq(maxPower,t0,"NEXT"); #restore i to what it was before comparison
    assem.subleq(t0,i1,"NEXT");
    assem.subleq(0,d_3 + ":#1",noADD);
    assem.subleq(adder,c,"NEXT");
    assem.subleq(noADD + ":" + t0,t0,"NEXT");
    assem.subleq(adder,t0,"NEXT");
    assem.subleq(t0,adder,"NEXT");

    #increment stuff
    assem.subleq(-1,i1,"NEXT");
    assem.subleq(1,decomp_i,"NEXT");
    assem.subleq(t0,t0,loop2);
    
    assem.subleq(continue3 + ":" + t0,t0,"NEXT");
    
    #determine sign. c is the negative right now so flip if flip flag == 0
    done = assem.getNextReserved("done");
    ansPos = assem.getNextReserved("ansPos");
    ansNeg = assem.getNextReserved("ansNeg");

    '''assem.subleq(result,result,"NEXT");
    assem.subleq(flip,result,"NEXT");
    assem.subleq(t0,t0,"#-1");'''

    assem.subleq(-1,flip,ansNeg);
    assem.subleq(1,flip,ansPos);
    assem.subleq(t0,t0,ansNeg);
    assem.subleq(ansPos + ":" + result,result,"NEXT");
    assem.subleq(c,result,"NEXT");
    assem.subleq(t0,t0,done);
    assem.subleq(ansNeg + ":" + t0,t0,"NEXT");
    assem.subleq(c,t0,"NEXT");
    assem.subleq(t0,result,"NEXT");
    assem.subleq(done + ":" + t0,t0,"NEXT");

    

    '''
    assem.progMem.append(next_subleq(continue2 + ": " + i,i));
    assem.progMem.append(next_subleq(begin2 + ": " + decomp,decomp));
    assem.progMem.append(next_subleq(decomp_,decomp));
    assem.progMem.append(next_subleq(0,decomp));
    assem.progMem.append(next_subleq(i,decomp));

    assem.progMem.append(clear(d_2));
    assem.progMem.append(next_subleq(decomp,d_2));
    assem.progMem.append(clear(d_3));
    assem.progMem.append(next_subleq(decomp,d_3));
    assem.progMem.append(clear(d_4));
    assem.progMem.append(next_subleq(decomp,d_4));

    assem.progMem.append(subleq(1,d_2 + ":#1",add));
    assem.progMem.append(subleq(d_3 + ":#1",d_4 + ":#1", regardless));
    assem.progMem.append(next_subleq(add + ": 0",c));
    assem.progMem.append(next_subleq(power,c));
    assem.progMem.append(next_subleq(regardless + ": " + t3,t3));
    assem.progMem.append(next_subleq(power,t3));
    assem.progMem.append(next_subleq(0,power));
    assem.progMem.append(next_subleq(t3,power));
    assem.progMem.append(next_subleq(0,i));
    assem.progMem.append(next_subleq(1,i));
    assem.progMem.append(next_subleq(t4,t4));
    assem.progMem.append(next_subleq(i,t4));
    assem.progMem.append(next_subleq(0,t4));
    assem.progMem.append(subleq(-30,t4,begin2));

    #flip the sign if necessary
    assem.progMem.append(subleq(1,flip,flipSign));
    assem.progMem.append(subleq(t0,t0,finish));

    assem.progMem.append(next_subleq(flipSign + ": 0",c));
    assem.progMem.append(next_subleq(finish + ": " + t0,t0)); #dummy'''


    assem.dataMem["1"] = "#1";
    assem.dataMem["-30"] = "#-30";
    assem.dataMem["0"] = "#0";
    assem.dataMem["30"] = "#30";
    assem.dataMem["-1"] = "#-1";
    assem.dataMem["2"] = "#2";
    assem.dataMem["2938483"] = "#2938483";

    #space for the powers of 2
    assem.dataMem["powersOf2_1"] = "#1"
    assem.dataMem["powersOf2_2"] = "#2"
    assem.dataMem["powersOf2_4"] = "#4"
    assem.dataMem["powersOf2_8"] = "#8"
    assem.dataMem["powersOf2_16"] = "#16"
    assem.dataMem["powersOf2_32"] = "#32"
    assem.dataMem["powersOf2_64"] = "#64"
    assem.dataMem["powersOf2_128"] = "#128"
    assem.dataMem["powersOf2_256"] = "#256"
    assem.dataMem["powersOf2_512"] = "#512"
    assem.dataMem["powersOf2_1024"] = "#1024"
    assem.dataMem["powersOf2_2048"] = "#2048"
    assem.dataMem["powersOf2_4096"] = "#4096"
    assem.dataMem["powersOf2_8192"] = "#8192"
    assem.dataMem["powersOf2_16384"] = "#16384"
    assem.dataMem["powersOf2_32768"] = "#32768"
    assem.dataMem["powersOf2_65536"] = "#65536"
    assem.dataMem["powersOf2_131072"] = "#131072"
    assem.dataMem["powersOf2_262144"] = "#262144"
    assem.dataMem["powersOf2_524288"] = "#524288"
    assem.dataMem["powersOf2_1048576"] = "#1048576"
    assem.dataMem["powersOf2_2097152"] = "#2097152"
    assem.dataMem["powersOf2_4194304"] = "#4194304"
    assem.dataMem["powersOf2_8388608"] = "#8388608"
    assem.dataMem["powersOf2_16777216"] = "#16777216"
    assem.dataMem["powersOf2_33554432"] = "#33554432"
    assem.dataMem["powersOf2_67108864"] = "#67108864"
    assem.dataMem["powersOf2_134217728"] = "#134217728"
    assem.dataMem["powersOf2_268435456"] = "#268435456"
    assem.dataMem["powersOf2_536870912"] = "#536870912"
    assem.dataMem["powersOf2_1073741824"] = "#1073741824"
    assem.dataMem["powersOf2_"] = "&powersOf2_1"


    #space for the decomposition, will be reused every multiplication
    assem.dataMem["mul_decomp_0"] = "#0"
    assem.dataMem["mul_decomp_1"] = "#0"
    assem.dataMem["mul_decomp_2"] = "#0"
    assem.dataMem["mul_decomp_3"] = "#0"
    assem.dataMem["mul_decomp_4"] = "#0"
    assem.dataMem["mul_decomp_5"] = "#0"
    assem.dataMem["mul_decomp_6"] = "#0"
    assem.dataMem["mul_decomp_7"] = "#0"
    assem.dataMem["mul_decomp_8"] = "#0"
    assem.dataMem["mul_decomp_9"] = "#0"
    assem.dataMem["mul_decomp_10"] = "#0"
    assem.dataMem["mul_decomp_11"] = "#0"
    assem.dataMem["mul_decomp_12"] = "#0"
    assem.dataMem["mul_decomp_13"] = "#0"
    assem.dataMem["mul_decomp_14"] = "#0"
    assem.dataMem["mul_decomp_15"] = "#0"
    assem.dataMem["mul_decomp_16"] = "#0"
    assem.dataMem["mul_decomp_17"] = "#0"
    assem.dataMem["mul_decomp_18"] = "#0"
    assem.dataMem["mul_decomp_19"] = "#0"
    assem.dataMem["mul_decomp_20"] = "#0"
    assem.dataMem["mul_decomp_21"] = "#0"
    assem.dataMem["mul_decomp_22"] = "#0"
    assem.dataMem["mul_decomp_23"] = "#0"
    assem.dataMem["mul_decomp_24"] = "#0"
    assem.dataMem["mul_decomp_25"] = "#0"
    assem.dataMem["mul_decomp_26"] = "#0"
    assem.dataMem["mul_decomp_27"] = "#0"
    assem.dataMem["mul_decomp_28"] = "#0"
    assem.dataMem["mul_decomp_29"] = "#0"
    assem.dataMem["mul_decomp_30"] = "#0"
    assem.dataMem["mul_decomp_"] = "&mul_decomp_0"

def div(instr, assem):
    arg1 = instr.args[0];
    arg2 = instr.args[1];
    c = instr.result;

    a = assem.getNextReserved("A");
    b = assem.getNextReserved("B");
    num = assem.getNextReserved("num");
    denom = assem.getNextReserved("denom");

    t0 = assem.getNextTemp();
    t1 = assem.getNextTemp();

    flip = assem.getNextReserved("flip");
    noflipA = assem.getNextReserved("noflipA");
    noflipB = assem.getNextReserved("noflipB");
    checkB = assem.getNextReserved("checkB");
    continue0 = assem.getNextReserved("continue");
    continue1 = assem.getNextReserved("continue");
    zero = assem.getNextReserved("zero");
    done = assem.getNextReserved("done");

    i0 = assem.getNextReserved("i");
    loop0 = assem.getNextReserved("loop");
    d_0 = assem.getNextReserved("d_0");
    d_1 = assem.getNextReserved("d_1");
    d_2 = assem.getNextReserved("d_2");
    d_3 = assem.getNextReserved("d_3");
    d_prev_0 = assem.getNextReserved("d_prev_0");
    d_prev_1 = assem.getNextReserved("d_prev_1");
    d_prev_2 = assem.getNextReserved("d_prev_2");

    assem.progMem.append("\n// " + instr.raw);

    #check for signs
    assem.subleq(a,a,"NEXT"); #check the sign of A
    assem.subleq(b,b,"NEXT");
    assem.subleq(flip,flip,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(arg1,t0,noflipA);
    assem.subleq(arg1,a,"NEXT");
    assem.subleq(1,flip,checkB);
    assem.subleq(noflipA + ":" + t0,a,"NEXT");

    assem.subleq(checkB + ":" + t0,t0,"NEXT"); #check the sign of B
    assem.subleq(arg2,t0,noflipB);
    assem.subleq(t0,b,"NEXT");
    assem.subleq(-1,flip,"NEXT");
    assem.subleq(t0,t0,continue1);
    assem.subleq(noflipB + ":" + arg2,b,"NEXT");

    #compute d*2^i
    assem.subleq(continue1 + ":" + b,"div_d_pwrs_0","NEXT");

    assem.subleq(i0,i0,"NEXT");
    assem.subleq(-1,i0,"NEXT");
      #for i = 1 -> 30
    assem.subleq(loop0 + ":" + t0,t0,"NEXT");
    assem.subleq(t1,t1,"NEXT");
    assem.subleq("div_d_pwrs_",t1,"NEXT"); #dereference d[i]
    assem.subleq(i0,t1,"NEXT");

    assem.subleq(d_0,d_0,"NEXT"); #change the appropriate instructions pointing to d[i]
    assem.subleq(t1,d_0,"NEXT");
    assem.subleq(d_1,d_1,"NEXT");
    assem.subleq(t1,d_1,"NEXT");
    assem.subleq(d_2,d_2,"NEXT");
    assem.subleq(t1,d_2,"NEXT");
    assem.subleq(d_3,d_3,"NEXT");
    assem.subleq(t1,d_3,"NEXT");

    assem.subleq(-1,t1,"NEXT"); #dereference d[i-1]
    assem.subleq(d_prev_0,d_prev_0,"NEXT"); #rewrite the appropriate instructions pointing to d[i-1]
    assem.subleq(t1,d_prev_0,"NEXT");

    assem.subleq(d_prev_0 + ":#1",t0,"NEXT");
    assem.subleq(d_0 + ":#1",d_1 + ":#1", "NEXT");
    assem.subleq(t0,d_2 + ":#1","NEXT");
    assem.subleq(t0,d_3 + ":#1","NEXT");

    assem.subleq(-1,i0,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(i0,t0,"NEXT");
    assem.subleq(t1,t1,"NEXT");
    assem.subleq(t0,t1,"NEXT");
    assem.subleq(30,t1,loop0);


    #for i = 30 -> 0
        #if n - d*2^i >= 0
            #n = n - d
            #result += 2^i
            # if n-d*2^i == 0
                #break

    loop1 = assem.getNextReserved("loop");
    n = assem.getNextReserved("n");
    i1 = assem.getNextReserved("i");
    inc = assem.getNextReserved("inc");
    restore = assem.getNextReserved("restore");
    break0 = assem.getNextReserved("break0");
    continue2 = assem.getNextReserved("continue2");
    d_i = "d_i";   #pointer to d*2^i
    two_i = "two_i"; #pointer to 2^i
    d_0 = assem.getNextReserved("d_0");
    d_1 = assem.getNextReserved("d_1");
    p_0 = assem.getNextReserved("p_0");


    assem.subleq(c,c,"NEXT");
    assem.subleq(n,n,"NEXT"); #setupt loop
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(a,t0,"NEXT");
    assem.subleq(t0,n,"NEXT")
    assem.subleq(i1,i1,"NEXT");
    assem.subleq(-30,i1,"NEXT");

    assem.subleq(loop1 + ":" + d_0,d_0,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(d_i,t0,"NEXT");
    assem.subleq(t0,d_0,"NEXT");
    assem.subleq(d_1,d_1,"NEXT");
    assem.subleq(t0,d_1,"NEXT");
    assem.subleq(p_0,p_0,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(two_i,t0,"NEXT");
    assem.subleq(t0,p_0,"NEXT");

    assem.subleq(d_0 + ":#1",n,"NEXT");
    assem.subleq(-1,n,restore);
    assem.subleq(t1,t1,"NEXT");
    assem.subleq(p_0 + ":#1",t1,"NEXT");
    assem.subleq(t1,c,"NEXT");
    assem.subleq(1,n,break0); #restore n to n = n -d*2^i and also break if necessary
    assem.subleq(t0,t0,inc);
    assem.subleq(break0 + ":" + t0,t0,continue2);
    assem.subleq(restore + ":" + t0,t0,"NEXT");
    assem.subleq(d_1 + ":#1",t0,"NEXT");
    assem.subleq(t0,n,"NEXT");
    assem.subleq(1,n,"NEXT");

    assem.subleq(inc + ":1",i1,"NEXT"); #decrement and check
    assem.subleq(1,d_i,"NEXT");
    assem.subleq(1,two_i,"NEXT");
    assem.subleq(t0,t0,"NEXT");
    assem.subleq(i1,t0,loop1);
    #assem.subleq(continue2 + ":" + t0,t0,"NEXT");

    #fli if necessary
    flipResult = assem.getNextReserved("flipResult");

    assem.subleq(continue2 +":-1" ,flip,flipResult);
    assem.subleq(1,flip,done);
    assem.subleq(flipResult + ":" + t0,t0,"NEXT");
    assem.subleq(c,t0,"NEXT");
    assem.subleq(c,c,"NEXT");
    assem.subleq(t1,t1,"NEXT");
    assem.subleq(t0,t1,"NEXT");
    assem.subleq(t1,c,"NEXT");

    #done
    assem.subleq(done + ":" + t0,t0,"NEXT");


    assem.dataMem[-1] = -1;
    assem.dataMem[1] = 1;
    assem.dataMem[30] = 30;
    assem.dataMem[-30] = -30;


    assem.dataMem["div_d_pwrs_0"] = "#0"
    assem.dataMem["div_d_pwrs_1"] = "#0"
    assem.dataMem["div_d_pwrs_2"] = "#0"
    assem.dataMem["div_d_pwrs_3"] = "#0"
    assem.dataMem["div_d_pwrs_4"] = "#0"
    assem.dataMem["div_d_pwrs_5"] = "#0"
    assem.dataMem["div_d_pwrs_6"] = "#0"
    assem.dataMem["div_d_pwrs_7"] = "#0"
    assem.dataMem["div_d_pwrs_8"] = "#0"
    assem.dataMem["div_d_pwrs_9"] = "#0"
    assem.dataMem["div_d_pwrs_10"] = "#0"
    assem.dataMem["div_d_pwrs_11"] = "#0"
    assem.dataMem["div_d_pwrs_12"] = "#0"
    assem.dataMem["div_d_pwrs_13"] = "#0"
    assem.dataMem["div_d_pwrs_14"] = "#0"
    assem.dataMem["div_d_pwrs_15"] = "#0"
    assem.dataMem["div_d_pwrs_16"] = "#0"
    assem.dataMem["div_d_pwrs_17"] = "#0"
    assem.dataMem["div_d_pwrs_18"] = "#0"
    assem.dataMem["div_d_pwrs_19"] = "#0"
    assem.dataMem["div_d_pwrs_20"] = "#0"
    assem.dataMem["div_d_pwrs_21"] = "#0"
    assem.dataMem["div_d_pwrs_22"] = "#0"
    assem.dataMem["div_d_pwrs_23"] = "#0"
    assem.dataMem["div_d_pwrs_24"] = "#0"
    assem.dataMem["div_d_pwrs_25"] = "#0"
    assem.dataMem["div_d_pwrs_26"] = "#0"
    assem.dataMem["div_d_pwrs_27"] = "#0"
    assem.dataMem["div_d_pwrs_28"] = "#0"
    assem.dataMem["div_d_pwrs_29"] = "#0"
    assem.dataMem["div_d_pwrs_30"] = "#0"
    assem.dataMem["div_d_pwrs_"] = "&div_d_pwrs_0"

    assem.dataMem["powersOf2_1"] = "#1"
    assem.dataMem["powersOf2_2"] = "#2"
    assem.dataMem["powersOf2_4"] = "#4"
    assem.dataMem["powersOf2_8"] = "#8"
    assem.dataMem["powersOf2_16"] = "#16"
    assem.dataMem["powersOf2_32"] = "#32"
    assem.dataMem["powersOf2_64"] = "#64"
    assem.dataMem["powersOf2_128"] = "#128"
    assem.dataMem["powersOf2_256"] = "#256"
    assem.dataMem["powersOf2_512"] = "#512"
    assem.dataMem["powersOf2_1024"] = "#1024"
    assem.dataMem["powersOf2_2048"] = "#2048"
    assem.dataMem["powersOf2_4096"] = "#4096"
    assem.dataMem["powersOf2_8192"] = "#8192"
    assem.dataMem["powersOf2_16384"] = "#16384"
    assem.dataMem["powersOf2_32768"] = "#32768"
    assem.dataMem["powersOf2_65536"] = "#65536"
    assem.dataMem["powersOf2_131072"] = "#131072"
    assem.dataMem["powersOf2_262144"] = "#262144"
    assem.dataMem["powersOf2_524288"] = "#524288"
    assem.dataMem["powersOf2_1048576"] = "#1048576"
    assem.dataMem["powersOf2_2097152"] = "#2097152"
    assem.dataMem["powersOf2_4194304"] = "#4194304"
    assem.dataMem["powersOf2_8388608"] = "#8388608"
    assem.dataMem["powersOf2_16777216"] = "#16777216"
    assem.dataMem["powersOf2_33554432"] = "#33554432"
    assem.dataMem["powersOf2_67108864"] = "#67108864"
    assem.dataMem["powersOf2_134217728"] = "#134217728"
    assem.dataMem["powersOf2_268435456"] = "#268435456"
    assem.dataMem["powersOf2_536870912"] = "#536870912"
    assem.dataMem["powersOf2_1073741824"] = "#1073741824"
    assem.dataMem["powersOf2_"] = "&powersOf2_1"

    assem.dataMem["d_i"] = "&div_d_pwrs_30";
    assem.dataMem["two_i"] = "&powersOf2_1073741824";

def parseArgs(argStr):

    arg1 = re.findall("(?<=\s)[^\s,]+(?=,)",argStr)[0];
    arg2 = re.findall("(?<=,\s)\s*\S+",argStr)[0];

    return [arg1.strip(),arg2.strip()]
