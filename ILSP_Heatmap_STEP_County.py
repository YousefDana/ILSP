#Illinois Safety Program - STEP Heatmaps Python Script
#Created by Yousef Dana (Milhouse Engineering) (ydana@milhouseinc.com)

#This script sets the symbology a PLSS layer and exports to PDF.


#Imports ArcPy environment
import arcpy

#Sets parameters for ArcMap
MXDFile = arcpy.GetParameterAsText(0)
SavingDirectory = arcpy.GetParameterAsText(1)

#Sets today's Date
todayDate = datetime.date.today().strftime("%Y%m%d")

#Sets variables for the script
mxd = arcpy.mapping.MapDocument(MXDFile)    #Sets the ArcMap File
df = arcpy.mapping.ListDataFrames(mxd)[0]   #Chooses the first data frame
lyr = arcpy.mapping.ListLayers(mxd)[0]      #Chooses the first layer within the first data frame
CrashAtt = "Total_KABC"                     #Sets the attribute for the PLSS heat maps

#Loops through each county/data-driven page
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum

    for lyr in arcpy.mapping.ListLayers(mxd):

        #Grabs every layer that has a graduated symbols property, and sets the attribute
        if lyr.symbologyType == "GRADUATED_COLORS":
            lyr.symbology.valueField = CrashAtt
    
    #Sets the county name depending on the row of the data-driven page
    countyName = mxd.dataDrivenPages.pageRow.STEPCounties

    #Exports a PDF for each page and displays the progress
    arcpy.AddMessage("Exporting page {0} of {1}".format(str(mxd.dataDrivenPages.currentPageID), str(mxd.dataDrivenPages.pageCount)))
    arcpy.mapping.ExportToPDF(mxd, SavingDirectory + "\County of " + str(countyName) + "_STEP_Map&Crash_Tables_" + todayDate)
del mxd