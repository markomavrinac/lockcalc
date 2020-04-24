#everything under the hood goes here
import datetime as dt
class Distance(object):
    def __init__(self, origin, destination,donutGalaxy,donutSystem,numberOfGalaxies): #[3 244 15], [2 424 12]
        self.rawCoords1 = origin
        self.rawCoords2 = destination
        self.galaxy1 = origin[0]
        self.solar1 = origin[1]
        self.slot1 = origin[2]
        self.galaxy2 = destination[0]
        self.solar2 =  destination[1]
        self.slot2 = destination[2]
        self.donutGalaxy = donutGalaxy
        self.donutSystem = donutSystem
        self.numberOfGalaxies = numberOfGalaxies
    def __moonToPlanet(self):
        return 5
    def __inSystem(self, slot1, slot2):
        
        return 1000+5*abs(slot2-slot1)
    def __inGalaxy(self,solar1,solar2):
        if not self.donutSystem:
            return 2700+(95*(abs(solar2-solar1)))
        else:
            route1 = abs(solar2-solar1)
            route2 = 499 - route1
            difference = min(route1,route2)
            return 2700+(95*difference)
    def __crossGalaxy(self,galaxy1,galaxy2):
        if not self.donutGalaxy:
            return 20000*abs(galaxy2-galaxy1)
        else:
            route1 = abs(galaxy2-galaxy1)
            route2 = self.numberOfGalaxies - route1
            difference = min(route1,route2)
            return 20000*abs(difference)
    def getDistance(self):
        if self.rawCoords1==self.rawCoords2:
            return self.__moonToPlanet()
        elif (self.galaxy1 == self.galaxy2) and (self.solar1==self.solar2):
            return self.__inSystem(self.slot1,self.slot2)
        elif self.galaxy1 == self.galaxy2:
            return self.__inGalaxy(self.solar1,self.solar2)
        else:
            return self.__crossGalaxy(self.galaxy1,self.galaxy2)
        
class TravelTime(object):
    def __init__(self, ship, distance, flightSpeed, uniSpeed, playerClass, generalBoost, collectorBoost):
        self.ship = ship
        self.distance = distance
        self.flightSpeed = flightSpeed
        self.uniSpeed = uniSpeed
        self.playerClass = playerClass
        self.generalBoost = generalBoost
        self.collectorBoost = collectorBoost
    def getFlightTime(self):
        timeInSeconds = round(((35000/self.flightSpeed)*(self.distance.getDistance()*1000/self.ship.getSpeed(self.playerClass, self.generalBoost, self.collectorBoost))**(0.5)+10)/self.uniSpeed)
        hours = int(str(timeInSeconds/3600).split(".")[0])
        remainder = timeInSeconds-hours*3600
        minutes = int(str(remainder/60).split(".")[0])
        seconds = remainder - minutes*60
        return hours, minutes, seconds
    def getReturnTime(self,arrivalTime, delay, recallTime):
        flightTime = self.getFlightTime()
        flightTime = dt.timedelta(hours=flightTime[0],minutes=flightTime[1],seconds=flightTime[2])
        arrival = dt.datetime(int(arrivalTime[0]),int(arrivalTime[1]),int(arrivalTime[2]),int(arrivalTime[3]),int(arrivalTime[4]),int(arrivalTime[5])) #year,month,day,hour,minute,second
        returnTime = arrival + flightTime
        
        if recallTime == False:
            return [returnTime.day,returnTime.month,returnTime.year,returnTime.hour,returnTime.minute,returnTime.second]
        
        else:
            recallTime = dt.datetime(int(recallTime[0]),int(recallTime[1]),int(recallTime[2]),int(recallTime[3]),int(recallTime[4]),int(recallTime[5]))
            recallInterval = arrival - recallTime
            
            #latest return time
            lateReturnTime = returnTime - 2*recallInterval
            delay = dt.timedelta(seconds=int(delay))
            earlyReturnTime = lateReturnTime - 2*delay
            if lateReturnTime == earlyReturnTime:
                return [earlyReturnTime.day,earlyReturnTime.month,earlyReturnTime.year,earlyReturnTime.hour,earlyReturnTime.minute,earlyReturnTime.second]
            else:
                return([earlyReturnTime.day,earlyReturnTime.month,earlyReturnTime.year,earlyReturnTime.hour,earlyReturnTime.minute,earlyReturnTime.second],[lateReturnTime.day,lateReturnTime.month,lateReturnTime.year,lateReturnTime.hour,lateReturnTime.minute,lateReturnTime.second]) #a tuple of lists
    

