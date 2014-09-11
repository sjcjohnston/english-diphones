#globals.py
#sets up any global vars for use by the system.

from retreive_data import SetOutputPath

# class Globals:

def init():

	set_output_path = SetOutputPath()
	
	global project_name
	project_name = set_output_path.specify_file()
	set_output_path.root.destroy()
	
	# print project_name

