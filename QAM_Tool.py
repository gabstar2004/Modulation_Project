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
import re

ctk.set_appearance_mode("dark")
 
root = ctk.CTk()   
root.geometry('1300x800')
root.title('QAM Tool')
root.iconbitmap('Logo2.ico')

title = ctk.CTkLabel(root, text='Quadrature Amplitude Modulation Tool', text_color="#d46a13", font = ('Arial', 30))
title.place(x=10, y = 10)

description = ctk.CTkTextbox(root, width = 610, fg_color = 'transparent')
description.insert(END, 'The constellation shown is the mapping that will be used to create the output file. Custom constellations'+
                           ' can be imported as a .xml file.')
description.configure(state='disabled')
description.place(x=5, y=45)

input_file = ''
input_file_name = ''
xml_file = ''
xml_file_name = ''
def saveInput():
    global input_file
    global input_file_name
    input_file_name = ''
    input_file = filedialog.askopenfilename(initialdir = "/", title = "Select Input File")
    for i in range(0, len(input_file)):
        if input_file[len(input_file) - i-1] == '/':
            break
        input_file_name += input_file[len(input_file) - i-1]
    input_file_name = input_file_name[::-1]
    input_file_label.configure(text='File selected: ' + input_file_name)
    
input_button = ctk.CTkButton(root, text = "Select Input File", command = saveInput
                             , fg_color="#d46a13", hover_color="#874f20", 
                             text_color="#ffffff")
input_button.place(x=10, y=110)

input_file_label = ctk.CTkLabel(root, text = 'File Selected: ' + input_file_name)
input_file_label.place(x=160, y = 110)


I, Q = LUT.Presets['QPSK'][0], LUT.Presets['QPSK'][1]
times_rotated = 0
def drawConstellation(choice, rotate = False):
    global I, Q, times_rotated
    I, Q = LUT.Presets[choice][0], LUT.Presets[choice][1]
    fig = Figure(figsize=(7,6))
    a = fig.add_subplot(111)
   # if rotate:
    #    I, Q = LUT.rotate45(list(I.values()), list(Q.values()), times_rotated)
    #    times_rotated += 1
    a.scatter(I.values(),Q.values(),color='#d46a13', s = 100)
    a.set_title(choice)
    a.set_xlabel('In Phase Component (I)')
    a.set_ylabel('Quadrature Component (Q)')
    a.grid(linestyle = '--')
    for i, txt in enumerate(I.keys()):
        a.annotate(txt, (list(I.values())[i], list(Q.values())[i]))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=700, y = 50)
    canvas.draw()



def drawCustomConstellation(choice):
    global I, Q
    I, Q = LUT.customQAM(xml_file, int(choice)-1)
    fig = Figure(figsize=(7,6))
    a = fig.add_subplot(111)
    a.scatter(I.values(),Q.values(),color='#d46a13', s = 100)
    a.set_title(xml_file_name + ' - Constellation ' + str(choice))
    a.set_xlabel('In Phase Component (I)')
    a.set_ylabel('Quadrature Component (Q)')
    a.grid(linestyle = '--')
    for i, txt in enumerate(I.keys()):
        a.annotate(txt, (list(I.values())[i], list(Q.values())[i]))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=700, y = 50)
    canvas.draw()

custom_QAM_select = ctk.CTkOptionMenu(root, fg_color="#d46a13", 
                                button_color="#874f20", button_hover_color = "#d46a13", width = 70, command = drawCustomConstellation)

def customQAMXML():
    global xml_file_name, xml_file
    xml_file = filedialog.askopenfilename(initialdir = "/", title = "Select XML File", filetypes = [('Xml Files', '.xml')])
    n = LUT.countConstels(xml_file)
    xml_file_name = xml_file[::-1].split('/')[0][4::][::-1]
    custom_QAM_select.configure(values = np.arange(1,n+1).astype(str))
    custom_QAM_select.set(value = '1')
    custom_QAM_select.place(x=200, y = 250)

custom_QAM_input = ctk.CTkButton(root, text = "Select Custom QAM Map", command = customQAMXML
                             , fg_color="#d46a13", hover_color="#874f20", 
                             text_color="#ffffff")
custom_QAM_input.place(x=10, y = 250)



error_label = ctk.CTkLabel(root, text = '')
error_label.place(x=10,y=720)    
    
