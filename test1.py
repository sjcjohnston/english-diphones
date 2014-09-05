import ttk
from Tkinter import *



class blarg:
    def __init__(self):
        self.master = Tk()
        ttk.Separator(self.master, orient=VERTICAL).grid(rowspan=27,column=1,sticky="ns")
        self.stuff()
                
    def var_states(self):
       print("male: %d,\nfemale: %d" % (self.var1.get(), self.var2.get()))

    def stuff(self):
        Label(self.master, text="Your sex:").grid(row=0, sticky=W)
        
        self.var1 = IntVar()
        Checkbutton(self.master, text="male", variable=self.var1).grid(row=1, sticky=W)
        
        self.var2 = IntVar()
        Checkbutton(self.master, text="female", variable=self.var2).grid(row=2, sticky=W)
        
        Button(self.master, text='Quit', command=self.master.quit).grid(row=3, sticky=W, pady=4)
        Button(self.master, text='Show', command=self.var_states).grid(row=4, sticky=W, pady=4)
        mainloop()

blarg = blarg()
