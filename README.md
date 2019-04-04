# barcode_function
The encompassing image recognition package for the Greenbot Rover Project

# Launch file (init.launch)
Use the command "roslaunch [user] barcode_functions init.launch" to run.

# Barcode Generation (barcode_generator)
Allows for mass generation of QR codes.
To increase the number of QR codes, modify the two variables at the beginning of the script.

# Alert System (alert_system)
Broadcasts two boolean values for the topics /isNotRepeated_QR and /isMissed_QR.

If a QR code is not repeated, /isNotRepeated_QR will provide a "True" value, which can be used to tell the robot to stop to scan the unique QR code.

/isMissed_QR will provide a "True" value if a barcode is missed in the sequence.
- Modifications need to be made to include row/aisle number in the sequence checking
- Additional interaction with the sensor serial data should be made in the case of a plant leaf obstructing a QR code
- This means that if a QR code is missed, but the sensor reads that there is an obstruction that the operator should be aware.

# Excel Logger (excel_writer)
Will save a file in (barcode_functions > src > logs).
Consider enabling configuration of file names to the operator as mandatory to prevent over writing of sessions.
Default log file name is log.xlsx

# Barcode Parser (barcode_parser)
Enables the data to be extracted from the current format
Consider adding a try/catch statement in case a QR of a different format is scanned.