def createOutput():
    global I, Q
    error_message = ''
    error_label.configure(text = error_message)
    
    alpha_regex = '^[01]+([.]\d+)?$'
    freq_regex = '^\d+([.]\d+)?$'
    
    a = alpha.get()
    
    freq = frequency.get()
    
    r_or_c = real_or_cmplx.get()
    if r_or_c == 'Real':
        r_or_c = True
    else:
        r_or_c = False
        
    L = samples_per_baud.get()
    if not L.isnumeric():
        error_message = 'Please select a valid samples/symbol value.'
    
    sign = signed.get()
    if sign == 'Signed':
        sign = True
    else:
        sign = False
        
    endian = MSBF.get()
    if endian == 'MSBF':
        endian = True
    else:
        endian = False
        
    bits = int(bits_select.get()[0:2])
    if bits == 12:
        bits = 128
        
    if input_file == '':
        error_message = 'Please select an input file.'
        
    if not re.match(alpha_regex, a):
        error_message = 'Please choose a valid RRC filter roll-off value.'
    else:
        a = float(a)
        if a <= 0 or a > 1:
            error_message = 'Please choose a valid RRC filter roll-off value.'
            
    if not re.match(freq_regex, freq):
        error_message = 'Please choose a valid carrier frequency.'
    else:
        freq = float(freq)
        
    if error_message == '':
        output_file = filedialog.asksaveasfile(initialdir = "/", title = "Save Output File")
        if output_file == None:
           error_message = 'Please select an output file location.'
           error_label.configure(text=error_message)
        else:
            error_label.configure(text='Please wait...')
            if diff_var.get() == 1:
                I, Q = LUT.differentialEncoder(I, Q)
            real, imag = ps.createWaveform(input_file, I, Q, int(L), freq, a)
            ps.saveSignal(output_file, real, imag, bits, r_or_c, endian, sign)
            print(I,Q, diff_var)
            error_label.configure(text = 'DONE!')
    else:
        error_label.configure(text = error_message)
    

constellation_label = ctk.CTkLabel(root, text="Preset Constellations", text_color = "#874f20", font = ('Arial', 15))
constellation_label.place(x=10,y=180)
       
QAM_options = ctk.CTkOptionMenu(root, values = ['QPSK', '16QAM'], command = drawConstellation, 
                                fg_color="#d46a13",  button_color="#874f20", button_hover_color = "#d46a13", width = 157)
QAM_options.place(x=10, y = 215)

diff_var = ctk.IntVar()
diff_encoding = ctk.CTkCheckBox(root, text = 'Differential Encoding', text_color = "#874f20", font = ('Arial', 15), fg_color="#d46a13", hover_color = "#874f20",
                                onvalue = 1, offvalue = 0, variable = diff_var)
diff_encoding.place(x=10, y = 300)

samples_per_baud = ctk.CTkEntry(root, placeholder_text='4')
samples_per_baud.place(x=10,y=380)
samples_per_baud_label = ctk.CTkLabel(root, text="Samples/Symbol (must be an integer)", text_color = "#874f20", font = ('Arial', 15))
samples_per_baud_label.place(x=10,y=350)

alpha = ctk.CTkEntry(root, placeholder_text='1.0')
alpha.place(x=10,y=460)
alpha_label = ctk.CTkLabel(root, text = 'RRC Filter Roll Off Factor (Float in (0, 1])', text_color = "#874f20", font = ('Arial', 15))
alpha_label.place(x=10,y=430)

frequency = ctk.CTkEntry(root, placeholder_text='0.0')
frequency.place(x=10,y=540)
freq_label = ctk.CTkLabel(root, text = 'Carrier Frequency', text_color = "#874f20", font = ('Arial', 15))
freq_label.place(x=10,y=510)

rotate45_button = ctk.CTkButton(root, text = "Rotate 45°",
                             command = lambda: drawConstellation(QAM_options.get(), True), fg_color="#d46a13", hover_color="#874f20", 
                             text_color="#ffffff")
#rotate45_button.place(x=170, y=250)

save_settings_label = ctk.CTkLabel(root, text = 'File Output Settings', text_color = "#874f20", font = ('Arial', 15))
save_settings_label.place(x=10,y=590)

bits_select = ctk.CTkOptionMenu(root, values=['16-bit','32-bit', '64-bit', '128-bit'], fg_color="#d46a13", 
                                button_color="#874f20", button_hover_color = "#d46a13", width = 90 )
bits_select.place(x=10, y=620)

real_or_cmplx = ctk.CTkSegmentedButton(root, values=['Real', 'Complex'],  selected_color= "#d46a13", selected_hover_color="#874f20" )
real_or_cmplx.place(x=110, y=620)
real_or_cmplx.set(value = 'Real')

signed = ctk.CTkSegmentedButton(root, values=['Signed', 'Unsigned'], selected_color= "#d46a13", selected_hover_color="#874f20")
signed.place(x=220, y=620)
signed.set(value = 'Signed')

MSBF = ctk.CTkSegmentedButton(root, values = [ 'LSBF', 'MSBF'], selected_color= "#d46a13", selected_hover_color="#874f20")
MSBF.place(x=347, y=620)
MSBF.set(value = 'LSBF')

save_button = ctk.CTkButton(root,  text = 'Save Output File', fg_color="#d46a13", hover_color="#874f20", text_color="#ffffff",
                            command=createOutput)
save_button.place(x=10, y=670)
root.after(1, drawConstellation, 'QPSK')
root.mainloop()

 