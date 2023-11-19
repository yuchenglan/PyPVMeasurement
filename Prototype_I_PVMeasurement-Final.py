# used for solar cell measurments
# coded in Lan's lab from 2019
# continued from 2020 May to 2020 Nov
# finish on Feb 13, 2021, Chinese New Year
# I-V data saved in csv
# fitting paramters saved in row
# I-V curve saved in pdf

#creat GUI using Tkinter
#import Tkinter as Tk
#from Tkinter import * #for python 2
from tkinter import * #for python 3
from tkinter import ttk #for python 3

#matplotlib graphing in tkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd # importing pandas as pd, save data in column  

# calculate FF
from scipy.interpolate import interp1d

#for saving data into csv format
import csv #save data in row, #all data in csv format, delimiter=', '

#import time
from time import sleep

# load the u3 module from LabJackPython, U3 device
import u3            

# initialize the LabJack U3 interface; assumes a single U3 is plugged in to a USB port
d = u3.U3()          # create a LabJack u3 device controller
d.configU3()         # set default configuration
d.getCalibrationData() # calibrate the labjack

root = Tk()
#root window, canvas, container
root.title("Photovoltaic Measurement Station: Data Collection and Analysis (Lan's Lab, 2019)")
root.geometry("900x742") # 200 for measuring frame, 700 for graphing frame, 200 for fitting frame, 50 for frame gaps
#root.geometry("800x400+100+100")

# three sections / columns: measuring, plotting, and fitting
# first frame: measuring
# second frame: plotting
# third frame: fitting
# background color of frames: white smoke
# title color (foreground) of frames: blue, gold, sea green

#first frame: measuring
frame_measuring = Frame(root, width = 200, height = 742, bg = "white smoke", highlightbackground = "green", highlightcolor = "green", highlightthickness = 1)
#frame_measure.grid(row = 0, column = 0)
frame_measuring.pack(side = LEFT, padx = 10, ipadx = 10, ipady = 10, expand = YES, fill = BOTH)

measuring_title = Label(frame_measuring, text = "I-V Data Measuring", fg = "blue", bg = "white smoke", font=("Helvetica", 24))
measuring_title.pack(ipady = 5, pady = 20)

measuring_point_number_indication = Label(frame_measuring, text = "Input # of Measurement Points", bg = "white smoke")
measuring_point_number_indication.pack()

measuring_point_number = Entry(frame_measuring, width = 20, bd = 3, bg = "white smoke")
measuring_point_number.pack()


#coding measurements
def measure():
    #swith to RPi and LabJack
    #Raspberry Pi 4 B + LabJack U3-HV

    #from labjack import u3

    # d.configIO( FIOAnalog = 1 )        # ask for analog inputs, configure FI1 as analog
    #AIN_REGISTER = 0
    #FI04_STATE_REGISTER = 6000
    #d.writeRegister(FIO4_STATE_REGISTER, 0) #set FIO 4 low
    #d.getAIN(AIN_REGISTER)

    #commond of LabJack
    #d.getAIN( 0 )  # read analog input channel 0 

    #d.configIO(NumberOfTimersEnabled = 2)
    #d.configTimerClock(TimerClockBase = 6, TimerClockDivisor = 15)

    # produce data file with CSV (comma-separated values) format 
    data_file = open('PV_data.csv','w')

    #DSSC is connected to a variable resistor made from MOSFET
    # MOSFET works as a loading whose resistor varies
    # V is measured from the MOSFET, from AIN0 of LabJack U3-HV
    # A resistor (1 Ohm) is contacted to the MOSFET in series.
    # The current is measured from the resistor I = V / R
    # Current is measured from AIN1 of LabJack U3-HV

    #Set DAC0 of LabJack to change resistance of R_DS of MOSFET: 0 --> infinity when V_DAC0 = 4V down to 0V
    #S-terminal (Pin 3) of MOSFET is connected to ADC 1 of LabJack
    #D-terminal (Pin 2) of MOSFET is connected to ADC 2 of LabJack
    #G-terminal (Pin 1) of MOSFET is connected to DAC0 of LabJack
    #set maxium DAC0 of LabJack as 5 V
    DAC0_REGISTER = 5000
    #set AIN0 of LabJack as 0V
    AIN0_REGISTER = 0
    #set AIN1 of LabJack as 0V
    AIN1_REGISTER = 0
    #set AIN2 of LabJack as 0V
    AIN2_REGISTER = 0

    for G in np.arange(0, 5.0, 0.01): #set voltage of DAC0 of LabJack / G-termidal of MOSFET, start, stop, and step of voltage
        d.writeRegister(DAC0_REGISTER, G) # Set voltage of DAC0 to G-terminal 0-5 V; Resistance of MOSFET changes from 0V to ? V   
        print(G) #print(DAC0_REGISTER)
        #read V of MOSFET,
     
        # wait 0.1 s for stablity
        sleep(0.1) #sleep for 0.1 second
    
        d.readRegister(AIN0_REGISTER)     # Read from AIN0
        V_AIN0 = d.getAIN(0)
        print("Voltage of AIN0: %s\n" % V_AIN0)  # read analog input channel 0 and print the result
        d.readRegister(AIN1_REGISTER)     # Read from AIN1
        V_AIN1 = d.getAIN(1)
        print("Voltage of AIN1: %s\n" % V_AIN1)  # read analog input channel 1 and print the result
        d.readRegister(AIN2_REGISTER)     # Read from AIN1
        V_AIN2 = d.getAIN(2)
        print("Voltage of AIN2: %s\n" % V_AIN2)  # read analog input channel 1 and print the result
        # produce CSV format data in Data-file
        data_file.write(str(G) + "," + str(V_AIN1 - V_AIN0) + "," + str((V_AIN2 - V_AIN1) / 20)  + "\n")
        #1st column: Gate voltage
        #2nd column: voltage of MOSFET (loading) / voltage of output
        #3rd column: voltage of series resistor / current of output
        data_file.flush()                           #Make sure everything is written to disk
 
    data_file.close()
 
    #reset DAC0 output as 0
    d.writeRegister(DAC0_REGISTER, 0)
    #end of measure

