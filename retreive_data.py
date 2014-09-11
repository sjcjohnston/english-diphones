from xlrd import open_workbook
from Tkinter import *
from tkFileDialog import *
from collections import defaultdict
from numpy import zeros


class ExcelReader:

	def __init__(self):
		self.root = Tk()
		self.root.withdraw()
		#requests the location of the excel file
		print "Please identify the location of the confusion matrix excel file."
				
		self.filename = askopenfilename()
		
		print "Collecting specified matrices from excel database...\n"
		
		self.wkbk = open_workbook(self.filename)
		
		
	def identify_sheet(self, segment, type):
		#creates a sheet object based on the initial setup values: segment & type
		self.sheet_name = "Seg{0}{1}s".format(segment,type)
		
		wkst = self.wkbk.sheet_by_name(self.sheet_name)

		return wkst
		

	def extract_values(self, target_sheet, subject_list, gate_list):
		#using the identified worksheet object, and the initial setup values: subject_list & gate_list - creates a dictionary of the confusion matrix values
		self.confusion_dict = defaultdict(lambda : defaultdict(dict))
		
		self.cell_contents = ""
		self.row_count = 5
		self.col_count = 3
		
		while True:		#counts the number of rows in the matrix
			self.row_count += 1
			self.cell_contents = target_sheet.cell(self.row_count, 3)
			if 'empty' in str(self.cell_contents):
				break
			
		while True: 	#counts the number of columns in the matrix
			self.col_count += 1
			self.cell_contents = target_sheet.cell(5, self.col_count)
			if 'empty' in str(self.cell_contents):
				break
			
		self.row_len = self.row_count - 5
		self.col_len = self.col_count - 3
		
		self.subject_row = 6
				
		#Moves through the open worksheet, populating the matrices for each subject/gate pair
		for self.subject in subject_list:
			self.subject_row = self.get_row_index(self.subject, self.subject_row, target_sheet, 0)
			self.gate_row = self.subject_row
			for self.gate in gate_list:
				self.gate_row = self.get_row_index(self.gate, self.gate_row, target_sheet, 1)
				self.confusion_dict[self.subject][self.gate] = self.populate_matrix(target_sheet)
	
		return self.confusion_dict
				

	def get_row_index(self, item_number, item_row, target_sheet, col):
		while True:
			self.cell_contents = target_sheet.cell(item_row, col)

			if str(self.cell_contents)[7:-1] != '':
				if int(float(str(self.cell_contents)[7:-1])) == int(item_number):
					return item_row
			item_row += 1
		
		
	def populate_matrix(self, target_sheet):
		confusion_matrix = zeros(shape=(self.row_len,self.col_len))

		for i in range(self.row_len):
			for j in range(self.col_len):
				# the string indices (7:-1) are to extract the cell contents from the cell object, once parsed into a string.
				if str(target_sheet.cell(i+6, j+4))[7:-1] == '':
					confusion_matrix[i,j] = 0
				else:
					confusion_matrix[i,j] = int(float(str(target_sheet.cell(i+6, j+4))[7:-1]))

		return confusion_matrix
	
		
class SetOutputPath:
	
	def __init__(self):
		print "Please identify the location and name you would like to use for the output file."

	def specify_file(self):
		self.root = Tk()
		self.project_name = asksaveasfilename(filetypes=[('Text File','.txt')])
		
		return self.project_name