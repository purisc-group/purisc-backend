import re
from class_def.function import Function
from class_def.assembly import Assembly
import sys, getopt

def main(argv):
    compilerVersion = 0.1;
    [inputFileName, outputFileName, fVerbose, debugging] = parseCmdArgs(argv);

    inputFile = open(inputFileName,'r');
    inputString = inputFile.read();
    inputFile.close();

    functions = [];

    #walk through the input file, parsing each function and creating a function 
    #class for each function
    currentIndex = inputString.find("define", 0);
    while(currentIndex != -1):
        endIndex = inputString.find("}",currentIndex);
        functions.append(Function(inputString[currentIndex:endIndex]));
        currentIndex = inputString.find("define",endIndex);


    #struct containing compiler information
    assem = Assembly();

    #walk through each function and generate subleq assembly
    for function in functions:
        for instruction in function.instructions:
            instruction.generateSubleq(instruction,assem);

    output = open(outputFileName,"w");
    output.write("//Compiler with j-backend-" + str(compilerVersion) + "\n");
    output.write("PROGRAM_MEM:\n\n");

    filt = re.compile("\s*//.*");
    for line in assem.progMem:

        #filter out comments if debugging flag is set
        if debugging:
            lineToWrite = line;
        else:
            lineToWrite = filt.sub("",line);
        
        if line[-1] != ":":
            lineToWrite += "\n";
            
        output.write(lineToWrite);
        if fVerbose:
            print lineToWrite;


    output.write("\n\n");
    output.write("DATA_MEM:\n\n");
    for mem in assem.dataMem:
        lineToWrite = mem + ":";
        lineToWrite += "#" + str(assem.dataMem[mem]) + "\n";

        output.write(lineToWrite);
        if fVerbose:
            print lineToWrite;

    output.close();

def parseCmdArgs(argv):
    inputFileName = "input.ll";
    outputFileName = "";
    fVerbose = False;
    debugging = False;

#Command line arguments
    try:
        opts, args = getopt.getopt(argv, "i:o:vd")
    except getopt.GetoptError:
        print "Usage: python",sys.argv[0],"[-i inputfile] [-o outputfile] [-v] [-d]"
        sys.exit(2);

    for opt, arg in opts:
        if opt in ("-i", "--infile"):
            inputFileName = arg;

        elif opt in ("-o", "--outfile"):
            outputFileName = arg;
                
        elif opt == "-v":
            fVerbose = True;

        elif opt == "-d":
            debugging = True;

    if outputFileName == "":
        endIndex = inputFileName.rfind(".");
        if endIndex == -1:
            endIndex = len(inputFileName);

        outputFileName = inputFileName[:endIndex] + ".subleq";

    return inputFileName, outputFileName, fVerbose, debugging;

if __name__ == '__main__':
    main(sys.argv[1:]);