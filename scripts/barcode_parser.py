#!/usr/bin/env python2.7
import rospy
import re
from std_msgs.msg import String
from custom_msgs.msg import IntList

#
# Custom Message (IntList)

# Function: To take data from the barcode and take the numbers for processing
qr_data = IntList() # Currently ID, Location. Used for read/write
                   # Can plan later to have plant health code in FUTURE
a = [] # placeholder for qr_data
pub = rospy.Publisher('/qr_data', IntList, queue_size = 10)

def parse(data):
  parsed_str = re.split("\s", data.data) # parses the qr strings into ["ID", id_no, "Location", location_no], we want id_no and location_no
  # rospy.loginfo(parsed_str) # print the parsing (for debug)
  count = 0 # Used to differentiate tag id and location #

  for data_var in parsed_str: # look through all strings of the parsed string
      if data_var.isdigit(): # if the parser runs into a number, it is either the id or location number
        a.append(int(data_var)) # load id onto index 0 or location onto index 1.
        count = count + 1 # id is found, look for location

  qr_data = a # assign values of a onto qr_data for publishing
  
  #rospy.logdebug(qr_data) # print the individual data value (debug)  # QR data is now recorded on the qr_data variable
  pub.publish(qr_data)
  
  del a[:] # Clear a

def main():
  rospy.init_node('barcode_parser', anonymous=False)
  rospy.Subscriber("/barcode", String, parse)
  # for data in qr_data: # Transfer one value at a time
  rospy.spin()

if __name__ == '__main__':
  main() # Listen for barcode, get data