text1b = ttk.Button(frame_measuring, text = "Measure I-V",  command = measure)
#text1b.grid(row = 3, column = 0)
text1b.pack()

#text1c = ttk.Button(frame_measuring, text = "I-V Data List", bg = "beige")
#text1c.grid(row = 4, column = 0)
#text1c.pack()

#data = Entry(frame_measuring, bg = "beige")
#data.grid(row = 6, column = 0)
#data.pack()

# save data in column, using Pandas, complex to use csv.writer, to save in column
def IV_data_save():
    # list of curret I, voltage V 
    V_gate, V_value, I_value = PV_data.csv # x-axis, y-axis in plotting
    # dictionary of I, V lists  
    IV_dict = {'Voltage': V_value, 'Current': I_value} 
    # data frame of I-V dictionary in Pandas
    IV_df = pd.DataFrame(IV_dict) 
    # saving the dataframe to csv in columns
    IV_df.to_csv('IV_data.csv', header=False, index=False)

# download I-V data in csv column.  First column: x (voltage V in mV); second column: y (current I in mA)
measuring_IV_data_download = ttk.Button(frame_measuring, text = "Download I-V Data in csv", command = IV_data_save)
measuring_IV_data_download.pack(pady = 10, side = BOTTOM)


#second frame: graphing
frame_graphing = Frame(root, width = 700, height = 742, highlightbackground = "green", highlightcolor = "green", highlightthickness = 1, bd = 0, bg = 'white smoke')
#frame_graph.grid(row = 0, column = 1)
#frame_graph.place(x = 400, y = 100, height=200, width=400)
frame_graphing.pack(side = LEFT, padx = 10, ipady = 10, expand = YES, fill = BOTH)

graphing_title = Label(frame_graphing, text = "I-V Data Graphing", fg = "gold", bg = "white smoke", font=("Helvetica", 24))
graphing_title.pack(ipady = 5, pady = 20)

#creating the graph
def plotting(): 
    f = Figure(figsize=(3,1.852), dpi=100) # set figure size on canvas 
    a = f.add_subplot(111) # add figure plot on canvas 
    V_gate, x, y = np.loadtxt('PV_data.csv', delimiter=',', unpack=True) # read data
    a.set_title('I-V Curve')
    a.set_xlabel('Voltage (V)')
    a.set_ylabel('I (A/cm$_2$)') #solar cell are: 10 mm X 10 mm
    a.scatter(x,y) # R = 10K Ohm; I = V /R; A --> mA
    #   embedding matplotlib figure 'f' on a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=frame_graphing)
    canvas.get_tk_widget().pack()  # position, *.pack(side=TOP, fill=BOTH, expand=1)
    # idea for Prototype II: dynamically show plotting
    # using textvarible + StringVar+ *.set
    # ???

graphing_button = ttk.Button(frame_graphing, text = "Plot I-V Curve", command = plotting)
graphing_button.pack()


