# pyinstaller -c -F NSolver_v2.py -i "icon.ico" --noconsole 

# Broadly, this program takes a string of letters and returns the closest match to a word in a file.
# In context, this program takes an anagram of a train station name and returns the original.
version = 'v2'

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
import sys

# statics
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabetcols = [letter for letter in alphabet]

strguide = 'Spoorweg anagram hier...'

# csv file names
rawnames = 'stationnames.csv'
encodednames = 'encodednames.csv'
backupfile = 'namesbackup.csv'
doRedoFiles = True

# SOLVER BUILDING BLOCKS
# turn string into string containing only its letters (lowercase)
def Filter(STR:str) -> str:
    # capital letters
    STR = STR.lower()

    # special letters
    tempSTR = ''

    for c in STR:
        if c.isalpha():
            tempSTR = tempSTR + c
    
    return tempSTR

# counts presence of each letter in a string
def Encoder(STR:str) -> pd.Series:
    arr = np.array([], dtype=np.int8)
    
    for letter in alphabet:
        arr = np.append(arr, STR.count(letter))

    series = pd.Series(arr, index=alphabetcols)
    
    return series

# IMPORT PREGENERATED DATAFRAMES FROM FILES
if not doRedoFiles:
    DFnames = pd.read_csv(rawnames, sep=',', engine='python', dtype=object)
    DFnamesEncoded = pd.read_csv(encodednames, sep=',', engine='python', dtype=int)
    
else:
    DFnames = pd.read_csv(backupfile, sep=',', engine='python', dtype=object)
    DFnamesEncoded = pd.DataFrame(columns=alphabetcols)

    # set up static cols
    colALL = DFnames.columns.values.tolist()
    colNAME = colALL[0]
    colFILTERED = 'filterednames'

    DFnames[colFILTERED] = DFnames[colNAME].apply(Filter)
    DFnamesEncoded = DFnames[colFILTERED].apply(Encoder)

    DFnames.to_csv(rawnames, header=True, index=False, mode='w')
    DFnamesEncoded.to_csv(encodednames, header=True, index=False, mode='w')

# IN [RAWNAMES].CSV
# static columns
colALL = DFnames.columns.values.tolist()
colNAME = colALL[0]
colFILTERED = colALL[1]

# dynamic columns
colDIFF = 'distance'
colCONF = 'confidence'

colOUTPUTS = [colNAME, colCONF]

guesses = 3

# SOLVER BODY
# calculate distance between two series
class distance:
    def __init__(self, SRSencodedAnagram:pd.Series):
        self.anagram = SRSencodedAnagram
    
    def ndamplitude(vector:pd.Series) -> float:
        amp = (vector**2).sum()**0.5

        return amp

    def get(self, SRSnamesEncoded:pd.Series) -> float:

        difference = abs(SRSnamesEncoded - self.anagram)

        return distance.ndamplitude(difference)

# solves and neatly organizes the gathered results
class solver:
    def __init__(self, anagram):
        self.anagram = anagram
        self.inputAnagramEncoded = Encoder(Filter(anagram))
        self.dfnames = DFnames
        self.dfnamesencoded = DFnamesEncoded
        
    def getconfidence(DF:pd.DataFrame) -> pd.DataFrame:
        
        DF[colCONF] = round(abs(DF[colDIFF] / DF[colDIFF].max() - 1) * 100, 1)

        # print(DF)
        
        return DF
    
    def execute(self) -> list:
        success = False

        if len(self.anagram) == 0 or self.anagram == strguide:
            sortedDF = pd.DataFrame(columns=colOUTPUTS)

            for col in colOUTPUTS:
                sortedDF[col] = [None for i in range(guesses)]
                
        else:
            anagramdistance = distance(self.inputAnagramEncoded)
            self.dfnames[colDIFF] = self.dfnamesencoded.apply(anagramdistance.get, axis=1)
            
            self.dfnames = solver.getconfidence(self.dfnames)

            sortedDF = self.dfnames.sort_values(by=colDIFF, ascending=True).iloc[0:guesses]

            # print(sortedDF)

            success = True

        return success, sortedDF[colOUTPUTS]

# SRSresult = solver('Zwolle').execute()

