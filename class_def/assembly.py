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