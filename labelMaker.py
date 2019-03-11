from os import system, name
from ftplib import FTP

# 
# A script to make print labels on the zebra printer
# by taking input, formatting it, and sending it to 
# a zebra printer via http.
#
#
# Written by: Andrew Engleman
version = "1.03"


############################################
#Console Clear 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
  


############################################
#Establish IP of zebra printer from the zebraIP.txt
# getIP[0] will return IP 
# getIP[1] will return printer name
def getIP():
        try:
            with open('zebraIP.txt', 'r') as f:
                lines = f.readlines()
                lines = [line.rstrip('\n') for line in open('zebraIP.txt')]
                return(lines)
        except:
            setIP()
            print("Run script again now that IP is set!")
            exit()

def setIP():
	ip = raw_input( "What's your label printer's IP?: ")
	name = raw_input("What's the location? (ex: VintHill): ")
	lines= ["", ""]
	lines[0]= ip + "\n"
	lines[1]= name
	print(lines)
	with open('zebraIP.txt', 'w') as f:
		f.writelines(lines)


###############################################
# Greeting 
def greeting():
	showgreeting="""
	****************************
	***** LabelMaker V""" + version + """ *****
	****************************

	[ctrl] + [c] to exit

	Current Zebra IP is set to: 
	"""+ getIP()[0] + " " + getIP()[1] +"""
	Enter "ip" to change.

	What type of label to print?
	1. Rack Label
	2. Device to Device
	3. Device to Device by CSV file
	4. Print Small labels
	5. Print Small labels from a file
	"""

	clear()
	print(showgreeting)

##############################################
# label printing function
def label_print(zpl):

	#print(zpl)
	f = open("print.zpl","w")
	f.write(zpl)
	f.close()

	f = open("print.zpl", 'rb')
	ftp = FTP(getIP()[0])
	ftp.set_pasv(True)
	ftp.login()
	ftp.storbinary('STOR print.zpl', f)
	
	
	ftp.quit()

	"""  requests way

	url = 'http://'+getIP()[0]+'/zpl?data=' +zpl + '&dev=R&oname=UNKNOWN&otype=ZPL&print=Print+Label&pw='
	r = requests.post(url)
	"""
	print("Print complete.")

	

	
##############################################
# The format function for Rack labels
def format_rack():
	clear()
	user_continue=""
	rack=""
	zpl=""
	temp_zpl=None
	while  user_continue != "p": 
		rack= raw_input( "Enter rack name: " + rack ) 
		#        %5EXA%0D%0A%5EFO50%2C50%5EA0120%2C120%5EFD+  +%5EFS%0D%0A%5EXZ%0D%0A%0D%0A
		#temp_zpl="%5EXA%0D%0A%5EFO50%2C50%5EA0120%2C120%5EFD+" +rack+ "+%5EFS%0D%0A%5EXZ%0D%0A%0D%0A"
		temp_zpl= """^XA
					 ^FO50,50^A0120,120^FD""" +rack+ """ ^FS
				     ^XZ
			      """
		zpl+=temp_zpl
		user_continue= raw_input("[Enter] for another, [p] to print: ")
	return(zpl)