# GUI
# rainbow colours
class Rainbow:
    def __init__(self, increments, a=1/20, b=np.pi/4):

        # mathematical constants
        self.a = a
        self.b = b
        self.cRed = 0.45
        self.cGreen = 1.8
        self.cBlue = 0.9
        self.d = 1-self.a

        # increment logic
        # x = np.arange(increments)+1

        # x = x / increments * 3 * np.pi + 2

        x = Rainbow.getSequence(increments)

        self.redChannel = self.red(x)
        self.greenChannel = self.green(x)
        self.blueChannel = self.blue(x)

        self.increments = increments
        self.x = x

    def getSequence(increments):
        # increment logic
        x = np.arange(increments)+1

        x = x / increments * 3 * np.pi + 2

        return x

    def red(self, x):
        return self.a*np.sin(self.b*x+self.cRed*np.pi)+self.d

    def green(self, x):
        return self.a*np.sin(self.b*x+self.cGreen*np.pi)+self.d

    def blue(self, x):
        return self.a*np.sin(self.b*x-self.cBlue*np.pi)+self.d

    def plot(self):
        analysislen = 100
        
        x = Rainbow.getSequence(analysislen)
        
        redC = self.red(x)
        greenC = self.green(x)
        blueC = self.blue(x)

        plt.plot(x, redC)
        plt.plot(x, greenC)
        plt.plot(x, blueC)
        
        plt.show()

    def makeRGB(red, green, blue):
        red = int(red*255)
        green = int(green*255)
        blue = int(blue*255)

        return tuple((red, green, blue))
    
    def getRGB(self):
        rgb = np.array([], dtype=np.int8)
        for xindex, xitem in enumerate(self.x):
            a = Rainbow.makeRGB(self.redChannel[xindex], self.greenChannel[xindex], self.blueChannel[xindex])
            rgb = np.append(rgb, a)
        
        rgb = rgb.reshape(self.increments, 3)
        
        return rgb
    
    def getHEX(self):
        rgbList = self.getRGB()

        hexcodes = []
        
        for rgbIndex, rgb in enumerate(rgbList):
            red = rgbList[rgbIndex][0]
            green = rgbList[rgbIndex][1]
            blue = rgbList[rgbIndex][2]

            hexcodes.append('#{:02x}{:02x}{:02x}'.format(red, green, blue))

        return hexcodes

# stylesheet
padding = 8

colorbg = "#CAE1DE"
colorlbl = "#ffffff"
colorbtnstandard = "#ffffff"
colorbtnsubmit = "#aaffaa"
colorbtnexit = "#ffaaaa"

colortxtwarn = "#ff6666"
colortxtstandard = "#000000"
colortxtfocusout = "#333333"

txtFONT = 'Helvetica 12'
txtsubmit = 'Zoeken'
txtexit = 'Sluiten'
txtname = 'Naam'
txtconfidence = 'Score'
txtfancy = 'Fancy'

strtitle = f':3 NSolver {version} :3'

increments = 50
rainbowcolors = Rainbow(increments, a=1/12).getHEX()
updatetime = 50

