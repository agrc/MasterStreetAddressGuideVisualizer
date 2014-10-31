'''
Created on Aug 29, 2014

@author: kwalker
'''
from ToolModules import AddressTableParser

class Test_InputFieldExtraction():
    
    def checkBuildStreetName(self):
        apiKey = "AGRC-EB4DCEF4346265"
        inputTable = r"C:\KW_Working\Geocoder_Tools\Zip_plus4\2012_11.mdb\ZIP4_845_Table_Tester"
#         outputDirectory = r"C:\Users\kwalker\Documents\GitHub\ZipPlusFour\ToolModules\data\newFiltersTest"#"C:\Users\kwalker\Documents\GitHub\ZipPlusFour\ToolModules\data"
        
        dirValue = "N"
        street = "100 EAST"
        testParser = AddressTableParser.MsagTableParser(inputTable)
        streetNameActual = testParser._buildStreetName(dirValue, street)
        streetNameExpected = dirValue + " " + street
       
        testPassed = streetNameActual == streetNameExpected
        print "Actual: {}, Expected: {}, Test passed: {}".format(streetNameActual, streetNameExpected, testPassed)
        
    def checkListCreation(self):
        inputTable = r"C:\KW_Working\Geocoder_Tools\Msag\SanJuanTestTable.dbf"
        testParser = AddressTableParser.MsagTableParser(inputTable)
        testAddrAndGrpList = testParser.getAddressListAndGrps()
        for grp in testAddrAndGrpList[1]:
            print "Group Number: {}".format(grp.groupNumber)
            for addr in grp.getAddresses():
                print "\t{}".format(addr)
        
        
if __name__ == "__main__":
    
    inputFieldTester = Test_InputFieldExtraction()
    #inputFieldTester.checkBuildStreetName()
    inputFieldTester.checkListCreation()