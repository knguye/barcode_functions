#!/usr/bin/env python2.7
import rospy
import re
import openpyxl
from std_msgs.msg import String
from custom_msgs.msg import IntList

# Function: To take data from the barcode parser and write the data on the xls file
wb = openpyxl.Workbook()
log_sheet = wb.active # Set log_sheet to active sheet for writing 
filename = "log" # MODIFY this to change the name of the log file.
username = "knguye" # MODIFY this to the current username to enable operation

filepath = "/home/{}".format(username) + "/catkin_ws/src/barcode_functions/logs/{}.xlsx".format(filename) #replace knguye with user
# openpyxl
b = IntList()
row = 2

# Create headers for rows
log_sheet['A1'] = 'Row'
log_sheet['B1'] = 'Location'
log_sheet['C1'] = 'Timestamp'

def getData(data):
    global row
    global b
    
    # try: # if QR is valid format for this usage
    if (data.data != b): # if the last barcode isnt a duplicate
        b = data.data 
        # Copying the values onto the excel cells
        log_sheet['A{}'.format(str(row))] = b[0]
        log_sheet['B{}'.format(str(row))]= b[1]
        log_sheet['C{}'.format(str(row))] = rospy.get_time()
        row  = row + 1
        rospy.loginfo("Logging data on Excel..")
        wb.save(filepath) # overwrite spreadsheet in real time
    # except:
    #    rospy.loginfo("Invalid QR format")

    #c = 0 # first val at 0, second at 1.. resets for each new entry
    #for values in data: 
            #log_sheet.cell(row, col, values)
            #col = col + 1
            #rospy.loginfo(values)
    #row = row + 1
    # Parse the data to get numbers
    # b = data
    #rospy.loginfo(data) # debug

    # For some reason, the open pyxl functions dont work here

def main():
    rospy.init_node('excel_writer', anonymous=False) # Anon = false to allow multiple excel writers
    #while not rospy.is_shutdown():
    rospy.Subscriber("/qr_data", IntList, getData) # Take data from topic and send to writing function
    rospy.spin()

if __name__ == "__main__":
    main()
