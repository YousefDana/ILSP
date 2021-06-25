#Illinois Safety Program - STEP Heatmaps Python Script
#Created by Yousef Dana (Milhouse Engineering) (ydana@milhouseinc.com)

#This script sets the symbology for two PLSS layers found in different data-frames, 
#sets a definition query for the city layer, has the extent of the second dataframe 
#zoom into the extent of the city layer in that dataframe, and exports to PDF.


#Imports ArcPy environment
import arcpy

#Sets parameters for ArcMap
MXDFile = arcpy.GetParameterAsText(0)
SavingDirectory = arcpy.GetParameterAsText(1)

#Sets today's Date
todayDate = datetime.date.today().strftime("%Y%m%d")

#Sets variables for the script
mxd = arcpy.mapping.MapDocument(MXDFile)                                        #Sets the ArcMap File
df = arcpy.mapping.ListDataFrames(mxd)[0]                                       #Chooses the first data frame
lyr = arcpy.mapping.ListLayers(mxd)[0]                                          #Chooses the first layer within the first data frame
CrashAtt = "Total_KABC"                                                         #Sets the attribute for the PLSS heat maps

#Loops through each county/data-driven page
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum

    #I am doing two different loops because they fall under two data-frames. Is that needed?
    #First for loop for the main-frame
    for lyr in arcpy.mapping.ListLayers(mxd):

        #Grabs every layer that has a graduated symbols property, and sets the attribute
        if lyr.symbologyType == "GRADUATED_COLORS":
            lyr.symbology.valueField = CrashAtt

    #Second for loop for the zoom-in frame
    for citylyr in arcpy.mapping.ListLayers(mxd):

        #Grabs every layer that has a graduated symbols property, and sets the attribute
        if citylyr.symbologyType == "GRADUATED_COLORS":
            citylyr.symbology.valueField = CrashAtt

    dfzoomin = arcpy.mapping.ListDataFrames(mxd)[1]                                 #Chooses the second data frame
    citylyr = arcpy.mapping.ListLayers(mxd,wildcard="CityBoundaryZoomIn")[0]        #Sets the city layer that determines the zoom-in
    
    #Sets defintions and zooms the Zoom-In dataframe to the City Layer
    cityName = mxd.dataDrivenPages.pageRow.STEPAgencies             #Sets the city name depending on the row of the data-driven page
    countyName = mxd.dataDrivenPages.pageRow.STEPCounty             #Sets the county name depending on the row of the data-driven page
    citylyr.definitionQuery = "[NAME]='" + str(cityName) + "'"      #Sets a definition query for the citylayer
    ext = citylyr.getExtent()                                       #Gets the extent of the citylayer
    dfzoomin.extent = ext                                           #Zooms the dataframe to the citylayer extent

    #Exports a PDF for each page and displays the progress
    arcpy.AddMessage("Exporting page {0} of {1}".format(str(mxd.dataDrivenPages.currentPageID), str(mxd.dataDrivenPages.pageCount)))
    arcpy.mapping.ExportToPDF(mxd, SavingDirectory + "\City_of_" + str(cityName) + "_in_" + str(countyName) + "County_STEP_Map&Crash_Tables_" + todayDate)
del mxd