import os, sys, re, globs
from collections import defaultdict
from os.path import join
from workshop import Workbench
from retreive_data import ExcelReader, SetOutputPath
from Percent_TI import Calculator
from display_case import DisplayShelf

globs.init()
display_shelf = DisplayShelf()

class Edit_Values:

	def __init__(self):

		self.new_values = " "
		self.additional_values = " "		
		self.removed_values = " "
	
	def new(self, blank_list):
		print "Enter values to be in list with single-space separation, e.g. '1 2 10...', or, as single numbers followed by an [enter] keystroke, e.g. 1 [enter] 2 [enter] ...\n"
		print "Press a final [enter] when finished to return to initial setup menu.\n"
		
		while self.new_values != "":
			self.new_values = raw_input("")
			
			blank_list += self.new_values.split()
		
		self.new_values = " "
		return list(set(blank_list))  #done to ensure no duplication of values
	
	def add(self, filled_list):
		print "Enter multiple values to add with single-space separation, e.g. '1 2 10...', or, as single numbers followed by an [enter] keystroke, e.g. 1 [enter] 2 [enter] ...\n"
		print "Press a final [enter] when finished to return to initial setup menu.\n"
			
		while self.additional_values != "":
			self.additional_values = raw_input("")
			
			filled_list += self.additional_values.split()
		
		self.additional_values = " "
		return list(set(filled_list)) 	#done to ensure no duplication of values
	
	def rm(self, filled_list):
		print "Enter multiple values to remove with single-space separation, e.g. '1 2 10...', or, as single numbers followed by an [enter] keystroke, e.g. 1 [enter] 2 [enter] ...\n"
		print "Press a final [enter] when finished to return to initial setup menu.\n"
		
		while self.removed_values != "":
			self.removed_values = raw_input("")
			print filled_list, type(filled_list)
			for value in self.removed_values.split():
				try:
					filled_list.remove(int(value))
				except ValueError:
					print 'error'
					pass
			print filled_list, type(filled_list)
		self.removed_values = " "
		return filled_list
	

class Not_Main:
	
	def __init__(self):
	
		#establishes initial setup values; assume all subjects, all gates, first segment, and consonants
		self.subject_list = range(1,29)
		self.missing_subjects = [6,8,9,13,14,18,19,23]
		
		for num in self.missing_subjects:
			self.subject_list.remove(num)

		self.gate_list = range(1,7)
		
		self.segment = "1"
		
		self.type = "C"

		

		self.edit = Edit_Values()

		
		
	def run(self):
		#this is the main function calling all others
		
		#will obtain user input, which can alter the established initial setup values
		self.command = "-"

		print "Enter initial setup commands\nPress [enter] to use default values, or submit commands and press [enter] when finished editing values\n"

		self.get_input()
		
		excel_reader = ExcelReader()

		self.target_sheet = excel_reader.identify_sheet(self.segment, self.type)

		self.confusion_dict = excel_reader.extract_values(self.target_sheet, self.subject_list, self.gate_list)
		
		excel_reader.root.destroy()

		#import module which acts as the "workbench" for specifying the necessary calculations
		workbench = Workbench(self.confusion_dict)


		for calculation in workbench.calculated_information:
			display_shelf.append_to_project(self.subject_list, self.gate_list, self.segment, self.type, calculation)
	
		while True:
			repeat = raw_input("Would you like to run any additional calculations?\nTo return to the initial setup menu, type 'return' and hit [enter]. To exit the program, type 'exit' [enter].\n")
		
			if repeat.strip() == 'return':
				self.run()
			if repeat.strip() == 'exit':
				display_shelf.store()
				break
			else:
				print "You must enter a valid input."


	def get_input(self):
		while self.command != "":
			
			self.command = raw_input("")
			
			if self.command == "":
				print "Below are your initial setup values.\n"
				print "Subject(s): {0}\n".format(self.subject_list)
				print "Gate(s): {0}\n".format(self.gate_list)
				print "Segment: {0}\n".format(self.segment)
				print "Type: {0}\n".format(self.type.replace("C","Consonant").replace("V","Vowel"))
				print "If these are the correct values, press [enter].  Otherwise, type 'return' and press [enter].\n"
				self.command = raw_input("")
				if self.command.strip() == "return":
					print "Returned; enter commands\n" 
				continue
			
			elif self.command.split()[0].strip() == '-new':
				if self.command.split()[1].strip() == 'subjects':
					self.subject_list = sorted([int(i) for i in self.edit.new([])])
				elif self.command.split()[1].strip() == 'gates':
					self.gate_list = sorted([int(i) for i in self.edit.new([])])
				elif self.command.split()[1].strip() == 'segment':
					self.segment = (self.edit.new([]))[0]
				elif self.command.split()[1].strip() == 'type':
					self.type = (self.edit.new([]))[0]
				
			elif self.command.split()[0].strip() == '-add':
				if self.command.split()[1].strip() == 'subjects':
					self.subject_list = sorted([int(i) for i in self.edit.add(self.subject_list)])
				elif self.command.split()[1].strip() == 'gates':
					self.gate_list = sorted([int(i) for i in self.edit.add(self.gate_list)])
			
			elif self.command.split()[0].strip() == '-rm':
				if self.command.split()[1].strip() == 'subjects':
					self.subject_list = self.edit.rm(self.subject_list)
					print self.subject_list
				elif self.command.split()[1].strip() == 'gates':
					print self.gate_list
					self.gate_list = self.edit.rm(self.gate_list)
			
			print "Returned to initial setup menu.  If completed, press [enter]\n"
					


Not_Main = Not_Main()
try:
	Not_Main.run()
except Exception as e:
	print e
	display_shelf.store()
