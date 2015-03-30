import re

class Argument:

	def __init__(self, argStr):
		if argStr != "()":
                    name = re.findall("%\S+",argStr)[0];
                    dataType = re.findall("[^%@]+(?=[%@])",argStr)[0];
                    self.type = dataType.replace("(","").replace(")","");
                    self.name = name.replace("(","").replace(")","");
		else:
			self.type = "void";
			self.name = "";
