from collections import OrderedDict

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
        self.dataMem["work_dims"] = 11; #11 is the maximum number of dimensions allowed
        for i in range(0,11):
            self.dataMem["glob_ids" + str(i)] = 0;

        self.dataMem["glob_ids"] = "&glob_ids0";

        #allocate memory for the maximum id, if the id equals this value, the core knows to stop
        for i in range(0,11):
            self.dataMem["glob_idsMax" + str(i)] = 1; #default each dimension will run once, for the kernel to run at all
                                                       #each dimension must run at least once. If a dimension is unused, just
                                                       #don't touch the data and everything will work

        self.dataMem["glob_idsMax"] = "&glob_idsMax0";
