#Illinois Safety Program - Heatmaps Python Script
#Created by Yousef Dana (Milhouse Engineering) (ydana@milhouseinc.com)
#This script updates the symbology of a crash data layer for each data driven page within an ArcMap document and exports to PDF


#Imports ArcPy environment
import arcpy

#Sets parameters for ArcMap
MXDFile = arcpy.GetParameterAsText(0)
EA = arcpy.GetParameterAsText(1)
SavingDirectory = arcpy.GetParameterAsText(2)
EAnum = arcpy.GetParameterAsText(3)

#Sets today's Date
todayDate = datetime.date.today().strftime("%Y%m%d")

#Sets variables for the script
mxd = arcpy.mapping.MapDocument(MXDFile)                                    #ArcMap File
df = arcpy.mapping.ListDataFrames(mxd)[0]                                   #Creates a matrix of dataframes found in the ArcMap File
lyr = arcpy.mapping.ListLayers(mxd)[0]                                      #Creates a matrix of layers found in the ArcMap File
countylyr = arcpy.mapping.ListLayers(mxd,wildcard="County Boundary")[0]     #Finds the layer that determines the data-driven pages

#Loops through each county/data-driven page
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    pageName = mxd.dataDrivenPages.pageRow.COUNTY_NAM
    for lyr in arcpy.mapping.ListLayers(mxd):

        #Grabs every layer that has a graduated symbols property, and sets the emphasis area and number of classes
        if lyr.symbologyType == "GRADUATED_COLORS":
            lyr.symbology.valueField = EA
            
            #Selects the county layer so it can find the max and min
            arcpy.SelectLayerByAttribute_management(countylyr,"NEW_SELECTION","[STATE_CODE]="+str(pageNum))
            arcpy.SelectLayerByLocation_management(lyr,"WITHIN",countylyr,selection_type="NEW_SELECTION")

            #Finds the maximum and minimum crashes within the county to set then class values
            maxNumberList = []
            for r in arcpy.SearchCursor(lyr):
                  maxNumberList.append(r.getValue(EA))
            maxCrashValueOrig = int(math.ceil(max(maxNumberList)))
            maxCrashValue = maxCrashValueOrig + 1
            v1=10**-100

	#Assigns different numbers of classes based on the maximum crash value
            if maxCrashValue >= 5:

                v2=int(math.ceil(maxCrashValue/5))
                v3=int(math.ceil((maxCrashValue/5)*2))
                v4=int(math.ceil((maxCrashValue/5)*3))
                v5=int(math.ceil((maxCrashValue/5)*4))

                lyr.symbology.classBreakValues = [v1,v2,v3,v4,v5,maxCrashValue]
                lyr.symbology.classBreakLabels = ["1 to " + str(v2),
                                                  str(v2+1) + " to " + str(v3),
                                                  str(v3+1) + " to " + str(v4),
                                                  str(v4+1) + " to " + str(v5),
                                                  str(v5+1) + " to " + str(maxCrashValue)]

            elif maxCrashValue == 4:

                v2=1
                v3=2
                v4=3

                lyr.symbology.classBreakValues = [v1,v2,v3,v4,maxCrashValue]
                lyr.symbology.classBreakLabels = ["1 to " + str(v2),
                                                  str(v2+1) + " to " + str(v3),
                                                  str(v3+1) + " to " + str(v4),
                                                  str(v4+1) + " to " + str(maxCrashValue)]

            elif maxCrashValue == 3:

                  v2=1
                  v3=2
                  
                  lyr.symbology.classBreakValues = [v1,v2,v3,maxCrashValue]
                  lyr.symbology.classBreakLabels = ["1", "2", "3"]

            elif maxCrashValue == 2:
			
                  v2=1
                  
                  lyr.symbology.classBreakValues = [v1,v2,maxCrashValue]
                  lyr.symbology.classBreakLabels = ["1", "2"]

            elif maxCrashValue == 1:

                  lyr.symbology.classBreakValues = [v1,maxCrashValue]
                  lyr.symbology.classBreakLabels = ["1"]

            elif maxCrashValue < 1:

                  lyr.symbology.classBreakValues = [0,maxCrashValue]
                  lyr.symbology.classBreakLabels = ["1"]

            else:
                  arcpy.AddMessage("ERROR: MaxValue out of range!")

            #De-selects the county layer
            arcpy.SelectLayerByAttribute_management(countylyr,"CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(lyr,selection_type="CLEAR_SELECTION")

            #Exports a PDF for each page
            arcpy.AddMessage("Exporting page {0} of {1}".format(str(mxd.dataDrivenPages.currentPageID), str(mxd.dataDrivenPages.pageCount)))
            arcpy.mapping.ExportToPDF(mxd, SavingDirectory + "\Heatmap2012to2016_EA" + EAnum + "_" + str(pageName) + "County_" + todayDate)

del mxd