#############################################
# Format for device to device
def format_devicetodevice():
	clear()
	user_continue=""
	zpl=""
	while user_continue != "p":
		device1= raw_input("Device 1: ")
		port1= raw_input("Port: ")
		device2= raw_input("Device 2: ")
		port2= raw_input("Port: ")
		#temp_zpl="%5EXA%5EFO0%2C55%5EGB600%2C35%2C35%5EFS%5EFO0%2C110%5EGB600%2C35%2C35%5EFS%5EFO300%2C0%5EGB2%2C200%2C2%5EFS%5EFO5%2C25%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EFO5%2C58%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO5%2C92%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO5%2C113%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO5%2C155%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EFO595%2C25%2C1%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EFO595%2C58%2C1%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO595%2C92%2C1%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO595%2C113%2C1%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO595%2C155%2C1%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EXZ%0D%0A" 
		#%5EXA%5EFO0%2C55%5EGB600%2C35%2C35%5EFS%5EFO0%2C110%5EGB600%2C35%2C35%5EFS%5EFO300%2C0%5EGB2%2C200%2C2%5EFS%5EFO5%2C25%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EFO5%2C58%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO5%2C92%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO5%2C113%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO5%2C155%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EFO595%2C25%2C1%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EFO595%2C58%2C1%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO595%2C92%2C1%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO595%2C113%2C1%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO595%2C155%2C1%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EXZ%0D%0A"
		#temp_zpl="null%5EXA%5EFO0%2C55%5EGB600%2C35%2C35%5EFS%5EFO0%2C110%5EGB600%2C35%2C35%5EFS%5EFO300%2C0%5EGB2%2C200%2C2%5EFS%5EFO5%2C25%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EFO5%2C58%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO5%2C92%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO5%2C113%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO5%2C155%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EFO595%2C25%2C1%5EFR%5EA0%2C20%5EFD" +device1+ "%5EFS%5EFO595%2C58%2C1%5EFR%5EA0%2C40%5EFD" +port1+ "%5EFS%5EFO595%2C92%2C1%5EFR%5EAC%5EFD%3C%3D%3E%5EFS%5EFO595%2C113%2C1%5EFR%5EA0%2C40%5EFD" +port2+ "%5EFS%5EFO595%2C155%2C1%5EFR%5EA0%2C20%5EFD" +device2+ "%5EFS%5EXZ%0D%0A"
		temp_zpl= "^XA^FO0,42^GB600,35,35^FS^FO0,120^GB600,35,35^FS^FO300,0^GB2,200,2^FS^FO5,12^FR^A0,30^FD"+device1+"^FS^FO5,45^FR^A0,40^FD"+port1+"^FS^FO5,80^FR^AC^FD"       "^FS^FO5,100^FR^AC^FD"       "^FS^FO5,123^FR^A0,40^FD" + port2+ "^FS^FO5,165^FR^A0,30^FD"+device2+"^FS^FO595,12,1^FR^A0,30^FD" + device1 +"^FS^FO595,45,1^FR^A0,40^FD"+port1+"^FS^FO595,80,1^FR^AC^FD"     "^FS^FO595,100,1^FR^AC^FD"     "^FS^FO595,123,1^FR^A0,40^FD"+ port2+ "^FS^FO595,165,1^FR^A0,30^FD"+ device2+"^FS^XZ^XA^FO0,42^GB600,35,35^FS^FO0,120^GB600,35,35^FS^FO300,0^GB2,200,2^FS^FO5,12^FR^A0,30^FD"+device2+"^FS^FO5,45^FR^A0,40^FD"+port2+"^FS^FO5,80^FR^AC^FD"   "^FS^FO5,100^FR^AC^FD"   "^FS^FO5,123^FR^A0,40^FD"+port1+"^FS^FO5,165^FR^A0,30^FD"+device1+"^FS^FO595,12,1^FR^A0,30^FD"+device2+"^FS^FO595,45,1^FR^A0,40^FD"+port2+"^FS^FO595,80,1^FR^AC^FD"   "^FS^FO595,100,1^FR^AC^FD"    "^FS^FO595,123,1^FR^A0,40^FD" + port1+ "^FS^FO595,165,1^FR^A0,30^FD" + device1+ "^FS^XZ"
		zpl+=temp_zpl
		user_continue= raw_input("[Enter] for another, [p] to print: ")
	return(zpl)