class Ship(object):
    def __init__(self, name, baseSpeed, drive, drives, shipType):
        self.name = name
        self.baseSpeed = baseSpeed
        self.drive = drive
        self.combo = drives[0]
        self.impulse = drives[1]
        self.hyper = drives[2]
        self.shipType = shipType
        if self.name == "Small Cargo" and self.impulse>=5:
            self.drive = "Impulse"
            self.baseSpeed = 10000
        if self.name == "Recycler" and self.impulse>=17:
            self.drive == "Impulse"
            self.baseSpeed = 4000
        
        if self.name == "Bomber" and self.hyper>=8:
            self.drive = "Hyper"
            self.baseSpeed = 5000
        if self.name == "Recycler" and self.hyper>=15:
            self.drive = "Hyper"
            self.baseSpeed = 6000
        
        if self.drive == "Combustion":
            self.multiplier = 0.1
        elif self.drive == "Impulse":
            self.multiplier = 0.2
        elif self.drive == "Hyper":
            self.multiplier = 0.3
        
        
    def getDriveLevel(self,drive):
        if drive == "Combustion":
            return self.combo
        elif drive == "Impulse":
            return self.impulse
        elif drive == "Hyper":
            return self.hyper

    def getSpeed(self, playerClass, generalBoost, collectorBoost):
        classBonus = 0
        if playerClass == "General":
            if (self.name == "Recycler" or self.shipType == "military") and self.name != "Deathstar":
                classBonus = float(generalBoost)
        elif playerClass == "Collector":
            if self.name == "Small Cargo" or self.name == "Large Cargo":
                classBonus = float(collectorBoost)
        self.speed = round(self.baseSpeed*(classBonus + 1 + self.multiplier*self.getDriveLevel(self.drive)))
        return int(self.speed)
    
        
class LockLogic(object):
    def __init__(self, arrivalTime, arrivalCoords, planetList, drives, onlyRecs, uniSpeed, tableObject, donutGalaxy, donutSystem, playerClass, collectorBoost, generalBoost, numberOfGalaxies, choosenShip, filterPlanetBool, filterPlanetSelect): # (arrivalTime= [13 24 57], arrivalCoords = [3 244 8], planetList =[[3,3,3],[2,123,15]], drives = [14,12,15], onlyRecs = True, uniSpeed = 6, mode = "Per planet"/"Fastest flight", tableObject = object reference to the table we want to fill)
        self.arrivalTime = dt.datetime(arrivalTime[2], arrivalTime[1], arrivalTime[0], arrivalTime[3],arrivalTime[4],arrivalTime[5])
        self.planetList = planetList
        self.onlyRecs = onlyRecs
        self.choosenShip = choosenShip #related to ship filtering
        self.tableObject = tableObject
        self.drives=drives
        self.combo = drives[0]
        self.impulse = drives[1]
        self.hyper = drives[2]
        self.arrivalCoords = arrivalCoords
        self.uniSpeed = uniSpeed
        self.donutGalaxy = donutGalaxy
        self.donutSystem = donutSystem
        self.playerClass = playerClass
        self.collectorBoost = collectorBoost
        self.generalBoost = generalBoost
        self.numberOfGalaxies = numberOfGalaxies
        self.filterPlanetBool = filterPlanetBool
        self.filterPlanetSelect = filterPlanetSelect
        
    def sortByAttribute(self,objectList, attribute, maxLength=15):
        sortedList = []
        while len(objectList)>1 and len(sortedList)<maxLength:
            smallestValueObject = objectList[0]
            for i in objectList:
                if getattr(i, attribute) <= getattr(smallestValueObject, attribute):
                    smallestValueObject = i
            sortedList.append(smallestValueObject)
            objectList.remove(smallestValueObject)
        else:
            if len(objectList)>0:
                sortedList.append(objectList[0]) #last object goes to the end of the list, if I don't put if statement the script crashes on empty list
        return sortedList
    def __getLockTimes(self, origin, destination, ships, donutGalaxy, donutSystem, numberOfGalaxies, uniSpeed): #time when we're supposed to send the fleet in order to lock along with other identifying info
        lockTimes = []
        speedList = [100,90,80,70,60,50,40,30,20,10]
        currentTime = dt.datetime.now()
        distance = Distance(origin, destination, donutGalaxy, donutSystem, numberOfGalaxies)
        for ship in ships:
            for speed in speedList:
                travelTimeHours, travelTimeMinutes, travelTimeSeconds = TravelTime(ship, distance, speed, uniSpeed, self.playerClass, self.generalBoost, self.collectorBoost).getFlightTime()
                travelTimeDelta = dt.timedelta(hours = travelTimeHours, minutes = travelTimeMinutes, seconds = travelTimeSeconds)
                lockTime = self.arrivalTime - travelTimeDelta #datetime object
                if (lockTime - currentTime) > TableResult.zero: #if lock can happen after current time, if not it's expired
                    lockTimes.append((origin, lockTime, ship.name, speed, travelTimeDelta))
        return lockTimes
            
            
    def fillTable(self):
        results = []
        TableResult.purgeResults()
        if self.onlyRecs: #not only recs anymore but left it as it is so I don't mess up this mess even more, onlyRecs now presents state of specific ship checkbox
            ships = onlyShip(self.drives, self.choosenShip)
        else:
            ships = createShips(self.drives)
        if self.filterPlanetBool:
            planetList = self.filterPlanetSelect
        else:
            planetList = self.planetList
        for planet in planetList: #cycle through every coordinate
            lockTimes = self.__getLockTimes(planet, self.arrivalCoords, ships, self.donutGalaxy, self.donutSystem, self.numberOfGalaxies, self.uniSpeed) #get lock times for all ships for these coordinates
            objectList = []
            for lockTime in lockTimes:
                objectList.append(TableResult(lockTime[0],lockTime[1],lockTime[2],lockTime[3],lockTime[4])) #origin, lockTime (dt object), ship.name (str), speed, travelTimeDelta -> append TableResult objects into an empty list for later
            results+=objectList
        results = self.sortByAttribute(results, "lockInterval")
        TableResult.submitResults(self.tableObject, results)
        return results

        