def graph_save():
    f = Figure(figsize=(3,1.854), dpi=100)
    a = f.add_subplot(111)
    x = np.arange(0, 5, 0.1)
    x, y = np.loadtxt('PV_data.csv', delimiter=', ', unpack=True) # read I-V data
    a.plot(x,y) #show I-V data
    a.set_title('I-V Curve') # set title of figure
    a.set_xlabel('V (V)')
    a.set_ylabel('I (A/cm$^2$)')
    canvas = FigureCanvasTkAgg(f, master=frame_graphing)
    canvas.get_tk_widget().pack() # position, *.pack(side=TOP, fill=BOTH, expand=1)
#    canvas._tkcanvas.pack()
    f.savefig('I-V_Curve') #save I-V curve image

graphing_download = ttk.Button(frame_graphing, text = "Download I-V curve in PDF", command = graph_save)
graphing_download.pack(pady = 10, side = BOTTOM)


#third frame: fitting
frame_fitting = Frame(root, width = 200, height = 742, highlightbackground = "green", highlightcolor = "green", highlightthickness = 1, bd = 0)
frame_fitting.configure(bg = 'white smoke')
#frame_fit.grid(row = 0, column = 2)
#frame_fit.place(x = 800, y = 100, height=200, width=400)
frame_fitting.pack(side = LEFT, padx = 10, ipady = 10, expand = YES, fill = BOTH)

fitting_title = Label(frame_fitting, text = "I-V Curve Fitting", fg = "sea green", bg = "white smoke", font=("Helvetica", 24))
fitting_title.pack(ipady = 5, pady = 20)

def fitting(): # find Isc, Voc, Pmax, calculate FF, ...
    # obtain Isc, Voc, FF, Pmax, and efficient from I-V curve
    #idea: compare I*V: if I*V is maxium, then -> Pmax
    V_gate, x, y = np.loadtxt('PV_data.csv', delimiter=',', unpack=True) # read I-V data, x: voltage; y: current
    isc = np.max(y)  # in A, find max current (y), find max I from data array, I is y-axis
    #idea: find max V from data array, V is x-axis
    voc = np.max(x)
    # idea 2: for Prototype II
    # use Interpolate to find Isc and Voc
    # isc = ?
    # voc = ?
    #idea: find max Pmax
    pmax = np.max(x * y) # find maxium I*V element from array
    # calculate filling factor
    f_slinear  = interp1d(x, y, kind = 'slinear')
    x_new1 = np.linspace(np.min(x), np.max(x), 200) # start from min x to max x, total 200 steps
    y_new1 = f_slinear(x_new1) # use interpolation function to calculate y-value
    area_fitting1 = np.trapz(y_new1, x_new1) # area from the first data, maybe not 0, to last data
    FF = area_fitting1/(isc * voc)
    #?
    #list current
    isc_current = Label(frame_fitting, text = "Isc = " + str("%.4G"%(isc)) + " A", bg = 'white smoke') # "%.4G"%: 4 significant figures
    isc_current.pack()
    #list voltage
    voc_voltage = Label(frame_fitting, text = "Voc = " + str("%.4G"%(voc)) + " V", bg = 'white smoke') # "%.4G"%: 4 significant figures
    voc_voltage.pack()
    #list filling factor
    ff_fillingfactor = Label(frame_fitting, text = "FF = " + str("%.4G"%(FF)), bg = 'white smoke')
    ff_fillingfactor.pack()
    #list max power
    pmax_power = Label(frame_fitting, text = "Pmax = " + str("%.4G"%(pmax)) + " W/cm2", bg = 'white smoke') # "%.4G"%: 4 significant figures
    pmax_power.pack()
    #list series resistance
    rs_resistance = Label(frame_fitting, text = "Rs = n/a", bg = 'white smoke')
    rs_resistance.pack()
    #list resistance
    ri_resistance = Label(frame_fitting, text = "Ri = n/a", bg = 'white smoke')
    ri_resistance.pack()
    #list efficient
    efficient = Label(frame_fitting, text = "Efficient = n/a", bg = 'white smoke')
    efficient.pack()

fitting_button = ttk.Button(frame_fitting, text = "Fit", command = fitting)
fitting_button.pack()
    
