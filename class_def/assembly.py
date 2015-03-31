from collections import OrderedDict
from conversions.helpers import *

class Assembly:
    def __init__(self):
        self.dataMem = OrderedDict(); 
        self.progMem = [];
        #count of the last temp variable used
        #if is count=3 then t3 was used last
        self.stackCount = 0;
        #list of number of times a reserved word was used
        self.reservedCount = {};
        self.allocateGlobalIdMem();

    #call this to get a keyword with a count appended to it to
    #avoid multiple label pointing to different locations
    def getNextReserved(self,keyword):
        if keyword in self.reservedCount:
            self.reservedCount[keyword] += 1;

        else:
            self.reservedCount[keyword] = 0;

        return str(keyword) + str(self.reservedCount[keyword]);

    def getNextTemp(self):
        temp = "t" + str(self.stackCount);
        self.stackCount +=1;
        return temp;

    def allocateGlobalIdMem(self):

        #allocate memory for global ids
        self.dataMem["work_dims"] = "$work_dimensions"; #11 is the maximum number of dimensions allowed
        for i in range(0,11):
            self.dataMem["glob_ids" + str(i)] = "$_initIndex" + str(i);

        self.dataMem["glob_ids"] = "&glob_ids0";

        #allocate memory for the maximum id, if the id equals this value, the core knows to stop
        for i in range(0,11):
            self.dataMem["glob_idsMax" + str(i)] = "$_maxIndex" + str(i); 

        self.dataMem["glob_idsMax"] = "&glob_idsMax0";

    def generateKernelLoop(self):

        for i in range(0,11):
            t0 = self.getNextTemp();
            dim = "dim" + str(i);
            globalMax = "glob_idsMax" + str(i);
            globalIds = "glob_ids" + str(i);
            finish = self.getNextReserved("finish");

            #put the beginning of the loop before everything
            self.progMem.insert(0,subleq(globalMax,t0,finish));
            self.progMem.insert(0,next_subleq(globalIds,t0));
            self.progMem.insert(0,next_subleq(dim + ":" + t0,t0));

            #put the increment stage at the end of everything
            self.progMem.append(next_subleq(0,globalIds));
            self.progMem.append(next_subleq(1,globalIds));
            self.progMem.append(subleq(t0,t0,dim));
            self.progMem.append(next_subleq(finish + ":" + t0,t0));

        self.dataMem["0"] = 0;
        self.dataMem["1"] = 1;
