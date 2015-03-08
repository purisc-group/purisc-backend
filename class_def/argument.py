import re

class Argument:

	def __init__(self, argStr):
		if argStr != "()":
			[dataType, name] = argStr.strip().split(" ");
			self.type = dataType.replace("(","").replace(")","");
			self.name = name.replace("(","").replace(")","");
		else:
			self.type = "void";
			self.name = "";