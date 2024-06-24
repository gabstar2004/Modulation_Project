from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
import LUT
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import PulseShaping as ps

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('FSK Tool')
        self.iconbitmap('Logo2.ico')
        self.geometry('1300x800')
        
        self.title = ctk.CTkLabel(self, text = 'Frequency Shift Keying Modulation Tool',
                                  font = ('Arial', 30))
        self.title.place(x=10,y=0)
        
root = App()
root.mainloop()