def fitting_parameters():
    # obtain Isc, Voc, FF, Pmax, and efficient from I-V curve
    #idea: compare I*V: if I*V is maxium, then -> Pmax
    x, y = np.loadtxt('IV_data.csv', delimiter=', ', unpack=True) # read I-V data
    pmax = np.max(x*y) # find maxium I*V element from array
    #idea: find max I from data array, I is y-axis
    isc = np.max(y)/10000*1000 # I = V/R, R = 10K Ohm, A--> mA
    #idea: find max V from data array, V is x-axis
    voc = np.max(x) # in V
    # idea 2: for Prototype II
    # use Interpolate to find Isc and Voc
    # isc = ?
    # voc = ?
    # calculate filling factor
    f_slinear  = interp1d(x, y, kind = 'slinear')
    x_new1 = np.linspace(np.min(x), np.max(x), 200) # start from min x to max x, total 200 steps
    y_new1 = f_slinear(x_new1) # use interpolation function to calculate y-value
    area_fitting1 = np.trapz(y_new1, x_new1) # area from the first data, maybe not 0, to last data
    FF = area_fitting1/(isc * voc)
    # list parameters
    solar_cell_parameter = ['Parameters', 'Isc (A)', 'Voc (V)', 'FF', 'Pmax', 'efficient', 'Ri', 'Rs']
    parameter_value = ['Values', "%.4G"%(isc), "%.4G"%(voc), "%.4G"%(FF), "%.4G"%(pmax), 'none', 'none', 'none'] #"%.4G"%: 4 significant figures
    #save into file, in row
    with open('fitting_parameter.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(solar_cell_parameter)
        csv_writer.writerow(parameter_value)
 
fitting_download = ttk.Button(frame_fitting, text = "Download Fitting Parameters in csv", command = fitting_parameters)
fitting_download.pack(pady = 10, side = BOTTOM)


#radiobutton = Radiobutton(root, text = "off")
#radiobutton.pack()
#radiobutton.grid(row = 1, column = 1)

#text = Entry(root, text = "This is a FIRST test")
#text.grid(row=4, column = 2)


root.mainloop()




"""
How to calculate FF of solar cell: area / Isc*Voc

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


# calculate the area below I-V curve
# idea: using numpy and loop, calculate each area of a (dx, ave_y) reactangle
# where dx is the width between two adjacent data, ave_y is the average height of two adjacent data
# then add total reactangle area together  
x, y = np.loadtxt('IVExperimentalData.csv', delimiter=', ', unpack=True) # read I-V data
area_loop1 = 0
for i in range(len(x)-1):
    dx = x[i+1] - x[i] # width of two adjacent data 
    ave_y = (y[i+1] + y[i])/2 # average height of two adjacent data
    area_loop1 = area_loop1 + ave_y * dx # area of a reactangle, then sum
print("Integral area-reatangle:", area_loop1)


# using array / loop and np.sum
# new array of x gap
x_gap = [x[i+1] - x[i] for i in range(len(x)-1)]
# new array of adjacent y-value, average value of two adjacent y-value
y_ave = [(y[i+1] + y[i])/2 for i in range(len(x)-1)]
# array of indivual data area: average y (height) * x gap (width)
#area_rectangle = np.multiply(x_gap, y_ave)
# add all rectangle array
#area = np.sum(area_rectangle) 
area_loop2 = np.sum(np.multiply(x_gap, y_ave))
print(area_loop2)


# calculate the area below I-V curve
# idea: using Trapezoidal rule in scipy
area_trapz = np.trapz(y, x) # x, y are arrays
# syntax: numpy.trapz(y, x=None, dx=1.0, axis=-1)
print(area_trapz)

# calculate the area below I-V curve
# idea: using Interpolate and trapz in scipy, in case the data step is not uniform
# used for Prototype I
f_slinear  = interp1d(x, y, kind = 'slinear')
x_new1 = np.linspace(np.min(x), np.max(x), 200) # start from min x to max x, total 200 steps
y_new1 = f_slinear(x_new1) # use interpolation function to calculate y-value
# syntax: numpy.trapz(y, x=None, dx=1.0, axis=-1)
area_fitting1 = np.trapz(y_new1, x_new1) # area from the first data, maybe not 0, to last data 
# calculate area using Interpolate and trapz method in scipy, 200 uniform steps in whole range
# idea: calculate area from V = 0 to voc
# used for Prototype II, 2% improved than that of first data to last data
#x_new2 = np.linspace(0, np.max(x), 200) # start from 0 to max x, total 200 steps
#y_new2 = f_slinear(x_new2)
# syntax: numpy.trapz(y, x=None, dx=1.0, axis=-1)
#area_fitting2 = np.trapz(y_new2, x_new2) # area from 0 to the last data 
print(area_fitting1)

plt.scatter(x,y)
plt.plot(x_new1,y_new1)

plt.show()
"""

