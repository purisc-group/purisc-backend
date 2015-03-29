from helpers import next_subleq
from helpers import subleq
from helpers import clear
import re

def add(instr, assem):
    arg1 = instr.args[0];
    arg2 = instr.args[1];
    result = instr.result;

    t0 = assem.getNextTemp();
    t1 = assem.getNextTemp();

    #check for literals
    if re.match("\d+",arg1):
        print arg1
        if arg1 not in assem.dataMem:
            assem.dataMem[arg1] = arg1;

    if re.match("\d+",arg2):
        print arg2
        if arg2 not in assem.dataMem:
            assem.dataMem[arg2] = arg2;

    assem.progMem.append("\n// " + instr.raw);
    assem.progMem.append(next_subleq(result,result));
    assem.progMem.append(clear(t0));
    assem.progMem.append(next_subleq(arg1,result));
    assem.progMem.append(clear(t1));
    assem.progMem.append(next_subleq(t1,result));
    assem.progMem.append(next_subleq(arg2,result));

def sub(instr, assem):
    arg1 = instr.args[0];
    arg2 = instr.args[1];
    result = instr.result;

    assem.progMem.append("\n // " + instr.raw);
    assem.progMem.append(clear(result))
    assem.progMem.append(next_subleq(arg2, result));
    assem.progMem.append(next_subleq(arg1, result));

def mul(instr, assem):
    arg1 = instr.args[0];
    brg2 = instr.args[1];
    c = instr.result;

    a = assem.getNextReserved("mul");
    b = assem.getNextReserved("mul");
    flip = assem.getNextReserved("flip");
    i = assem.getNextReserved("i");
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

    t0 = assem.getNextTemp();
    t1 = assem.getNextTemp();
    t3 = assem.getNextTemp();
    t4 = assem.getNextTemp();


    assem.progMem.append("\n// " + instr.raw);

    #determine the sign of the result
    assem.progMem.append(clear(c));
    assem.progMem.append(clear(a));
    assem.progMem.append(clear(b));
    assem.progMem.append(clear(flip));
    assem.progMem.append(subleq(a,t0,flipA));
    assem.progMem.append(subleq(t0,t0,checkB));
    assem.progMem.append(next_subleq(flipA + ": 0",a));
    assem.progMem.append(next_subleq(1,flip));
    assem.progMem.append(next_subleq(checkB + ": " + t0,t0));
    assem.progMem.append(subleq(b,t0,flipB));
    assem.progMem.append(subleq(t0,t0,continue1));
    assem.progMem.append(next_subleq(flipB + ": 0",b));
    assem.progMem.append(next_subleq(1,flip));

    #determine the operand
    assem.progMem.append(next_subleq(continue1 + ": " + b,t1));
    assem.progMem.append(subleq(a,t1,aLess));
    assem.progMem.append(next_subleq(b,operand));
    assem.progMem.append(next_subleq(a,power));
    assem.progMem.append(subleq(t0,t0,continue2));
    assem.progMem.append(next_subleq(aLess + ": " + a,operand));
    assem.progMem.append(next_subleq(b,power));

    #decompose the operand into powers of 2
    assem.progMem.append(next_subleq(continue2 + ": " + i,i));
    assem.progMem.append(next_subleq(30,i));
    assem.progMem.append(next_subleq(begin + ": " + decomp,decomp));
    assem.progMem.append(next_subleq(decomp_,decomp));
    assem.progMem.append(next_subleq(0,decomp));
    assem.progMem.append(next_subleq(i,decomp));
    assem.progMem.append(next_subleq(powers,powers));
    assem.progMem.append(next_subleq(p_,powers));
    assem.progMem.append(next_subleq(0,powers));
    assem.progMem.append(next_subleq(i,powers));
    assem.progMem.append(clear(p_0));
    assem.progMem.append(next_subleq(powers,p_0));
    assem.progMem.append(clear(d_0));
    assem.progMem.append(next_subleq(decomp,d_0));
    assem.progMem.append(clear(p_1));
    assem.progMem.append(next_subleq(powers,p_1));

    assem.progMem.append(next_subleq(p_0 + ": #1",operand));
    assem.progMem.append(subleq(1,operand,less));
    assem.progMem.append(next_subleq(1,d_0 + ":#1"));
    assem.progMem.append(next_subleq(1,operand));
    assem.progMem.append(next_subleq(0,operand));
    assem.progMem.append(subleq(t0,t0,test));
    assem.progMem.append(next_subleq(less + ": 1",operand));
    assem.progMem.append(next_subleq(p_1 + ":#1",operand));
    assem.progMem.append(next_subleq(test + ": 0",i));
    assem.progMem.append(next_subleq(-1,i));
    assem.progMem.append(subleq(1,operand,restore));
    assem.progMem.append(subleq(t0,t0,continue3));
    assem.progMem.append(next_subleq(restore + ": 1",operand));
    assem.progMem.append(subleq(t0,t0,begin));

    #do successive additions of powers of 2
    assem.progMem.append(next_subleq(continue3 + ": " + i,i));
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
    assem.progMem.append(next_subleq(finish + ": " + t0,t0)); #dummy


    assem.dataMem["1"] = "#1";
    assem.dataMem["-30"] = "#-30";
    assem.dataMem["0"] = "#0";
    assem.dataMem["30"] = "#30";
    assem.dataMem["-1"] = "#-1";
    assem.dataMem["2"] = "#2";

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

def parseArgs(argStr):

    arg1 = re.findall("(?<=\s)[^\s,]+(?=,)",argStr)[0];
    arg2 = re.findall("(?<=,\s)\s*\S+",argStr)[0];

    return [arg1.strip(),arg2.strip()]
