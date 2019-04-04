#!/usr/bin/env python2.7
import rospy
import functools
import re
from std_msgs.msg import Bool, Int32
from custom_msgs.msg import IntList

b = IntList()
data_vars = [0, 0]

pub = rospy.Publisher('/isNotRepeated_QR', Bool, queue_size = 1)
pub_2 = rospy.Publisher('/missed_QR', Bool, queue_size = 1)
rospy.init_node('alert_system', anonymous=False)
old_time = 0.0

def compareData(data): #, event):
    global b
    global data_vars
    global old_time
    count = 0
    new_time = rospy.get_time() # Check the time

    # delay reads by 2 seconds, not just broadcasting
    if ((new_time - old_time) > 5.0): # If the time now is 5 seconds after the barcode was scanned, fulfill this
        if (b == data.data): # if the data from the new QR is the same as the old.
            pub.publish(False) # publish false if the QR repeats
            rospy.loginfo('Repeated QR, robot ignoring..')
        else:
            if (((data_vars[1] + 1 != data.data[1]) or data_vars[0] != data.data[0]) and data_vars[1] != 0): 
                # Check if location id of new barcode is 1 more than the previous barcode. If it is not, then the barcode is missed. Also check if the row # is the same, if not, then the barcode is missed.
                pub_2.publish(True) # Publish to missed barcode topic
                # rospy.loginfo(data_vars[1])
                # rospy.loginfo(data.data[1])
                rospy.logwarn('QR code missed!') # could try to look for the missing QR code.
                rospy.logwarn('QR Data: ' + str(data.data))
                rospy.loginfo('Last QR Scanned: ' + str(b))
            else: # if barcode is not missed
                b = data.data
                for var in data.data: # Set data_vars to have the values of the QR code just scanned for next comparison.
                    data_vars.insert(count, var)
                    count += 1
                    pub_2.publish(False) # Publish barcode not missed (false)
                rospy.loginfo('New QR code detected')
                rospy.loginfo('QR Data: ' + str(b))
                pub.publish(True) # Barcode not repeated (True)
                # The robot should stop if isNotRepeated_QR == true. We want to scan every non repeated QR.
                rospy.loginfo("Stopping robot to scan..")
        old_time = rospy.get_time() # Last time a barcode was scanned

def main():
    #while not rospy.is_shutdown():
    rospy.Subscriber("/qr_data", IntList, compareData) # Take data from topic and send to writing function
    #rospy.Timer(rospy.Duration(2), compareData)
    rospy.spin()

if __name__ == "__main__":
    main()

