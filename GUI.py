
version = "0.9b"
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import os #sys can't exit....okkkkkk
import core
import threading
import time
import pygame
class LockCalc(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def __parser(self,flag,parameter):
        if flag == "planets":
            self.numberOfPlanets = int(parameter)
        elif flag == "uniSpeed":
            self.uniSpeed = int(parameter)
        elif flag == "galaxies":
            self.numberOfGalaxies = int(parameter)
        elif flag == "donutGalaxy":
            self.donutGalaxy = bool(parameter)
        elif flag == "donutSystem":
            self.donutSystem = bool(parameter)
        elif flag == "collectorBoost":
            self.collectorBoost = float(parameter)
        elif flag == "generalBoost":
            self.generalBoost = float(parameter)
        elif flag == "combo":
            self.combo = int(parameter)
        elif flag == "impulse":
            self.impulse = int(parameter)
        elif flag == "hyper":
            self.hyper = int(parameter)
        elif flag == "class":
            self.playerClass = parameter #it's already just a string
        else:
            raise
    def finishButton(self):
        for i in range(1,self.numberOfPlanets+1):
            try:
                self.planets = []
                exec("self.planet%i=[int(self.planetGalaxyEntry%i.get()),int(self.planetSystemEntry%i.get()),int(self.planetSlotEntry%i.get())]"%(i,i,i,i))
                exec("self.planets.append(self.planet%i)"%(i))
            except:
                messagebox.showerror("Bad input","Planet %i - input invalid!"%(i))
                return        
        self.saveOptions()
        messagebox.showinfo("Restart required", "Please restart the program so the settings load correctly.")
        os._exit(1) #if I start LC right away for some reason it loads only one planet and messes everything up
    def saveOptions(self):
        try:
            target = open("settings.ini","w")
            output=""
            output+="planets %i\n"%(self.numberOfPlanets)
            output+="uniSpeed %i\n"%(self.uniSpeed)
            output+="galaxies %i\n"%(self.numberOfGalaxies)
            if self.donutGalaxy:
                output+="donutGalaxy 1\n"
            else:
                output+="donutGalaxy 0\n"
            if self.donutSystem:
                output+="donutSystem 1\n"
            else:
                output+="donutSystem 0\n"
            output+= "collectorBoost %.2f\n"%(self.collectorBoost)
            output+= "generalBoost %.2f\n"%(self.generalBoost)
            output+= "combo %i\n"%(self.combo)
            output+= "impulse %i\n"%(self.impulse)
            output+= "hyper %i\n"%(self.hyper)
            output+= "class %s\n"%(self.playerClass)
            output+= "PLANETLIST\n"
            planetlist = ""
            for i in range(1,self.numberOfPlanets+1):
                planetlist+="%i %i %i,"%(int(eval("self.planetGalaxyEntry%i"%i).get()),int(eval("self.planetSystemEntry%i"%i).get()), int(eval("self.planetSlotEntry%i"%i).get()))
            planetlist = planetlist[0:len(planetlist)-1] #removing last comma
            output+=planetlist
            target.write(output)
            target.close()
        except:
            messagebox.showerror("Permission denied", "No write permissions in current folder.\nThe program will exit.")
            os._exit(1)
    def stopIt(self): #STAAAHP
        self.stop = True
    def setTableUp(self):
        self.bellTrigger=True
        logic = core.LockLogic([int(self.dayArrival.get()),int(self.monthArrival.get()),int(self.yearArrival.get()),int(self.hourArrival.get()),int(self.minuteArrival.get()),int(self.secondArrival.get())],[int(self.arrivalGalaxyEntry.get()),int(self.arrivalSystemEntry.get()),int(self.arrivalSlotEntry.get())],self.planets, [self.combo,self.impulse,self.hyper], self.onlyShipVar.get(), self.uniSpeed, self.table, self.donutGalaxy, self.donutSystem, self.playerClass, self.collectorBoost, self.generalBoost, self.numberOfGalaxies, self.onlyShipSelectCombo.get(), self.singlePlanetVar.get(), self.__handlePlanetChoice(self.singlePlanetSelectCombo.get()))
        self.results = logic.fillTable() #I fetch results here so I can use them as argument to refresh and hopefully reduce time needed to refresh because part of code executes once per click only
    def refresh(self):
        while not self.stop:
            indexCounter = 0 #to keep track of items in self.results
            for child in self.table.get_children():
                try:
                    self.table.item(child, text = "", values=("[%s %s %s]"%(self.results[indexCounter].coords[0], self.results[indexCounter].coords[1], self.results[indexCounter].coords[2]),self.results[indexCounter].getLockInterval(),self.results[indexCounter].ship,"%i%%"%(self.results[indexCounter].speed),self.results[indexCounter].flightTime))
                except:
                    self.setTableUp()
                indexCounter+=1
            if len(self.table.get_children())>0:
                if(self.table.item(self.table.get_children()[0])["values"][1])=="lock expired":
                    self.setTableUp()

                elif(int(self.table.item(self.table.get_children()[0])["values"][1].split(":")[0])==0 and int(self.table.item(self.table.get_children()[0])["values"][1].split(":")[1])==0 and int(self.table.item(self.table.get_children()[0])["values"][1].split(":")[2])<30 and int(self.table.item(self.table.get_children()[0])["values"][1].split(":")[2])>10):
                    if self.bellTrigger and self.dingBool.get():
                        self.bellSound.play()
                        self.bellTrigger = False
            else:
                self.setTableUp()            

            #core.TableResult.purgeResults()
            #core.TableResult.submitResults(self.table, self.results)
            time.sleep(1)
            
        else:
            self.stop=False
            return         

        
    def track(self):
        try:
            if self.trackButton['text'] == "Track":
                self.trackButton.config({'text':"Stop tracking"})
                self.editButton.config({'state':tk.DISABLED})
                self.setTableUp()
    
                self.thread = threading.Thread(group=None, target = self.refresh, args=())
                self.thread.start()
                
            elif self.trackButton['text'] == "Stop tracking":
                self.editButton.config({'state':tk.NORMAL})
                self.trackButton.config({'text':"Track"})
                self.stop=True
        except:
            messagebox.showerror("Bad input", "Please input arrival time and coordinates correctly.")
            self.editButton.config({'state':tk.NORMAL})
            self.trackButton.config({'text':"Track"})
            self.stop=False
    def lockCalc(self):
        self.LC = tk.Toplevel()
        self.LC.grid()
        self.LC.title('LockCalc by Savage')
        self.LC.focus_force()
        self.LC.protocol("WM_DELETE_WINDOW", purge)
        self.LC.resizable(False,False)
        try:
            self.setupQuery.wm_withdraw()
        except:
            pass
        try:
            self.wm_withdraw()
        except:
            pass
        self.makeWeight(self.LC,20)
        coordinateFrame = tk.Frame(self.LC,relief=tk.GROOVE,borderwidth = 2)
        self.makeWeight(coordinateFrame,20)
        coordinateLabel = tk.Label(coordinateFrame,justify = tk.CENTER, text ="Coordinates and Arrival Time", font = ("Segoe UI",10,"bold"))
        coordinateLabel.grid(row=0,column=0,columnspan=20)        
        coordinateFrame.grid(row=2,column=0,columnspan=20,sticky = 'NSEW')
        arrivalLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Arrival Time:")
        arrivalLabel.grid(row=1,column=0,columnspan=5,sticky = 'E')
        arrivalFrame = tk.Frame(coordinateFrame,relief=tk.GROOVE,borderwidth = 2)
        arrivalFrame.grid(row=1,column=5,columnspan=15,sticky='W')
        self.makeWeight(arrivalFrame,18)
        self.dayArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.dayArrival.grid(row=0,column=0,columnspan=3,sticky='WE')
        self.monthArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.monthArrival.grid(row=0,column=3,columnspan=3,sticky='WE')
        self.yearArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=6)
        self.yearArrival.grid(row=0,column=6,columnspan=3,sticky='WE')        
        self.hourArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.hourArrival.grid(row=0,column=9,columnspan=3,sticky='WE')
        self.minuteArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.minuteArrival.grid(row=0,column=12,columnspan=3,sticky='WE')
        self.secondArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.secondArrival.grid(row=0,column=15,columnspan=3,sticky='WE')
        currentTime = dt.datetime.now()
        self.dayArrival.insert(0,str(currentTime.day))
        self.monthArrival.insert(0,str(currentTime.month))
        self.yearArrival.insert(0,str(currentTime.year))
        self.arrivalCoordinatesLabel = tk.Label(coordinateFrame,text = "Arrival coordinates:", justify = tk.CENTER)
        self.arrivalCoordinatesLabel.grid(row=2,column=0,columnspan=10,sticky = 'E')
        arrivalCoordinatesFrame = tk.Frame(coordinateFrame,relief=tk.GROOVE,borderwidth = 2)
        arrivalCoordinatesFrame.grid(row=2,column=10,columnspan=10,sticky='W')
        self.makeWeight(arrivalCoordinatesFrame,10)
        self.arrivalGalaxyEntry = tk.Entry( arrivalCoordinatesFrame, justify=tk.CENTER,width=5)
        self.arrivalGalaxyEntry.grid(row=0,column=0,columnspan=3,sticky="EW")
        self.arrivalSystemEntry = tk.Entry( arrivalCoordinatesFrame, justify=tk.CENTER,width=6)
        self.arrivalSystemEntry.grid(row=0,column=3,columnspan=4,sticky="EW")
        self.arrivalSlotEntry = tk.Entry( arrivalCoordinatesFrame, justify=tk.CENTER,width=5)
        self.arrivalSlotEntry.grid(row=0,column=7,columnspan=3,sticky="EW")
        settingsFrame = tk.Frame(self.LC,relief=tk.GROOVE,borderwidth = 2)
        settingsFrame.grid(row=3,column=0,columnspan=20,sticky = "NSEW")
        self.makeWeight(settingsFrame,20)
        settingsLabel = tk.Label(settingsFrame,text="Settings",justify = tk.CENTER, font = ("Segoe UI",10,"bold"))
        settingsLabel.grid(row=0,column=0,columnspan=20)
        self.uniSpeedLabel = tk.Label(settingsFrame,text="Uni speed = %i"%(self.uniSpeed),justify = tk.CENTER)
        self.uniSpeedLabel.grid(row=1,column=0,columnspan=20)
        self.numberOfGalaxiesLabel = tk.Label(settingsFrame,text="Galaxies = %i"%(self.numberOfGalaxies),justify = tk.CENTER)
        self.numberOfGalaxiesLabel.grid(row=2,column=0,columnspan=20)
        self.donutGalaxyLabel = tk.Label(settingsFrame,text="Donut galaxy = %s"%(str(bool(self.donutGalaxy))),justify = tk.CENTER)
        self.donutGalaxyLabel.grid(row=3,column=0,columnspan=20)
        self.donutSystemLabel = tk.Label(settingsFrame,text="Donut system = %s"%(str(bool(self.donutSystem))),justify = tk.CENTER)
        self.donutSystemLabel.grid(row=4,column=0,columnspan=20)
        self.playerInfoLabel = tk.Label(settingsFrame,text="Player Info",justify = tk.CENTER, font = ("Segoe UI",10,"bold"))
        self.playerInfoLabel.grid(row=5,column=0,columnspan=20)
        self.playerClassLabel = tk.Label(settingsFrame,text="Player class: %s"%(self.playerClass),justify = tk.CENTER)
        self.playerClassLabel.grid(row=6,column=0,columnspan=20)
        self.comboLabel = tk.Label(settingsFrame,text="Combustion = %i"%(self.combo),justify = tk.CENTER)
        self.comboLabel.grid(row=7,column=0,columnspan=20)
        self.impulseLabel = tk.Label(settingsFrame,text="Impulse = %i"%(self.impulse),justify = tk.CENTER)
        self.impulseLabel.grid(row=8,column=0,columnspan=20)
        self.hyperLabel = tk.Label(settingsFrame,text="Hyperspace = %i"%(self.hyper),justify = tk.CENTER)
        self.hyperLabel.grid(row=9,column=0,columnspan=20)
        self.boostLabel = tk.Label(settingsFrame,text="General/Collector boost = %.2f/%.2f"%(self.generalBoost,self.collectorBoost),justify = tk.CENTER)
        self.boostLabel.grid(row=10,column=0,columnspan=20)
        self.editButton = tk.Button(settingsFrame, text = "Edit", justify = tk.CENTER,command = self.startSetup)
        self.editButton.grid(row=11,column=0,columnspan=20,sticky="EW")
        reportFrame = tk.Frame(self.LC,relief=tk.GROOVE,borderwidth = 2)
        reportFrame.grid(row=12,column=0,columnspan=20,sticky="NSEW")
        self.makeWeight(reportFrame,20)
        self.table = ttk.Treeview(reportFrame,height = 15)
        self.table["columns"]=("coords","lockin","ship","speed", "flighttime")
        self.table.grid(row=0,column=0,columnspan=20)
        self.table.column("#0",stretch=tk.NO,width=75,minwidth=75,anchor=tk.CENTER)
        self.table.column("coords",stretch=tk.NO,width=75,anchor=tk.CENTER)
        self.table.column("lockin",stretch=tk.NO,width=75,anchor=tk.CENTER)
        self.table.column("ship",stretch=tk.NO,width=100,anchor=tk.CENTER)
        self.table.column("speed",stretch=tk.NO,width=50,anchor=tk.CENTER)
        self.table.column("flighttime",stretch=tk.NO,width=75,anchor=tk.CENTER)
        self.table['show'] = 'headings'
        self.table.heading("#0", text= "Coordinates",anchor=tk.CENTER)
        self.table.heading("coords", text= "Coordinates",anchor=tk.CENTER)
        self.table.heading("lockin", text= "Lock in",anchor=tk.CENTER)
        self.table.heading("ship", text= "Ship",anchor=tk.CENTER)
        self.table.heading("speed", text= "Speed",anchor=tk.CENTER)
        self.table.heading("flighttime", text= "Flight time",anchor=tk.CENTER)
        
        
        onlyRecsLabel = tk.Label(reportFrame, text = "Filter only selected ship", justify = tk.CENTER) #it says only recs because it was initially supposed to filter recs, so I don't mess up the whole code I decided to leave it like this, it's related to choosing a specific ship as a target filter
        onlyRecsLabel.grid(row=12, column=0, columnspan=9,sticky = 'E')
        self.onlyShipSelectCombo = ttk.Combobox(reportFrame, width=20, values = ["Small Cargo", "Large Cargo", "Light Fighter", "Heavy Fighter", "Cruiser", "Battleship", "Colony Ship", "Recycler", "Bomber", "Destroyer", "Deathstar", "Battlecruiser", "Reaper", "Pathfinder"], justify = tk.CENTER, state="readonly")
        self.onlyShipSelectCombo.grid(row=12,column=9,columnspan=8,sticky='W')
        self.onlyShipVar = tk.IntVar()
        self.onlyRecsCheck = tk.Checkbutton(reportFrame,var = self.onlyShipVar)
        self.onlyRecsCheck.grid(row=12,column=17,columnspan=3,sticky = "W")
        #planet filtering below (only UI)
        singlePlanetLabel = tk.Label(reportFrame, text = "Filter only selected planet", justify = tk.CENTER) #it says only recs because it was initially supposed to filter recs, so I don't mess up the whole code I decided to leave it like this, it's related to choosing a specific ship as a target filter
        singlePlanetLabel.grid(row=13, column=0, columnspan=9,sticky = 'E')
        self.singlePlanetSelectCombo = ttk.Combobox(reportFrame, width=20, values = self.__getPlanetListPretty(), justify = tk.CENTER, state="readonly")
        self.singlePlanetSelectCombo.grid(row=13,column=9,columnspan=8,sticky='W')
        self.singlePlanetVar = tk.IntVar()
        self.singlePlanetCheck = tk.Checkbutton(reportFrame,var = self.singlePlanetVar)
        self.singlePlanetCheck.grid(row=13,column=17,columnspan=3,sticky = "W")
        dingLabel = tk.Label(reportFrame, text = "Sound notification", justify = tk.CENTER)
        dingLabel.grid(row=14,column=0,columnspan=12,sticky="E")
        self.dingBool = tk.IntVar()
        self.dingCheck = tk.Checkbutton(reportFrame,var = self.dingBool)
        self.dingCheck.grid(row=14,column=12,columnspan=8, sticky="W")
        self.trackButton = tk.Button(self.LC, text = "Track", justify = tk.CENTER,command = self.track)
        self.trackButton.grid(row=15,column=0,columnspan=20,sticky="NSEW")
    def __handlePlanetChoice(self, choice): #format chosen planet from x:xxx:x to [[x,xxx,x]] -> return type list in list to skip having to make special cases in core script in case of a single choice, this way for loop only works once instead of once for each planet, used to basically transform choice from filter planet combobox to data that can be reffered to
        if len(choice.split(":"))==3:
            planet = [int(choice.split(":")[0]),int(choice.split(":")[1]),int(choice.split(":")[2])]
        else:
            return
        return [planet]
    def __getPlanetListPretty(self): #this is used to display planet list in the combobox!
        planetList = []
        for planet in self.planets:
            planetList.append("{}:{}:{}".format(planet[0], planet[1], planet[2]))
        return planetList
    def startSetup(self): #1st setup menu
        self.setup = tk.Toplevel()
        self.makeWeight(self.setup,10)
        self.setup.grid()
        self.setup.title('Setup')
        self.setup.protocol("WM_DELETE_WINDOW", purge)
        self.setup.resizable(False,False)
        try:
            self.LC.wm_withdraw()
        except:
            pass #making sure we can get to this menu from both starting the program and by clicking edit button later
        self.setup.focus_force()
        selectPlanetLabel = tk.Label(self.setup, text = "Select number of planets:")
        selectPlanetLabel.grid(row=0,column=0)
        self.selectPlanetCombo = ttk.Combobox(self.setup, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], state = "readonly", justify = tk.CENTER, width = 10)
        self.selectPlanetCombo.set(1)
        self.selectPlanetCombo.grid(row=0, column = 1)
        uniSpeedLabel = tk.Label(self.setup, text = "Uni speed:", justify = tk.CENTER)
        uniSpeedLabel.grid(row=1,column=0)
        self.uniSpeedCombo = ttk.Combobox(self.setup, values=[1,2,3,4,5,6], state = "readonly", justify = tk.CENTER, width = 10)
        self.uniSpeedCombo.set(1)
        self.uniSpeedCombo.grid(row=1,column=1)
        numberOfGalaxieslabel = tk.Label(self.setup, text = "Number of galaxies:", justify = tk.CENTER)
        numberOfGalaxieslabel.grid(row=2,column=0)
        self.numberOfGalaxiesCombo = ttk.Combobox(self.setup, values=[1,2,3,4,5,6,7,8,9], state = "readonly", justify = tk.CENTER, width = 10)
        self.numberOfGalaxiesCombo.grid(row=2,column=1)
        self.numberOfGalaxiesCombo.set(9)
        donutGalaxyLabel = tk.Label(self.setup, justify = tk.CENTER, text = "Donut Galaxy")
        donutGalaxyLabel.grid(row=4,column=0)
        self.donutGalaxyVar = tk.IntVar()
        self.donutGalaxyCheck = tk.Checkbutton(self.setup,var = self.donutGalaxyVar) #OPTION
        self.donutGalaxyCheck.select()
        self.donutGalaxyCheck.grid(row=4,column=1)
        donutSystemLabel = tk.Label(self.setup, justify = tk.CENTER, text = "Donut System")
        donutSystemLabel.grid(row=5,column=0)
        self.donutSystemVar = tk.IntVar()
        self.donutSystemCheck = tk.Checkbutton(self.setup, var = self.donutSystemVar) #OPTION
        self.donutSystemCheck.select()
        self.donutSystemCheck.grid(row=5,column=1)
        collectorBoostLabel = tk.Label(self.setup, justify = tk.CENTER, text = "Collector speed boost:")
        collectorBoostLabel.grid(row=6,column=0)
        self.collectorBoostCombo = ttk.Combobox(self.setup, values = self.getBoostRange(1,0.25), state = 'readonly', justify = tk.CENTER, width = 10)
        self.collectorBoostCombo.grid(row=6,column=1)
        self.collectorBoostCombo.set(1)
        generalBoostLabel = tk.Label(self.setup, justify = tk.CENTER, text = "General speed boost:")
        generalBoostLabel.grid(row=7,column=0)
        self.generalBoostCombo = ttk.Combobox(self.setup, values = self.getBoostRange(1,0.25), state = 'readonly', justify = tk.CENTER, width = 10)
        self.generalBoostCombo.grid(row=7,column=1)
        self.generalBoostCombo.set(1)
        playerInfoLabel = tk.Label(self.setup, text= "Player Info", justify = tk.CENTER, font = ("Segoe UI",10,"bold"))
        playerInfoLabel.grid(row=8,column=0, columnspan=2)
        
        combustionLabel = tk.Label(self.setup,justify = tk.CENTER, text = "Combustion Drive:")
        combustionLabel.grid(row=9,column=0)
        self.combustionEntry = tk.Entry(self.setup,justify = tk.CENTER, width = 13)
        self.combustionEntry.grid(row=9,column=1)
        impulseLabel = tk.Label(self.setup,justify = tk.CENTER, text = "Impulse Drive:")
        impulseLabel.grid(row=10,column=0)
        self.impulseEntry = tk.Entry(self.setup,justify = tk.CENTER, width = 13)
        self.impulseEntry.grid(row=10,column=1)
        hyperLabel = tk.Label(self.setup,justify = tk.CENTER, text = "Hyperspace Drive:")
        hyperLabel.grid(row=11,column=0)
        self.hyperEntry = tk.Entry(self.setup,justify = tk.CENTER, width = 13)
        self.hyperEntry.grid(row=11,column=1)
        self.classLabel = tk.Label(self.setup, justify = tk.CENTER, text = "Class:")
        self.classLabel.grid(row=12,column=0)
        self.classCombo = ttk.Combobox(self.setup, values = ["Collector", "General", "Discoverer"], width = 10, state = 'readonly', justify = tk.CENTER)
        self.classCombo.grid(row=12, column=1)
        
        selectPlanetButton = tk.Button(self.setup, text = "Next", command = self.setupFinal)
        selectPlanetButton.grid(row=15,column=0,columnspan=2,sticky='EW')
    def setupFinal(self): #second setup menu
        try:
            self.combo = int(self.combustionEntry.get())
            self.impulse = int(self.impulseEntry.get())
            self.hyper = int(self.hyperEntry.get())
        except:
            messagebox.showerror("Bad input","Bad drive levels!")
            return
        try:
            self.playerClass = self.classCombo.get()
            if len(self.playerClass)==0:
                messagebox.showerror("Bad input", "Class not selected!")
                return
        except:
            messagebox.showerror("Bad input","Class not selected!")
            return
        self.numberOfPlanets = int(self.selectPlanetCombo.get())
        self.uniSpeed = int(self.uniSpeedCombo.get())
        self.numberOfGalaxies = int(self.numberOfGalaxiesCombo.get())
        self.donutGalaxy = self.donutGalaxyVar.get()
        self.donutSystem = self.donutSystemVar.get()
        self.collectorBoost = float(self.collectorBoostCombo.get())
        self.generalBoost = float(self.generalBoostCombo.get())
        
        self.setupQuery = tk.Toplevel()
        self.setup.destroy()
        self.makeWeight(self.setupQuery,10)
        self.setupQuery.grid()
        self.setupQuery.title("Setup")
        self.setupQuery.protocol("WM_DELETE_WINDOW", purge)
        self.setupQuery.resizable(False,False)
        titleLabel = tk.Label(self.setupQuery,text = "Please enter your planet coordinates", justify = tk.CENTER, font = ("Segoe UI",10,"bold"))
        titleLabel.grid(row=0,column=0,columnspan=10)
        counter=1
        for i in range(1,self.numberOfPlanets+1): #we make as many widgets as there are planets, probably could've been done without exec but as there's no user input it's not unsafe (I assume??xD)
            counter+=1
            command1 = "planetLabel%i=tk.Label(self.setupQuery,text = 'Planet %i:', justify = tk.CENTER)"%(i,i)
            command2 = "planetLabel%i.grid(row=%i,column=0,columnspan=5)"%(i,i)
            command3 = "self.planetGalaxyEntry%i = tk.Entry(self.setupQuery,justify=tk.CENTER,width=3)"%i
            command4 = "self.planetGalaxyEntry%i.grid(row=%i,column=5,sticky='WE')"%(i,i)
            command5 = "self.planetSystemEntry%i = tk.Entry(self.setupQuery,justify=tk.CENTER,width=5)"%i
            command6 = "self.planetSystemEntry%i.grid(row=%i,column=6,columnspan=3,sticky='WE')"%(i,i)
            command7 = "self.planetSlotEntry%i = tk.Entry(self.setupQuery,justify=tk.CENTER,width=3)"%i
            command8 = "self.planetSlotEntry%i.grid(row=%i,column=9,sticky='WE')"%(i,i)            
            exec(command1+"\n"+command2+"\n"+command3+"\n"+command4+"\n"+command5+"\n"+command6+"\n"+command7+"\n"+command8)
        finishButton = tk.Button(self.setupQuery,text = "Finish", justify = tk.CENTER,command=self.finishButton)
        finishButton.grid(row=counter,column=0,columnspan=10,sticky='EW')
        
    def getBoostRange(self, maxValue, increment): #just so I don't have to dig manually through the code if limits turn out to be different
        output = []
        assert(maxValue>increment)
        currentValue = increment
        while currentValue<=maxValue:
            if int(currentValue)!=currentValue:
                output.append(currentValue)
            else:
                output.append(int(currentValue)) #avoiding 1.0 etc
            currentValue+=increment
        return output    
    def makeWeight(self,object,iterations): #related to tkinter, needed to organize UI elements easier and avoid overlapping
        for i in range(iterations):
            object.columnconfigure(i,weight=1)
    
    def initialize(self):
        pygame.mixer.init()
        self.bellSound = pygame.mixer.Sound("beep.wav")
        self.bellTrigger = True
        self.stop = False #flag that the thread uses to stop itself, set by clicking Stop tracking button
        self.wm_withdraw() #since I will be using multiple windows, I'll just go ahead and get rid of root
        numberOfPlanets = 0
        uniSpeed = 0
        playerClass = False
        generalBoost = 1
        collectorBoost = 1
        
        try:
            a= open("settings.ini",'r')
            content = a.readlines()
            a.close()            
        except:
            self.startSetup()
        try:
            for setting in content:
                if len(setting.split()) == 2:
                    flag, parameter = setting.split()
                    parameter = parameter.rstrip()
                    self.__parser(flag, parameter)
                elif len(setting.split()) == 1:
                    if setting.rstrip() == "PLANETLIST":
                        break
                    else:
                        raise #no 1 word commands other than PLANETLIST
            planetList = content[len(content)-1].rstrip().split(",")
            assert(len(planetList)==self.numberOfPlanets) #if there's different amount of planets listed than the flag says, we raise error
            self.planets = []
            for i in range(self.numberOfPlanets):
                exec("self.planet%i=[int(planetList[%i].split()[0]),int(planetList[%i].split()[1]),int(planetList[%i].split()[2])]"%(i+1,i,i,i))
                exec("self.planets.append(self.planet%i)"%(i+1))
            self.lockCalc()
        except:
            messagebox.showinfo("Bad settings file", "Settings file is corrupted or missing.\nYou will be guided through the setup process.")

    
def purge(): #to make sure app is killed upon killing child windows, also making sure we don't murder someone's PC with a rogue thread
    app.stopIt()
    time.sleep(2) #allow the tracking thread to stop
    try:
        app.thread.join() #if thread was never called this throws an error so this is a poor man's way of patching it
    except:
        os._exit(1)
    os._exit(1)

        
        
        
        
        
        


if __name__ == "__main__":
    app = LockCalc(None)
    app.title('LockCalc')
    app.resizable(False,False)
    app.protocol("WM_DELETE_WINDOW", purge)
    app.mainloop()