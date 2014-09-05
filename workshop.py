import math
import ttk
from Tkinter import *
from numpy import zeros



class Workbench:

	def __init__(self, confusion_dict):
		print "\nEntering Workbench\n"
		
		self.confusion_dict = confusion_dict
		self.master = Tk()
		self.master.wm_title("Workbench")
		self.master.geometry("250x625")

		ttk.Separator(self.master, orient=VERTICAL).grid(rowspan=27,column=1,sticky="ns")
		
		self.toolbox()
		self.workbench()
		


	def new(self):
		print self.var_all.get()

	def construction(self):
	
		self.containment = {"vd":0,"vless":0,"stop":0,"fric":0,"aff":0,"glide":0,"liq":0,"nas":0,"lab":0,"dent":0,"alv":0,"pal":0,"vel":0,"glot":0}
		print self.var_all.get()
		
		while True:
			#If using complete confusion matrix, set all field-values to "checked"
			if self.var_all.get() == 1:
				for feature in self.containment:
					self.containment[feature] = 1
				print self.containment
				break
			if self.var_all_v == 1:
				self.var_voiced = 1
				self.var_voiceless = 1
			if self.var_all_m == 1:
				self.var_stop = 1
				self.var_fricative = 1
				self.var_affricate = 1
				self.var_nasal = 1
				self.var_glide = 1
				self.var_liquid = 1
			if self.var_all_p == 1:
				self.var_labial = 1
				self.var_dental = 1
				self.var_alveolar = 1
				self.var_palatal = 1
				self.var_velar = 1
				self.var_glottal = 1
			
			#set dictionary values according to checked boxes
			self.containment['vd'] = 1 if self.var_voiced == 1 else 'unchecked'
			self.containment['vless'] = 1 if self.var_voiceless == 1 else 'unchecked'
			self.containment['stop'] = 1 if self.var_stop == 1 else 'unchecked'
			self.containment['fric'] = 1 if self.var_fricative == 1 else 'unchecked'
			self.containment['aff'] = 1 if self.var_affricate == 1 else 'unchecked'
			self.containment['nas'] = 1 if self.var_nasal == 1 else 'unchecked'
			self.containment['glide'] = 1 if self.var_glide == 1 else 'unchecked'
			self.containment['liq'] = 1 if self.var_liquid == 1 else 'unchecked'
			self.containment['lab'] = 1 if self.var_labial == 1 else 'unchecked'
			self.containment['dent'] = 1 if self.var_dental == 1 else 'unchecked'
			self.containment['alv'] = 1 if self.var_alveolar == 1 else 'unchecked'
			self.containment['pal'] = 1 if self.var_palatal == 1 else 'unchecked'
			self.containment['vel'] = 1 if self.var_velar == 1 else 'unchecked'
			self.containment['glot'] = 1 if self.var_glottal == 1 else 'unchecked'
			break
		
		
		self.confusion_matrix, self.ti_condition = zeros(shape=(2,2)), 'voicing' if self.radio_var == "voicing" else 'unchecked'
		self.confusion_matrix, self.ti_condition = zeros(shape=(7,6)), 'manner' if self.radio_var == "manner" else 'unchecked'
		self.confusion_matrix, self.ti_condition = zeros(shape=(7,6)), 'place' if self.radio_var == "place" else 'unchecked'
		
		for subject in self.confusion_dict:
			#print subject
			for gate in self.confusion_dict[subject]:
				#print gate, "\n"
				self.matrix = self.confusion_dict[subject][gate]
				
				for x in range(25):
					#check if the sound was selected - if so, check the ti_condition
					#print x, self.containment[self.input_voice_correspondence[x]], self.containment[self.input_manner_correspondence[x]], self.containment[self.input_place_correspondence[x]]
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
		print self.confusion_matrix
		
		
	#set up the gui
	def workbench(self):#, confusion_dict):
		#self.confusion_dict = confusion_dict
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
		#self.all_cc = 
		Checkbutton(self.master, text="ALL", variable = self.var_all).grid(row=3,column=0)
		
		self.var_all_v = IntVar()
		self.var_voiced = IntVar()
		self.var_voiceless = IntVar()
		self.all_v = Checkbutton(self.master, text="all", variable = self.var_all_v)
		self.voiced_cc = Checkbutton(self.master, text="Voiced", variable = self.var_voiced)
		self.voiceless_cc = Checkbutton(self.master, text="Voiceless", variable = self.var_voiceless)

		self.var_all_m = IntVar()
		self.var_stop = IntVar()
		self.var_fricative = IntVar()
		self.var_affricate = IntVar()
		self.var_nasal = IntVar()
		self.var_glide = IntVar()
		self.var_liquid = IntVar()
		self.all_m = Checkbutton(self.master, text="all", variable = self.var_all_m)
		self.stop_cc = Checkbutton(self.master, text="Stop", variable = self.var_stop)
		self.fricative_cc = Checkbutton(self.master, text="Fricative", variable = self.var_fricative)
		self.affricate_cc = Checkbutton(self.master, text="Affricate", variable = self.var_affricate)
		self.nasal_cc = Checkbutton(self.master, text="Nasal", variable = self.var_nasal)
		self.glide_cc = Checkbutton(self.master, text="Glide", variable = self.var_glide)
		self.liquid_cc = Checkbutton(self.master, text="Liquid", variable = self.var_liquid)

		self.var_all_p = IntVar()
		self.var_labial = IntVar()
		self.var_dental = IntVar()
		self.var_alveolar = IntVar()
		self.var_palatal = IntVar()
		self.var_velar = IntVar()
		self.var_glottal = IntVar()
		self.all_p = Checkbutton(self.master, text="all", variable = self.var_all_p)
		self.labial_cc = Checkbutton(self.master, text="Labial", variable = self.var_labial)
		self.dental_cc = Checkbutton(self.master, text="Dental", variable = self.var_dental)
		self.alveolar_cc = Checkbutton(self.master, text="Alveolar", variable = self.var_alveolar)
		self.palatal_cc = Checkbutton(self.master, text="Palatal", variable = self.var_palatal)
		self.velar_cc = Checkbutton(self.master, text="Velar", variable = self.var_velar)
		self.glottal_cc = Checkbutton(self.master, text="Glottal", variable = self.var_glottal)

		#radiobuttons - percent ti variable
		self.radio_var = StringVar()
		self._voicing_ti = ttk.Radiobutton(self.master, text="Voicing", variable = self.radio_var, value="voicing")
		self._manner_ti = ttk.Radiobutton(self.master, text="Manner", variable = self.radio_var, value="manner")
		self._place_ti = ttk.Radiobutton(self.master, text="Place", variable = self.radio_var, value="place")
		

		#Checkbutton instantiations
		#self.all_cc.grid(row=3,column=0)
		self.all_v.grid(row=6,column=0)
		self.voiced_cc.grid(row=7,column= 0)
		self.voiceless_cc.grid(row=8,column=0)
		self.all_m.grid(row=11,column=0)
		self.stop_cc.grid(row=12,column=0)
		self.fricative_cc.grid(row=13,column=0)
		self.affricate_cc.grid(row=14,column=0)
		self.nasal_cc.grid(row=15,column=0)
		self.glide_cc.grid(row=16,column=0)
		self.liquid_cc.grid(row=17,column=0)
		self.all_p.grid(row=20,column=0)
		self.labial_cc.grid(row=21,column=0)
		self.dental_cc.grid(row=22,column=0)
		self.alveolar_cc.grid(row=23,column=0)
		self.palatal_cc.grid(row=24,column=0)
		self.velar_cc.grid(row=25,column=0)
		self.glottal_cc.grid(row=26,column=0)

		self._voicing_ti.grid(row=7,column=2)
		self._manner_ti.grid(row=14,column=2)
		self._place_ti.grid(row=23,column=2)
		
		#establishes buttons and their event bindings
		self.calculate = Button(self.master, text="Calculate %TI", command = self.new).grid(row=29, column=2, sticky=N+S+E+W)
		self.reset_initial_setup = Button(self.master, text="Return to setup options", command = self.go_home).grid(row=29, column=0, sticky=N+S+E+W)
		
		#returns to the initial setup menu if the 'X' button is pressed
		self.master.protocol('WM_DELETE_WINDOW', self.exit_override)
		
		#Instantiate the window
		mainloop()
		
		
	def toolbox(self):
		#1b, 2ch, 3d,4 dh, 5f, 6F, 7g, 8h, 9j, 10k, 11l, 12m, 13n, 14ng, 15p, 16r, 17s, 18sh, 19t, 20th, 21v, 22w, 23y, 24z, 25zh, 26'total'
		self.input_voice_correspondence = {0:'vd',1:'vless',2:'vd',3:'vd',4:'vless',5:'vd',6:'vd',7:'vless',8:'vd',9:'vless',10:'vd',11:'vd',12:'vd',13:'vd',14:'vless',15:'vd',16:'vless',17:'vless',18:'vless',19:'vless',20:'vd',21:'vd',22:'vd',23:'vd',24:'vd',25:'total'}
		self.input_manner_correspondence = {0:'stop',1:'aff',2:'stop',3:'fric',4:'fric',5:'stop',6:'stop',7:'fric',8:'aff',9:'stop',10:'liq',11:'nas',12:'nas',13:'nas',14:'stop',15:'liq',16:'fric',17:'fric',18:'stop',19:'fric',20:'fric',21:'glide',22:'glide',23:'fric',24:'fric',25:'total'}
		self.input_place_correspondence = {0:'lab',1:'pal',2:'alv',3:'dent',4:'dent',5:'alv',6:'vel',7:'glot',8:'pal',9:'vel',10:'alv',11:'lab',12:'alv',13:'vel',14:'lab',15:'pal',16:'alv',17:'pal',18:'alv',19:'dent',20:'dent',21:'lab',22:'pal',23:'alv',24:'pal',25:'total'}
		
		#1b, 2ch, 3d, 4dh, 5f, 6g, 7h, 8j, 9k, 10 l, 11m,12n, 13ng, 14p, 15r, 16s, 17sh, 18t, 19th, 20v, 21w, 22y, 23z, 24zh, 25Voc, 26'total'
		self.prediction_voice_correspondence = {0:'vd',1:'vless',2:'vd',3:'vd',4:'vless',5:'vd',6:'vless',7:'vd',8:'vless',9:'vd',10:'vd',11:'vd',12:'vd',13:'vless',14:'vd',15:'vless',16:'vless',17:'vless',18:'vless',19:'vd',20:'vd',21:'vd',22:'vd',23:'vd',24:'vd',25:'total'}
		self.prediction_manner_correspondence = {0:'stop',1:'aff',2:'stop',3:'fric',4:'fric',5:'stop',6:'fric',7:'aff',8:'stop',9:'liq',10:'nas',11:'nas',12:'nas',13:'stop',14:'liq',15:'fric',16:'fric',17:'stop',18:'fric',19:'fric',20:'glide',21:'glide',22:'fric',23:'fric',24:'vowel',25:'total'}
		self.prediction_place_correspondence = {0:'lab',1:'pal',2:'alv',3:'dent',4:'dent',5:'vel',6:'glot',7:'pal',8:'vel',9:'alv',10:'lab',11:'alv',12:'vel',13:'lab',14:'pal',15:'alv',16:'pal',17:'alv',18:'dent',19:'dent',20:'lab',21:'pal',22:'alv',23:'pal',24:'vowel',25:'total'}
		
		self.input_voicing = {'vd':0,'vless':1}
		self.input_manner = {'stop':0,'fric':1,'aff':2,'nas':3,'glide':4,'liq':5,'vowel':6}
		self.input_place = {'lab':0,'dent':1,'alv':2,'pal':3,'vel':4,'glot':5,'vowel':6}
		
		self.prediction_voicing = {'vd':0,'vless':1}
		self.prediction_manner = {'stop':0,'fric':1,'aff':2,'nas':3,'glide':4,'liq':5}
		self.prediction_place = {'lab':0,'dent':1,'alv':2,'pal':3,'vel':4,'glot':5}
		
		
		self.ti_condition = ""
		
	
		
		
	def go_home(self):
		self.master.destroy()
		self.master.quit()
		
	def exit_override(self):
		self.master.destroy()
		self.master.quit()

if __name__ == '__main__':
	a = {'k':1}
	Workbench(a)
