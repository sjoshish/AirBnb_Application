#Script
import arcpy
import pandas as pd
import openpyxl

#Creates a new file geodatabase to store outputs in
arcpy.CreateFileGDB_management(r"C:\Users\sshrestha\Desktop\Linear_Segmentation_AFB\Patrick AFB & Cape Canaveral\GeoCGI Data Sent\Data Summary\Electrical", "Patrick_AFB.gdb")
output_geodatabase_location = r'C:\Users\sshrestha\Desktop\Linear_Segmentation_AFB\Patrick AFB & Cape Canaveral\GeoCGI Data Sent\Data Summary\Electrical\Patrick_AFB.gdb'
utilitiesElectricalLocation = r'C:\Users\sshrestha\Desktop\Linear_Segmentation_AFB\Patrick AFB & Cape Canaveral\GeoCGI Data Sent\2021LinearSegPatrick\2021LinearSegPatrick\2021LinearSegPatrick\SXHT_Patrick8_13_21.gdb\utilitiesElectrical'
dataModelLocation = r'C:\Users\sshrestha\Desktop\311_AFIMSCDet2_shell.gdb\311_AFIMSCDet2_shell.gdb\311_AFIMSCDet2_shell.gdb\utilitiesElectrical'

#For an accurate summary report, this function updates all feature classes in the UtilitiesElectrical feature
#dataset for cells with an empty(blank) value. It updates all blank cells to a NULL value.
def convertToNull():

    arcpy.env.workspace = utilitiesElectricalLocation
    fcList = arcpy.ListFeatureClasses()

    for fc in fcList:
        with arcpy.da.UpdateCursor(fc, ["*"]) as cursor:
            print("Updating blank cells to NULL for", fc)
            for row in cursor:
                #print(row)
                for i in range((len(row))):
                    if ((row[i] == ' ') or (row[i] == 'TBD') or (row[i] == 'N/A') or (row[i] == 'To be determined')):
                        row[i] = None
                
                    cursor.updateRow(row)


def exportMissingFCTableList():
    dataModelfcList, dataSentfcList, list_difference = [],[],[]
    arcpy.env.workspace = dataModelLocation
    dataModel = arcpy.ListFeatureClasses()
    for fc in dataModel:
        dataModelfcList.append(fc)


    arcpy.env.workspace = utilitiesElectricalLocation
    dataSent = arcpy.ListFeatureClasses()
    for fc in dataSent:
        dataSentfcList.append(fc)

    
    for item in dataModelfcList:
        if item not in dataSentfcList:
            list_difference.append(item)

    targetFile = r"C:\Users\sshrestha\Desktop\Linear_Segmentation_AFB\Patrick AFB & Cape Canaveral\GeoCGI Data Sent\Data Summary\Electrical\Missing_FeatureClasses_Compared_to_SDSFIE3_1_Data_Model.xlsx"
    wb = openpyxl.Workbook()
    wb.save(targetFile)
    writer = pd.ExcelWriter(targetFile)
    df = pd.DataFrame(list_difference)
    df.columns = ['Missing Feature Classes']
    df.to_excel(writer)
    #del df
    writer.save()
    print("Missing feature class list exported to Excel")
