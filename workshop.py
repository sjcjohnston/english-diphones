import ttk
from Tkinter import *
from numpy import zeros
from Percent_TI import Calculator



class Workbench:

	def __init__(self, confusion_dict):
		print "\nEntering Workbench\n"
		
		self.confusion_dict = confusion_dict
		self.master = Tk()
		self.master.wm_title("Workbench")
		self.master.geometry("300x450")

		ttk.Separator(self.master, orient=VERTICAL).grid(rowspan=27,column=1,sticky="ns")
		
		self.calculated_information = []

		self.toolbox()
		
		self.workbench()
		

	def construction(self):
	
		self.containment = {"vd":0,"vless":0,"stop":0,"fric":0,"aff":0,"glide":0,"liq":0,"nas":0,"lab":0,"dent":0,"alv":0,"pal":0,"vel":0,"glot":0}

		#If using complete confusion matrix, set all field-values to "checked"
		if self.var_all.get() == 1:
			for feature in self.containment:
				self.containment[feature] = 1

		else:
			#set dictionary values according to checked boxes
			self.containment['vd'] = 1 if self.var_voiced.get() == 1 else 'unchecked'
			self.containment['vless'] = 1 if self.var_voiceless.get() == 1 else 'unchecked'
			self.containment['stop'] = 1 if self.var_stop.get() == 1 else 'unchecked'
			self.containment['fric'] = 1 if self.var_fricative.get() == 1 else 'unchecked'
			self.containment['aff'] = 1 if self.var_affricate.get() == 1 else 'unchecked'
			self.containment['nas'] = 1 if self.var_nasal.get() == 1 else 'unchecked'
			self.containment['glide'] = 1 if self.var_glide.get() == 1 else 'unchecked'
			self.containment['liq'] = 1 if self.var_liquid.get() == 1 else 'unchecked'
			self.containment['lab'] = 1 if self.var_labial.get() == 1 else 'unchecked'
			self.containment['dent'] = 1 if self.var_dental.get() == 1 else 'unchecked'
			self.containment['alv'] = 1 if self.var_alveolar.get() == 1 else 'unchecked'
			self.containment['pal'] = 1 if self.var_palatal.get() == 1 else 'unchecked'
			self.containment['vel'] = 1 if self.var_velar.get() == 1 else 'unchecked'
			self.containment['glot'] = 1 if self.var_glottal.get() == 1 else 'unchecked'

		if self.radio_var.get() == "voicing":
			self.confusion_matrix, self.ti_condition = zeros(shape=(3,3)), 'voicing' 
		elif self.radio_var.get() == "manner":
			self.confusion_matrix, self.ti_condition = zeros(shape=(7,8)), 'manner' 
		elif self.radio_var.get() == "place":
			self.confusion_matrix, self.ti_condition = zeros(shape=(7,8)), 'place'
		
		for subject in self.confusion_dict:
			for gate in self.confusion_dict[subject]:
				self.matrix = self.confusion_dict[subject][gate]
				
				for x in range(25):
					#check if the sound was selected - if so, check the ti_condition
					if self.containment[self.input_voice_correspondence[x]] == 1 and self.containment[self.input_manner_correspondence[x]] == 1 and self.containment[self.input_place_correspondence[x]] == 1:
						for y in range(25):
							#extract value from the input confusion matrix
							val = self.matrix[x,y]
							if self.ti_condition == 'voicing':
								self.confusion_matrix[self.input_voicing[self.input_voice_correspondence[x]],self.prediction_voicing[self.prediction_voice_correspondence[y]]] += val
							if self.ti_condition == 'manner':
								self.confusion_matrix[self.input_manner[self.input_manner_correspondence[x]],self.prediction_manner[self.prediction_manner_correspondence[y]]] += val
							if self.ti_condition == 'place':
								self.confusion_matrix[self.input_place[self.input_place_correspondence[x]],self.prediction_place[self.prediction_place_correspondence[y]]] += val
					else:
						continue
				#sum row/col totals
				num_of_cols = len(self.confusion_matrix[1])
				for i in range(num_of_cols):
					col_total = 0
					for j in range(len(self.confusion_matrix)):
						if i == 0:
							self.confusion_matrix[j,num_of_cols-1] = sum(self.confusion_matrix[j])
						col_total += self.confusion_matrix[j,i]
					self.confusion_matrix[j,i] = col_total

		self.calculate = Calculator(self.confusion_matrix)
		self.calculate.percent_ti()

		self.selected_categories = []
		
		#create the list of constraint features (e.g., if only "palatal" were checked, only "palatal" would be in this list)
		print [i for i,j in self.containment.items() if j=='unchecked']
		for k in [i for i,j in self.containment.items() if j=='unchecked']:
			if k in self.voice_list:
				self.selected_categories += self.voice_list
				for i in [i for i,j in self.containment.items() if j=='unchecked' and i in self.voice_list]:
					self.selected_categories .remove(i)
				break
			if k in self.manner_list:
				self.selected_categories += self.manner_list
				for i in [i for i,j in self.containment.items() if j=='unchecked' and i in self.manner_list]:
					self.selected_categories.remove(i)
				break
			if k in self.place_list:
				self.selected_categories = self.place_list
				for i in [i for i,j in self.containment.items() if j=='unchecked' and i in self.place_list]:
					self.selected_categories.remove(i)
				break
		if self.selected_categories == []:
			self.selected_categories = ["No Constraints"]

		self.packaged_info = (self.selected_categories, self.radio_var.get() , self.calculate.final_values)

		self.calculated_information.append(self.packaged_info)

		
	#set up the gui
	def workbench(self):
		#Primary labels
		#containment_category = Label(master, text="Containment Category").grid(row=0, column=0)
		Label(self.master, text="Containment Category").grid(row=0, column=0)
		#percent_ti_var = Label(master, text="Calculate %TI for...").grid(row=0, column=2)
		Label(self.master, text="Calculate %TI for...").grid(row=0, column=2)

		#secondary labels - containment category
		Label(self.master, text="Voicing").grid(row=5,column=0)
		Label(self.master, text="Manners").grid(row=10,column=0)
		Label(self.master, text="Places").grid(row=19,column=0)

		#secondary labels - percent ti variables
		Label(self.master, text="Voicing").grid(row=5,column=2)
		Label(self.master, text="Manners").grid(row=10,column=2)
		Label(self.master, text="Places").grid(row=19,column=2)

		#checkbuttons - containment category 
		self.var_all =  IntVar()
		self.all = Checkbutton(self.master, text="ALL", variable = self.var_all, command=self.deactivate_all).grid(row=3,column=0)
		
		# self.var_all_v = IntVar()
		self.var_voiced = IntVar()
		self.var_voiceless = IntVar()
		# Checkbutton(self.master, text="all", variable = self.var_all_v).grid(row=6,column=0)
		self.voiced = Checkbutton(self.master, text="Voiced", variable = self.var_voiced, command=self.selectall_nonvoice)
		self.voiced.grid(row=7,column= 0)
		self.voiceless = Checkbutton(self.master, text="Voiceless", variable = self.var_voiceless, command=self.selectall_nonvoice)
		self.voiceless.grid(row=8,column=0)

		# self.var_all_m = IntVar()
		self.var_stop = IntVar()
		self.var_fricative = IntVar()
		self.var_affricate = IntVar()
		self.var_nasal = IntVar()
		self.var_glide = IntVar()
		self.var_liquid = IntVar()
		# Checkbutton(self.master, text="all", variable = self.var_all_m).grid(row=11,column=0)
		self.stop = Checkbutton(self.master, text="Stop", variable = self.var_stop, command=self.selectall_nonmanner)
		self.stop.grid(row=12,column=0)
		self.fricative = Checkbutton(self.master, text="Fricative", variable = self.var_fricative, command=self.selectall_nonmanner)
		self.fricative.grid(row=13,column=0)
		self.affricate = Checkbutton(self.master, text="Affricate", variable = self.var_affricate, command=self.selectall_nonmanner)
		self.affricate.grid(row=14,column=0)
		self.nasal = Checkbutton(self.master, text="Nasal", variable = self.var_nasal, command=self.selectall_nonmanner)
		self.nasal.grid(row=15,column=0)
		self.glide = Checkbutton(self.master, text="Glide", variable = self.var_glide, command=self.selectall_nonmanner)
		self.glide.grid(row=16,column=0)
		self.liquid = Checkbutton(self.master, text="Liquid", variable = self.var_liquid, command=self.selectall_nonmanner)
		self.liquid.grid(row=17,column=0)

		# self.var_all_p = IntVar()
		self.var_labial = IntVar()
		self.var_dental = IntVar()
		self.var_alveolar = IntVar()
		self.var_palatal = IntVar()
		self.var_velar = IntVar()
		self.var_glottal = IntVar()
		# Checkbutton(self.master, text="all", variable = self.var_all_p).grid(row=20,column=0)
		self.labial = Checkbutton(self.master, text="Labial", variable = self.var_labial, command=self.selectall_nonplace)
		self.labial.grid(row=21,column=0)
		self.dental = Checkbutton(self.master, text="Dental", variable = self.var_dental, command=self.selectall_nonplace)
		self.dental.grid(row=22,column=0)
		self.alveolar = Checkbutton(self.master, text="Alveolar", variable = self.var_alveolar, command=self.selectall_nonplace)
		self.alveolar.grid(row=23,column=0)
		self.palatal = Checkbutton(self.master, text="Palatal", variable = self.var_palatal, command=self.selectall_nonplace)
		self.palatal.grid(row=24,column=0)
		self.velar = Checkbutton(self.master, text="Velar", variable = self.var_velar, command=self.selectall_nonplace)
		self.velar.grid(row=25,column=0)
		self.glottal = Checkbutton(self.master, text="Glottal", variable = self.var_glottal, command=self.selectall_nonplace)
		self.glottal.grid(row=26,column=0)

		#checkbutton lists
		self.voice_set = set([self.voiced,self.voiceless])
		self.manner_set = set([self.stop,self.fricative,self.affricate,self.nasal,self.glide,self.liquid])
		self.place_set = set([self.labial,self.dental,self.alveolar,self.palatal,self.velar,self.glottal])

		#radiobuttons - percent ti variable
		self.radio_var = StringVar(value="voicing")
		ttk.Radiobutton(self.master, text="Voicing", variable = self.radio_var, value="voicing").grid(row=7,column=2)
		ttk.Radiobutton(self.master, text="Manner", variable = self.radio_var, value="manner").grid(row=14,column=2)
		ttk.Radiobutton(self.master, text="Place", variable = self.radio_var, value="place").grid(row=23,column=2)

		#establishes buttons and their event bindings
		self.calculate = Button(self.master, text="Calculate %TI", command = self.construction).grid(row=29, column=2, sticky=N+S+E+W)
		self.reset_initial_setup = Button(self.master, text="Return to setup options", command = self.go_home).grid(row=29, column=0, sticky=N+S+E+W)
		
		#returns to the initial setup menu if the 'X' button is pressed
		self.master.protocol('WM_DELETE_WINDOW', self.go_home)
		
		#Instantiate the window
		mainloop()
		
		
	def toolbox(self):
		#1b, 2ch, 3d,4 dh, 5f, 6F, 7g, 8h, 9j, 10k, 11l, 12m, 13n, 14ng, 15p, 16r, 17s, 18sh, 19t, 20th, 21v, 22w, 23y, 24z, 25zh, 26'total'
		self.input_voice_correspondence = {0:'vd',1:'vless',2:'vd',3:'vd',4:'vless',5:'vd',6:'vd',7:'vless',8:'vd',9:'vless',10:'vd',11:'vd',12:'vd',13:'vd',14:'vless',15:'vd',16:'vless',17:'vless',18:'vless',19:'vless',20:'vd',21:'vd',22:'vd',23:'vd',24:'vd',25:'total'}
		self.input_manner_correspondence = {0:'stop',1:'aff',2:'stop',3:'fric',4:'fric',5:'stop',6:'stop',7:'fric',8:'aff',9:'stop',10:'liq',11:'nas',12:'nas',13:'nas',14:'stop',15:'liq',16:'fric',17:'fric',18:'stop',19:'fric',20:'fric',21:'glide',22:'glide',23:'fric',24:'fric',25:'total'}
		self.input_place_correspondence = {0:'lab',1:'pal',2:'alv',3:'dent',4:'lab',5:'alv',6:'vel',7:'glot',8:'pal',9:'vel',10:'alv',11:'lab',12:'alv',13:'vel',14:'lab',15:'pal',16:'alv',17:'pal',18:'alv',19:'dent',20:'lab',21:'lab',22:'pal',23:'alv',24:'pal',25:'total'}
		
		#1b, 2ch, 3d, 4dh, 5f, 6g, 7h, 8j, 9k, 10 l, 11m,12n, 13ng, 14p, 15r, 16s, 17sh, 18t, 19th, 20v, 21w, 22y, 23z, 24zh, 25Voc, 26'total'
		self.prediction_voice_correspondence = {0:'vd',1:'vless',2:'vd',3:'vd',4:'vless',5:'vd',6:'vless',7:'vd',8:'vless',9:'vd',10:'vd',11:'vd',12:'vd',13:'vless',14:'vd',15:'vless',16:'vless',17:'vless',18:'vless',19:'vd',20:'vd',21:'vd',22:'vd',23:'vd',24:'vd',25:'total'}
		self.prediction_manner_correspondence = {0:'stop',1:'aff',2:'stop',3:'fric',4:'fric',5:'stop',6:'fric',7:'aff',8:'stop',9:'liq',10:'nas',11:'nas',12:'nas',13:'stop',14:'liq',15:'fric',16:'fric',17:'stop',18:'fric',19:'fric',20:'glide',21:'glide',22:'fric',23:'fric',24:'vowel',25:'total'}
		self.prediction_place_correspondence = {0:'lab',1:'pal',2:'alv',3:'dent',4:'lab',5:'vel',6:'glot',7:'pal',8:'vel',9:'alv',10:'lab',11:'alv',12:'vel',13:'lab',14:'pal',15:'alv',16:'pal',17:'alv',18:'dent',19:'lab',20:'lab',21:'pal',22:'alv',23:'pal',24:'vowel',25:'total'}
		
		self.input_voicing = {'vd':0,'vless':1}
		self.input_manner = {'stop':0,'fric':1,'aff':2,'nas':3,'glide':4,'liq':5}
		self.input_place = {'lab':0,'dent':1,'alv':2,'pal':3,'vel':4,'glot':5}
		
		self.prediction_voicing = {'vd':0,'vless':1}
		self.prediction_manner = {'stop':0,'fric':1,'aff':2,'nas':3,'glide':4,'liq':5,'vowel':6}
		self.prediction_place = {'lab':0,'dent':1,'alv':2,'pal':3,'vel':4,'glot':5,'vowel':6}

		self.voice_list = ["vd","vless"]
		self.manner_list = ["stop","fric","aff","nas","glide","liq"]
		self.place_list = ["lab","dent","alv","pal","vel","glot"]
		
		self.ti_condition = ""
		
	def selectall_nonvoice(self):
		if self.var_voiced.get() == 1 or self.var_voiceless.get() == 1:
			for feature in self.manner_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
			for feature in self.place_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
		if self.var_voiced.get() == 0 and self.var_voiceless.get() == 0:
			for feature in self.manner_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')
			for feature in self.place_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')

	def selectall_nonmanner(self):
		if self.var_stop.get() == 1 or self.var_fricative.get() == 1 or self.var_affricate.get() == 1 or self.var_nasal.get() == 1 or self.var_glide.get() == 1 or self.var_liquid.get() == 1:
			for feature in self.voice_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
			for feature in self.place_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
		if self.var_stop.get() == 0 and self.var_fricative.get() == 0 and self.var_affricate.get() == 0 and self.var_nasal.get() == 0 and self.var_glide.get() == 0 and self.var_liquid.get() == 0:
			for feature in self.voice_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')
			for feature in self.place_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')


	def selectall_nonplace(self):
		if self.var_labial.get() == 1 or self.var_dental.get() == 1 or self.var_alveolar.get() == 1 or self.var_palatal.get() == 1 or self.var_velar.get() == 1 or self.var_glottal.get() == 1:
			for feature in self.voice_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
			for feature in self.manner_set:
				feature.select()
				feature.configure(state='disable', disabledforeground='gray')
		if self.var_labial.get() == 0 and self.var_dental.get() == 0 and self.var_alveolar.get() == 0 and self.var_palatal.get() == 0 and self.var_velar.get() == 0 and self.var_glottal.get() == 0:
			for feature in self.voice_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')
			for feature in self.manner_set:
				feature.deselect()
				feature.configure(state='normal', disabledforeground='black')


	def deactivate_all(self):
		if self.var_all.get() == 1:
			for feature in self.voice_set:
				feature.configure(state='disabled', disabledforeground='gray')
			for feature in self.manner_set:
				feature.configure(state='disabled', disabledforeground='gray')
			for feature in self.place_set:
				feature.configure(state='disabled', disabledforeground='gray')
		elif self.var_all.get() == 0:
			for feature in self.voice_set:
				feature.configure(state='normal', disabledforeground='black')
			for feature in self.manner_set:
				feature.configure(state='normal', disabledforeground='black')
			for feature in self.place_set:
				feature.configure(state='normal', disabledforeground='black')


	def go_home(self):
		self.master.destroy()
		self.master.quit()

