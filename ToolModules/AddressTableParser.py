'''
Created on Aug 18, 2014

@author: kwalker
'''

import arcpy, fields, MsagVisualizerTool
from operator import attrgetter
#from MsagVisualizerTool import Address



class MsagTableParser (object):
    
    def __init__(self, addressTable):
        self._addressTable = addressTable

    
    
    def _getStreetSideLists(self, addressLowNum, addressHighNum):
        lowNum = int(addressLowNum)
        highNum = int(addressHighNum)
        streetSideLists = []
        evenSide = []
        oddSide = []
        
        if (lowNum % 10) < 2:
            lowNum += 2
        
        if (highNum % 10) < 2:
            highNum -= 2
            
        if lowNum % 2 == 0:
            evenSide.append(lowNum)
            oddSide.append(lowNum + 1)
        else:
            evenSide.append(lowNum + 1)
            oddSide.append(lowNum)
        
        if highNum % 2 == 0:
            evenSide.append(highNum)
            oddSide.append(highNum - 1)
        else:
            evenSide.append(highNum - 1)
            oddSide.append(highNum)
        
        streetSideLists.append(self._getHouseNumbers(evenSide[0], evenSide[1]))
        streetSideLists.append(self._getHouseNumbers(oddSide[0], oddSide[1]))
        return streetSideLists
            
    
    def _getHouseNumbers(self, addressLowNum, addressHighNum):
        """Creates house numbers from range between provided fields."""
        
        lowNum = int(addressLowNum)
        highNum = int(addressHighNum)

        #Check that both numbers odd or even
        if lowNum % 2 != highNum % 2:
            lowNum += 1
        

        houseNumList = [str(lowNum)]# + 2 Moves low number two away from the corner
    
        numdiff = int(highNum) - int(lowNum)
        
        if numdiff > 1000:
            highNum = str(lowNum + 1000)
            numdiff = int(highNum) - int(lowNum)
    

        if numdiff > 40:
            for num in range(int(lowNum) + 20, int(highNum), 20):
                houseNumList.append(num)
                
        if numdiff > 4:
            houseNumList.append(str(highNum))# - 2 Moves high number two away from the corner
        
        elif numdiff > 0:
            houseNumList.append(str(highNum))
        
        return houseNumList    


    def _buildStreetName(self, preDir, streetName):
        """Build the street name from parts that exist in many fields in input table"""
        streetAddress = ""
    
        if not preDir == None:
            if len(preDir) > 0:
                streetAddress = preDir
    
        streetAddress = streetAddress + " " + streetName.strip()
    

        for c in range(34,48):
            streetAddress = streetAddress.replace(chr(c)," ")
        streetAddress = streetAddress.replace("_"," ")
        
        return streetAddress
    

    
    def getAddressListAndGrps(self):
        addrList = []
        addrGrps = []
        addrGrpNumber = 1
        inFields = fields.Input()
        fieldList = inFields.getFields()       
    
        with arcpy.da.SearchCursor(self._addressTable, fieldList) as cursor:
            for row in cursor:
                
                streetName = self._buildStreetName(row[inFields.getI(inFields.preDirection)], row[inFields.getI(inFields.streetName)])
                
                zone = str(row[inFields.getI(inFields.zone)])
                if zone == None:
                    zone = ""

                houseNumList = self._getStreetSideLists(row[inFields.getI(inFields.lowHouseNum)], row[inFields.getI(inFields.highHouseNum)])#row[0], row[1])
                for numList in houseNumList:
                    tempAddrGroupList = []
                    addressGroup = MsagVisualizerTool.AddressGroup(addrGrpNumber)
                    tempAddrGroupList.append(addressGroup)
                    addrGrpNumber += 1
                    
                    addrI = 0
                    for houseNum in numList:
                        if addrI == 0:
                            lowAddr = MsagVisualizerTool.Address(streetName, houseNum, zone, addrI, row[inFields.getI(inFields.objectId)])#row[11])
                            addrList.append(lowAddr)                            
                            for addressGroup in tempAddrGroupList:
                                addressGroup.addAddress(lowAddr)
                        elif addrI != (len(numList) - 1):                    
                            midAddr = MsagVisualizerTool.Address(streetName, houseNum, zone, addrI, row[inFields.getI(inFields.objectId)])
                            addrList.append(midAddr)
                            for addressGroup in tempAddrGroupList:
                                addressGroup.addAddress(midAddr)
                        elif addrI == (len(numList) - 1):                         
                            highAddr = MsagVisualizerTool.Address(streetName, houseNum, zone, addrI, row[inFields.getI(inFields.objectId)])
                            addrList.append(highAddr)
                            for addressGroup in tempAddrGroupList:
                                addressGroup.addAddress(highAddr)
                    
                        addrI += 1
                    
                    addrGrps.extend(tempAddrGroupList)
                                   
                
                
        return [addrList, addrGrps]
    
    def getAddressGroups(self):
        
        return self._addressGroups
        
    
        
        