#############################################
# Format for device to device from file
def format_devicetoDeviceFile():
	clear()
	user_continue=""
	device1=""
	port1=""
	device2=""
	port2=""
	temp_zpl=None
	zpl=""
	print("Make sure the file is in the same directory/folder as this program.\n")
	print("Give full filename. Example: 'devices.csv'")
	sensorFile = raw_input("What file would you like to read from?: ")
	with open(sensorFile) as f:
		for line in f:
			splitLine = line.split(",")
			print( line, splitLine)
			device1 = splitLine[0]
			port1 = splitLine[1]
			device2= splitLine[2]
			port2=   splitLine[3]
			temp_zpl= "^XA^FO0,42^GB600,35,35^FS^FO0,120^GB600,35,35^FS^FO300,0^GB2,200,2^FS^FO5,12^FR^A0,30^FD"+device1+"^FS^FO5,45^FR^A0,40^FD"+port1+"^FS^FO5,80^FR^AC^FD"       "^FS^FO5,100^FR^AC^FD"       "^FS^FO5,123^FR^A0,40^FD" + port2+ "^FS^FO5,165^FR^A0,30^FD"+device2+"^FS^FO595,12,1^FR^A0,30^FD" + device1 +"^FS^FO595,45,1^FR^A0,40^FD"+port1+"^FS^FO595,80,1^FR^AC^FD"     "^FS^FO595,100,1^FR^AC^FD"     "^FS^FO595,123,1^FR^A0,40^FD"+ port2+ "^FS^FO595,165,1^FR^A0,30^FD"+ device2+"^FS^XZ^XA^FO0,42^GB600,35,35^FS^FO0,120^GB600,35,35^FS^FO300,0^GB2,200,2^FS^FO5,12^FR^A0,30^FD"+device2+"^FS^FO5,45^FR^A0,40^FD"+port2+"^FS^FO5,80^FR^AC^FD"   "^FS^FO5,100^FR^AC^FD"   "^FS^FO5,123^FR^A0,40^FD"+port1+"^FS^FO5,165^FR^A0,30^FD"+device1+"^FS^FO595,12,1^FR^A0,30^FD"+device2+"^FS^FO595,45,1^FR^A0,40^FD"+port2+"^FS^FO595,80,1^FR^AC^FD"   "^FS^FO595,100,1^FR^AC^FD"    "^FS^FO595,123,1^FR^A0,40^FD" + port1+ "^FS^FO595,165,1^FR^A0,30^FD" + device1+ "^FS^XZ"
			zpl+=temp_zpl
		return(zpl)

#############################################
# Format for small font labels
def format_smallFont():
	clear()
	user_continue=""
	top=""
	bottom=""
	zpl=""
	temp_zpl=None
	while  user_continue != "p": 
		top= raw_input( "Enter top row text: " ) 
		bottom= raw_input( "Enter bottom row text: " ) 

		#        %5EXA%0D%0A%5EFO50%2C50%5EA0120%2C120%5EFD+  +%5EFS%0D%0A%5EXZ%0D%0A%0D%0A
		#temp_zpl="%5EXA%0D%0A%5EFO50%2C50%5EA0120%2C120%5EFD+" +rack+ "+%5EFS%0D%0A%5EXZ%0D%0A%0D%0A"
		temp_zpl= """^XA
					 ^FO10,10^A060,60^FD""" +top+ """ ^FS
					 ^FO10,80^A035,35^FD""" +bottom+ """ ^FS
				     ^XZ
			      """
		zpl+=temp_zpl
		user_continue= raw_input("[Enter] for another, [p] to print: ")
	return(zpl)

####################################################
# Format for small font labels for senstors text file
def format_smallFontFile():
	clear()
	user_continue=""
	top=""
	bottom=""
	zpl=""
	temp_zpl=None
	print("Make sure the file is in the same directory/folder as this program.\n")
	print("Give full filename. Example: 'sensors.txt'")
	sensorFile = raw_input("What file would you like to read from?: ")
	with open(sensorFile) as f:
		for line in f:
			splitLine = line.split(":")
			top = splitLine[1]
			bottom = splitLine[0]
			temp_zpl= """^XA
					 ^FO10,10^A060,60^FD""" +top+ """ ^FS
					 ^FO10,80^A035,35^FD""" +bottom+ """ ^FS
				     ^XZ
			      """
			zpl+=temp_zpl
		return(zpl)
		

def main():
	while True:
		greeting()

		choice= raw_input("Type number followed by [ENTER]:")

		########### Set IP ##########################
		if choice == "ip":
			setIP()
		########### RACK LABELS #########################
		elif choice == "1": 
			printJob= format_rack()
			#print(printJob)
			label_print(printJob)
			break
		########### Device to Device ####################
		elif choice == "2":
			printjob = format_devicetodevice()
			#print(printjob)
			label_print(printjob)
			break
		########### Print Device2Device by file ####################
		elif choice == "3":
			printjob = format_devicetoDeviceFile()
			#print(printjob)
			label_print(printjob)
			break
		########### Small text label ####################
		elif choice == "4":
			printjob = format_smallFont()
			#print(printjob)
			label_print(printjob)
			break
		########### Print by file ####################
		elif choice == "5":
			printjob = format_smallFontFile()
			#print(printjob)
			label_print(printjob)
			break


main()
