import os, sys, globs
from collections import defaultdict


class DisplayShelf:

	def __init__(self):
		if os.path.exists(globs.project_name):
			pass
		else:
			self.output = open(globs.project_name, 'w')
			self.output.write("PERCENT TRANSFERRED INFORMATION\n\n")
			self.output.close()


	def append_to_project(self, subjects, gates, segment, sound, final_vals):
		self.output = open(globs.project_name, 'a')

		self.output.write("Subjects:\t{0}\nGates:\t{1}\nSegment:\t{2}\nType:\t{3}\nConstraints:\t{8}\nCategory Tested:\t{7}\nT-value:\t{4}\nH-value:\t{5}\nPercent_TI-value:\t{6}\n\n".format(subjects,gates,segment,sound,final_vals[2][0],final_vals[2][1],final_vals[2][2],final_vals[1],final_vals[0]))
		


	def store(self):
		self.output.close()