# placements & widgets
class MainGUI:
    def __init__(self, master):
        self.colorbg = colorbg
        
        self.master = master

        self.master.title(strtitle)

        # master variables
        increment = tk.IntVar()
        increment.set(0)
        self.increment = increment

        doFancy = tk.BooleanVar()
        doFancy.set(False)
        self.doFancy = doFancy

        # set up grid for frame
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        frame = tk.Frame(self.master)
        frame.configure(background=self.colorbg)
        self.frame = frame

        frame.grid(column=0, row=0, sticky='new')
        frame.grid_columnconfigure(2, weight=3)
        frame.grid_rowconfigure(1, weight=3)

        # window
        topframe = tk.Frame(frame)
        topframe.configure(background=self.colorbg)
        topframe.grid(column=0, row=0, columnspan=3, sticky='ew', pady=(0,padding))
        topframe.columnconfigure(0, weight=3)
        self.topframe = topframe

        outputframe = tk.Frame(frame)
        outputframe.configure(background=self.colorbg)
        outputframe.grid(column=0, row=1, sticky='ew')
        self.outputframe = outputframe

        btnframe = tk.Frame(frame)
        btnframe.configure(background=self.colorbg)
        btnframe.grid(column=1, row=1, padx=(padding,0), sticky='ns')
        self.btnframe = btnframe

        # window elements
        entry = tk.Entry(topframe, font=txtFONT)
        entry.configure(background=colorlbl)
        entry.insert(0, strguide)
        entry.bind('<Return>', self.onReturn)
        entry.bind('<FocusIn>', self.onEntryFocusIn)
        entry.bind('<FocusOut>', self.onEntryFocusOut)
        entry.config(fg = colortxtfocusout)

        blockconfidence = tk.Text(outputframe, height=guesses+4, width=8, font=txtFONT)
        blockconfidence.configure(background=colorlbl)
        blockconfidence.tag_configure('bold', font=txtFONT+' bold')
        blockconfidence.insert(tk.END, f'{txtconfidence}\n', 'bold')

        blocknames = tk.Text(outputframe, height=guesses+4, width=30, font=txtFONT)
        blocknames.configure(background=colorlbl)
        blocknames.tag_configure('bold', font=txtFONT+' bold')
        blocknames.insert(tk.END, f'{txtname}\n', 'bold')

        for i in range(guesses):
            blockconfidence.insert(tk.END, f'-%\n')
            blocknames.insert(tk.END, f'-\n')

        btnsubmit = tk.Button(btnframe, text=txtsubmit, font=txtFONT, command=self.widgetSubmit)
        btnsubmit.configure(background=colorbtnsubmit)

        btnexit = tk.Button(btnframe, text=txtexit, font=txtFONT, command=self.widgetExit)
        btnexit.configure(background=colorbtnexit)

        btnfancy = tk.Button(btnframe, text=txtfancy, font=txtFONT, command=self.widgetSwitchFancyMode)
        btnfancy.configure(background=colorbtnstandard)

        entry.grid(column=0, row=0, sticky='ew')
        self.entry = entry

        blocknames.grid(column=0, row=0, padx=(0,padding), sticky='new')
        self.blocknames = blocknames

        blockconfidence.grid(column=1, row=0, sticky='new')
        self.blockconfidence = blockconfidence

        btnsubmit.grid(column=0, row=0, pady=(0, padding), sticky='new')
        self.btnsubmit = btnsubmit

        btnexit.grid(column=0, row=1, pady=(0, padding), sticky='new')
        self.btnexit = btnexit
        
        btnfancy.grid(column=0, row=2, pady=(padding, padding), sticky='new')
        self.btnfancy = btnfancy

        frame.pack(padx=padding, pady=padding)

    # static widgets
    def widgetSubmit(self):
        success, results = solver(self.entry.get()).execute()

        # clear existing
        self.blockconfidence.delete('1.0', tk.END)
        self.blockconfidence.insert(tk.END, 'Score\n', 'bold')

        self.blocknames.delete('1.0', tk.END)
        self.blocknames.insert(tk.END, 'Naam\n', 'bold')

        for i in range(guesses):
            if success:
                valCONF = results[colCONF].iloc[i]
                strNAME = results[colNAME].iloc[i]
            else:
                valCONF = '-'
                strNAME = '-'

            self.blockconfidence.insert(tk.END, f'{valCONF}%\n')
            self.blocknames.insert(tk.END, f'{strNAME}\n')

    def widgetExit(self):
        sys.exit('Program ended normally')

    def widgetSwitchFancyMode(self):
        self.doFancy.set(not self.doFancy.get())

    # handle events
    def onEntryFocusIn(self, event):
        if self.entry.get() == strguide:
            self.entry.delete(0, "end") # delete all the text in the entry
            self.entry.insert(0, '') #Insert blank for user input
            self.entry.config(fg = colortxtstandard)

    def onEntryFocusOut(self, event):
        if self.entry.get() == '':
            self.entry.insert(0, strguide)
            self.entry.config(fg = colortxtfocusout)

    def onReturn(self, event):
        self.widgetSubmit()

    def onPressedKey(event):
        # quit
        if event.keycode == 27 or event.keycode == 81:
            sys.exit('Program ended normally')

    def updateBackground(self):
        increment = self.increment.get() % increments
        
        if self.doFancy.get():
            self.colorbg = rainbowcolors[increment]
        else:
            self.colorbg = colorbg

        root.configure(background=self.colorbg)
        self.frame.configure(background=self.colorbg)
        self.topframe.configure(background=self.colorbg)
        self.outputframe.configure(background=self.colorbg)
        self.btnframe.configure(background=self.colorbg)

        self.increment.set(increment + 1)
        
        root.after(updatetime, self.updateBackground)

# mainloop
root = tk.Tk()

icon = tk.PhotoImage(file='icon.png')
root.iconphoto(True, icon)

root.resizable(False, False)
root.configure(bg=colorbg)

masterGUI = MainGUI(root)
root.bind('<KeyRelease>', MainGUI.onPressedKey)
root.after(updatetime, masterGUI.updateBackground)

root.mainloop()