import os, sys, globals
from collections import defaultdict


class DisplayShelf:

	def __init__(self):
		output = open(globals.project_name, 'w')
		output.write("PERCENT TRANSFERRED INFORMATION\n\n")
		output.close()


	def append_to_project(self, subjects, gates, segment, type, t, h, perc_ti):
		output = open(globals.project_name, 'a')
		output.write("Subjects:\t{0}\nGates:\t{1}\nSegment:\t{2}\nType:\t{3}\nT-value:\t{4}\nH-value:\t{5}\nPercent_TI-value:\t{6}\n".format(subjects, gates, segment, type, t, h, perc_ti))
		output.close()