class TableResult(object):
    results=[] #we keep track of all results here
    zero = dt.timedelta(seconds=0) #artificial zero for comparison with datetime objects
    def __init__(self, coords, lockTime, ship, speed, flightTime): # coords = [3 24 5], lockin = vec neki format vidjet cemo, "Light Fighter", 10, "vec neki format"
        self.coords = coords
        self.lockTime = lockTime
        self.ship = ship
        self.speed = speed
        self.flightTime = flightTime
        self.trigger = True #bell trigger
        self.lockInterval = lockTime - dt.datetime.now()
        TableResult.results.append(self)
    def purgeResults():
        TableResult.results = []
    def getLockInterval(self, lockVar = None): #basically refresh the time until lock value
        self.lockInterval = self.lockTime - dt.datetime.now()
        if self.lockInterval<TableResult.zero:
            self.lockInterval = "lock expired"
            if lockVar:
                lockVar = False
        return str(self.lockInterval).split(".")[0]
  
    def submitResults(tableObject, results):
        for i in tableObject.get_children(): #not sure if I can just overlap over old items but it's been 6 hoursssss so tired (for anyone interested, yes it will overlap)
            tableObject.delete(i)
        indexCounter = 1 #this is to make sure to get proper index on treeview in the main GUI
        for result in results:
            tableObject.insert("", indexCounter, None, text= "", values=("[%s %s %s]"%(result.coords[0], result.coords[1], result.coords[2]),result.getLockInterval(),result.ship,"%i%%"%(result.speed),result.flightTime))
            indexCounter+=1
def createShips(drives):
    sc = Ship("Small Cargo", 5000, "Combustion",drives, "civil")
    lc = Ship("Large Cargo", 7500, "Combustion",drives, "civil")
    lf = Ship("Light Fighter", 12500, "Combustion",drives, "military")
    hf = Ship("Heavy Fighter", 10000, "Impulse",drives, "military")
    cru = Ship("Cruiser", 15000, "Impulse",drives, "military")
    bs = Ship("Battleship", 10000, "Hyper",drives, "military")
    colo = Ship("Colony Ship", 2500, "Impulse",drives, "civil")
    rec = Ship("Recycler", 2000, "Combustion",drives, "civil")
    bomb = Ship("Bomber", 4000, "Impulse",drives, "military")
    des = Ship("Destroyer", 5000, "Hyper",drives, "military")
    rip = Ship("Deathstar", 100, "Hyper",drives, "military")
    bc = Ship("Battlecruiser", 10000, "Hyper",drives, "military")
    rp = Ship("Reaper", 7000, "Hyper", drives, "military")
    pf = Ship("Pathfinder", 12000, "Hyper", drives, "military")
    return [sc,lc,lf,hf,cru,bs,colo,rec,bomb,des,rip,bc,rp,pf]
def onlyShip(drives, shipName): #just so I don't break all the logic of the script with modifications to already used functions, I make this one so the return type to handle rec filtering in gui
    for ship in createShips(drives):
        if shipName==ship.name:
            return [ship]