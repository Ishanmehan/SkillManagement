import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from ReadInput import ReadInput
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.path = ""
        self.master = master
        self.e1 = ""
        self.e2 = ""
        self.e3 = ""
        self.create_widgets()


    def browsefunc(self):
        self.ent1.insert(tk.END,"")

        self.master.sourceFile = filedialog.askopenfilename(parent=self.master, initialdir="/",
                                                            title="Please select a directory")
        self.ent1.insert(tk.END, self.master.sourceFile)  # add this
        self.path = self.ent1.get()
        self.ReadInput_obj = ReadInput(self.path)
        print(self.path)

    def create_widgets(self):
        tk.Label(self.master, text="SKILL MANAGEMENT TOOL").grid(row=1, column=1)
        tk.Label(self.master, text="Path").grid(row=2, column=1)
        tk.Label(self.master, text="Employee ID").grid(row=4, column=1)
        tk.Label(self.master, text="Area to check(eg Primarly skill, skill)").grid(row=6, column=1)
        tk.Label(self.master, text="Enter Future skills(enter with , )").grid(row=9, column=1)

        self.ent1 = tk.Entry(self.master, font=25)
        self.ent1.grid(row=2, column=3)
        b1 = tk.Button(self.master, text="FIND", font=40, command=self.browsefunc).grid(row=2, column=6)
        self.e1 = tk.Entry(self.master, font=40)
        self.e1.grid(row=4, column=3)
        self.e2 = tk.Entry(self.master, font=40)
        self.e2.grid(row=6, column=3)
        self.e3 = tk.Entry(self.master, font=40)
        self.e3.grid(row=9, column=3)

        self.usecase1 = tk.Button(self.master, text="usecase1")
        self.usecase2 = tk.Button(self.master, text="usecase2")
        self.usecase3 = tk.Button(self.master, text="usecase3")
        self.usecase4 = tk.Button(self.master, text="usecase4")

        self.usecase1.grid(row=10, column=1)
        self.usecase2.grid(row=10, column=2)
        self.usecase3.grid(row=12, column=1)
        self.usecase4.grid(row=12, column=2)

        self.usecase1["command"] = self.usecase1func
        self.usecase2["command"] = self.usecase2func
        self.usecase3["command"] = self.usecase3func
        self.usecase4["command"] = self.usecase4func

    def usecase1func(self):
        time1 = time.time()
        self.ReadInput_obj.updatenearnessmatrix([2,6], "usecase1")
        time2 = time.time()
        print(time2-time1)

    def usecase2func(self):
        time1 = time.time()
        self.ReadInput_obj.updatenearnessmatrix([6,1], "usecase2")
        time2 = time.time()
        print(time2 - time1)

    def usecase3func(self):
        time1 = time.time()
        self.ReadInput_obj.updatenearnessmatrix3var([0, 6, 2],"usecase3")
        time2 = time.time()
        print(time2 - time1)

    def usecase4func(self):
        x = self.ReadInput_obj.check_employee_skill_nearness(self.e1.get(), self.e3.get(), self.e2.get())
        if(len(x)==2):
            nearness = Entry(self.master, font=40)
            nearness.grid(row=12, column=3)
            nearness.insert(0, "Nearness Value :"+str(x[0]))
            nearness1 = Entry(self.master, font=20)
            nearness1.grid(row=13, column=1,columnspan=4, sticky=W+E)
            nearness1.insert(0, str(x[1]))
        else:
            nearness1 = Entry(self.master, font=20)
            nearness1.grid(row=13, column=1, columnspan=4, sticky=W + E)
            nearness1.insert(0, "Please check EMP ID or Area to check..value is wrong")



root = tk.Tk()
app = Application(master=root)
app.mainloop()
