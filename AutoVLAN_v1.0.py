#Import Libraries #
import paramiko
import time
import getpass
import re
# User Defined Functions #
def CiscoConfig(): # Model and execute Cisco needed configuration.
	def CiscoCoreConf():
		if optionstate == 'option_1':
			addciscovlan()
		elif optionstate == 'option_2':
			addciscorange()
		elif optionstate == 'option_3':
			ciscodelvlanonce()
		elif optionstate == 'option_4':
			if allowstate == "novlan-trunk":
				if allowreq == "access":
					addciscovlan()
					ciscodefint()
					ciscocallint()
					ciscoaccesstotrunk()
				elif allowreq == "trunk":
					addciscovlan()
					ciscocallint()
					ciscotrunktotrunk()
			elif allowstate == "novlan-access":
				if allowreq == "access":
					addciscovlan()
					ciscocallint()
					ciscoaccesstoaccess()
				elif allowreq == "trunk":
					addciscovlan()
					ciscodefint()
					ciscocallint()
					ciscoaccesstotrunk()
			elif allowstate == "vlan-trunk" :
				if allowreq == "access":
					ciscodefint()
					ciscocallint()
					ciscotrunktoaccess()
				elif allowreq == "trunk":
					ciscocallint()
					ciscotrunktotrunk()	
			elif allowstate == "vlan-access":
				if allowreq == "access":
					ciscocallint()
					ciscoaccesstoaccess()
				elif allowreq == "trunk":
					ciscodefint()
					ciscocallint()
					ciscoaccesstotrunk()	
			elif allowstate == "novlan-blank":
				if allowreq == "access":
					addciscovlan()
					ciscodefint()
					ciscocallint()
					ciscotrunktoaccess()
				elif allowreq == "trunk":
					addciscovlan()
					ciscodefint()
					ciscocallint()
					ciscoaccesstotrunk()
			elif allowstate == "vlan-blank":
				if allowreq == "access":
					ciscodefint()
					ciscocallint()
					ciscotrunktoaccess()
				elif allowreq == "trunk":
					ciscodefint()
					ciscocallint()
					ciscoaccesstotrunk()
		elif optionstate == 'option_5':
			if allowstate == "vlan-trunk" :
					ciscocallint()
					ciscotrunkrem()
			elif allowstate == "vlan-access":
					ciscocallint()
					ciscoaccessrem()
	def addciscovlan():
		if confstate == 'preview':
			if vlanstate == 'new':
				print('vlan ' + str(rVLAN))
				print('name ' + '"' + str(newVLAND) + '"')
			else:
				pass
		elif confstate == 'execute':
			if vlanstate == 'new':
				remote_connection.send('vlan ' + str(rVLAN)  + '\n')
				remote_connection.send('name ' + '"' + str(newVLAND) + '"' + '\n')
			else:
				pass
	def addciscorange():
		if confstate == 'preview':
			for everyvlan in range(vy, vy=1):
				print('vlan ' + str(everyvlan))
				print('name ' + '"' + str(newVLAND) + '_' + str(everyvlan) +  '"')
		elif confstate == 'execute':
			for everyvlan in range(vy, vy=1):
				remote_connection.send('vlan ' + str(everyvlan)  + '\n')
				remote_connection.send('name ' + '"' + str(newVLAND) + '_' + str(everyvlan) + + '"' + '\n')
	def ciscodefint():
		if confstate == 'preview':
			print('default interface ' + str(ifname))
		elif confstate == 'execute':
			remote_connection.send('default interface ' + str(ifname) + '\n')
	def ciscocallint():
		if confstate == 'preview':
			print('interface ' + str(ifname))
		elif confstate == 'execute':
			remote_connection.send('interface ' + str(ifname) + '\n')
	def ciscotrunktoaccess():
		if confstate == 'preview':
			print('switchport')
			print('switchport mode access')
			print('switchport access vlan ' + str(rVLAN))
		elif confstate == 'execute':
			remote_connection.send('switchport\n')
			remote_connection.send('switchport mode access\n')
			remote_connection.send('switchport access vlan ' + str(rVLAN) + '\n')
	def ciscoaccesstotrunk():
		if confstate == 'preview':
			print('switchport')
			print('switchport trunk encapsulation dot1q')
			print('switchport trunk allowed vlan ' + str(rVLAN))	
			print('switchport mode trunk')
		elif confstate == 'execute':
			remote_connection.send('switchport\n')
			remote_connection.send('switchport trunk encapsulation dot1q\n')
			remote_connection.send('switchport trunk allowed vlan ' + str(rVLAN) + '\n')	
			remote_connection.send('switchport mode trunk\n')
	def ciscotrunktotrunk():
		if confstate == 'preview':
			print('switchport trunk allowed vlan add ' + str(rVLAN))
		elif confstate == 'execute':
			remote_connection.send('switchport trunk allowed vlan add ' + str(rVLAN) + '\n' )
	def ciscoaccesstoaccess():
		if confstate == 'preview':
			print('switchport access vlan ' + str(rVLAN))
		elif confstate == 'execute':
			remote_connection.send('switchport access vlan ' + str(rVLAN) + '\n')
	def ciscoaccessrem():
		if confstate == 'preview':
			print('no switchport access vlan ' + str(rVLAN))
		elif confstate == 'execute':
			remote_connection.send('no switchport access vlan ' + str(rVLAN) + '\n')
	def ciscotrunkrem():
		if confstate == 'preview':
			print('switchport trunk allowed vlan remove ' + str(rVLAN))
		elif confstate == 'execute':
			remote_connection.send('switchport trunk allowed vlan remove ' + str(rVLAN) + '\n' )
	def ciscodelvlanonce():
		if confstate == 'preview':
			for eachpipe in combinedval:
				exactpipe = re.findall("F?a?G?i?[0-9]+\/[0-9]+\/?[0-9]?[0-9]?", eachpipe)
				exactpipestr = str(exactpipe)
				for imps in bad_chars:
					exactpipestr = exactpipestr.replace(imps, '')
				if 'dot1q' in eachpipe:
					print('interface ' + str(exactpipestr))
					print('no switchport access vlan ' + str(rVLAN))
					print('exit')				
				elif 'trunk' in eachpipe:
					print('interface ' + str(exactpipestr))
					print('switchport trunk allowed vlan remove ' + str(rVLAN))
					print('exit')
				elif 'access' in eachpipe:
					print('interface ' + str(exactpipestr))
					print('no switchport access vlan ' + str(rVLAN))
					print('exit')
			print('no vlan ' + str(rVLAN))
		elif confstate == 'execute':
			for eachpipe in combinedval:
				exactpipe = re.findall("F?a?G?i?[0-9]+\/[0-9]+\/?[0-9]?[0-9]?", eachpipe)
				exactpipestr = str(exactpipe)
				for imps in bad_chars:
					exactpipestr = exactpipestr.replace(imps, '')
				if 'dot1q' in eachpipe:
					remote_connection.send('interface ' + str(exactpipestr) + '\n')
					remote_connection.send('no switchport access vlan ' + str(rVLAN) + '\n')
					remote_connection.send('exit' + '\n')				
				elif 'trunk' in eachpipe:
					remote_connection.send('interface ' + str(exactpipestr) + '\n')
					remote_connection.send('switchport trunk allowed vlan remove ' + str(rVLAN) + '\n')
					remote_connection.send('exit' + '\n')
				elif 'access' in eachpipe:
					remote_connection.send('interface ' + str(exactpipestr) + '\n')
					remote_connection.send('no switchport access vlan ' + str(rVLAN) + '\n')
					remote_connection.send('exit' + '\n')
			remote_connection.send('no vlan ' + str(rVLAN) + '\n')
	if confstate == 'preview':
		print('The following configuration will be applied upon your approval !')
		print('#'*105)
		print('configure terminal')
		CiscoCoreConf()
		print('end')
		print('#'*105)
		print("Proceed? Type 'Y' to approve or any key to abort.")
	elif confstate == 'execute':
		initSSHCall()
		remote_connection.send('configure terminal\n')
		CiscoCoreConf()
		remote_connection.send('end\n')
		remote_connection.send('wr\n')
		time.sleep(5)
		output_script_2 = remote_connection.recv(65535)
		print('#'*105)
		print("Configuration Report:")
		print('#'*105)
		print ((output_script_2).decode('ascii'))
		print('#'*105)
		ssh_client.close()
		returnBack()
def JuniperConfig(): # Model and execute Juniper needed configuration.
	def JuniperCoreConf():
		if optionstate == 'option_1':
			vlanformat()
			addlinevlan()
		elif optionstate == 'option_2':
			rangeformat()
			addrangevlan()
		elif optionstate == 'option_3':
			vlanformat()
			dellinevlanonce()
		elif optionstate == 'option_4':
			vlanformat()
			if allowstate == "novlan-trunk":
				if allowreq == "access":
					addlinevlan()
					dellineintany()
					addlineint()
					addlinetype()
				elif allowreq == "trunk":
					addlinevlan()
					addlineint()
			elif allowstate == "novlan-access":
				if allowreq == "access":
					addlinevlan()
					dellineintany()
					addlineint()
				elif allowreq == "trunk":
					addlinevlan()
					dellineintany()
					addlineint()
					addlinetype()
			elif allowstate == "vlan-trunk":
				if allowreq == "access":
					dellineintany()
					addlinetype()
					addlineint()
				elif allowreq == "trunk":
					addlineint()
			elif allowstate == "vlan-access":
				if allowreq == "access":
					dellineintany()
					addlineint()
				elif allowreq == "trunk":
					dellineintany()
					addlinetype()
					addlineint()
			elif allowstate == "novlan-blank":
				if allowreq == "access":
					addlinevlan()
					addlinetype()
					addlineint()
				elif allowreq == "trunk":
					addlinevlan()
					addlinetype()
					addlineint()
			elif allowstate == "vlan-blank":
				if allowreq == "access":
					dellineintany()
					addlinetype()
					addlineint()
				elif allowreq == "trunk":
					dellineintany()
					addlinetype()
					addlineint()
		elif optionstate == 'option_5':
			vlanformat()
			dellineint()
	def rangeformat():
		global rangelength
		for everyvlan in range(vx, vy+1):
			everyvlanlen = len(str(everyvlan))
			if everyvlanlen == 1:
				rangelength = 'VLAN000'
			elif everyvlanlen == 2:
				rangelength = 'VLAN00'
			elif everyvlanlen == 3:
				rangelength = 'VLAN0'
			elif everyvlanlen == 4:
				rangelength = 'VLAN'
	def vlanformat():
		global vlanlength, vlanexname
		if vlanT == 'custom':
				vlanexname = ''
				vlanlength = str(jvlantval)
		elif vlanT == 'standard':
			vlanexname = int(rVLAN)
			if rVLANlength == 1:
				vlanlength = 'VLAN000'
			elif rVLANlength == 2:	
				vlanlength = 'VLAN00'
			elif rVLANlength == 3:
				vlanlength = 'VLAN0'
			elif rVLANlength == 4:
				vlanlength = 'VLAN'	
	def addlinetype():
		if allowreq == 'access':
			if confstate == 'preview':
				print('set interface ' + str(ifname) + ' family ethernet-switching port-type access')
			elif confstate == 'execute':
				remote_connection.send('set interface ' + str(ifname) + ' family ethernet-switching port-type access' + '\n')
		elif allowreq == 'trunk':
			if confstate == 'preview':
				print('set interface ' + str(ifname) + ' family ethernet-switching port-type trunk')
			elif confstate == 'execute':
				remote_connection.send('set interface ' + str(ifname) + ' family ethernet-switching port-type trunk' + '\n')
	def addlineint():
		if confstate == 'preview':
			print('set interface ' + str(ifname) + ' family ethernet-switching vlan members ' + str(vlanlength) + str(vlanexname))
		elif confstate == 'execute':
			remote_connection.send('set interface ' + str(ifname) + ' family ethernet-switching vlan members ' + str(vlanlength) +  str(vlanexname) + '\n')
	def addlinevlan():
		if confstate == 'preview':
			print('set vlans ' + str(vlanlength) + str(vlanexname) + ' vlan-id ' + str(rVLAN) + ' description ' + '"' + str(newVLAND) + '"')
		elif confstate == 'execute':
			remote_connection.send('set vlans ' + str(vlanlength) + str(vlanexname) + ' vlan-id ' + str(rVLAN) + ' description ' + '"' + str(newVLAND) + '"' + '\n')
	def addrangevlan():
		if confstate == 'preview':
			for eachvlan in range(vx, vy+1):
				print('set vlans ' + str(rangelength) + str(eachvlan) + ' vlan-id ' + str(eachvlan) + ' description ' + '"' + str(newVLAND) + '_' + str(eachvlan) + '"')
		elif confstate == 'execute':
			for eachvlan in range(vx, vy+1):
				remote_connection.send('set vlans ' + str(rangelength) + str(eachvlan) + ' vlan-id ' + str(eachvlan) + ' description ' + '"' + str(newVLAND) + '_' + str(eachvlan)+'"' + '\n')
	def dellineint():
		if confstate == 'preview':
			print('delete interface ' + str(ifname) + ' family ethernet-switching vlan members ' + str(vlanlength) + str(vlanexname))
		elif confstate == 'execute':
			remote_connection.send('delete interface ' + str(ifname) + ' family ethernet-switching vlan members ' + str(vlanlength) + + str(vlanexname) + '\n')
	def dellineintany():
		if confstate == 'preview':
			print('delete interface ' + str(ifname) + ' family ethernet-switching vlan members ')
		elif confstate == 'execute':
			remote_connection.send('delete interface ' + str(ifname) + ' family ethernet-switching vlan members\n')
	def dellinevlan():
		if confstate == 'preview':
			print('delete vlans ' + str(vlanlength) + str(vlanexname))
		elif confstate == 'execute':
			remote_connection.send('delete vlans ' + str(vlanlength) + str(vlanexname) + '\n')
	def dellinevlanonce():
		if confstate == 'preview':
			if vlanT == 'standard':
				for eachpipe in allpipescombinedlist:
					if eachpipe == '':
						pass
					else:
						print('delete interface ' + str(eachpipe) + ' family ethernet-switching vlan members ' + str(vlanlength) + str(vlanexname))
				print('delete vlans ' + str(vlanlength) + str(vlanexname))
			elif vlanT == 'custom':
				for eachpipe in allpipescombinedlist:
					if eachpipe == '':
						pass
					else:
						print('delete interface ' + str(eachpipe) + ' family ethernet-switching vlan members ' + str(vlanlength)+ str(vlanexname))
				print('delete vlans ' + str(vlanlength))
		elif confstate == 'execute':
			if vlanT == 'standard':
				for eachpipe in allpipescombinedlist:
					if eachpipe == '':
						pass
					else:
						remote_connection.send('delete interface ' + str(eachpipe) + ' family ethernet-switching vlan members ' + str(vlanlength) + str(vlanexname) + '\n')
				remote_connection.send('delete vlans ' + str(vlanlength) + str(vlanexname) + '\n')
			elif vlanT == 'custom':
				for eachpipe in allpipescombinedlist:
					if eachpipe == '':
						pass
					else:
						remote_connection.send('delete interface ' + str(eachpipe) + ' family ethernet-switching vlan members ' + str(vlanlength) + str(vlanexname) + '\n')
				remote_connection.send('delete vlans ' + str(vlanlength) + '\n')
	if confstate == 'preview':
		print('The following configuration will be applied upon your approval !')
		print('#'*105)
		print('edit')
		JuniperCoreConf()
		print('commit')
		print('#'*105)
		print("Proceed? Type 'Y' to approve or any key to abort.")
	elif confstate == 'execute':
		initSSHCall()
		remote_connection.send('edit\n')
		JuniperCoreConf()
		remote_connection.send('show|compare\n')
		remote_connection.send('commit and-quit\n')
		time.sleep(5)
		output_script_2 = remote_connection.recv(65535)
		print('#'*105)
		print("Configuration Report:")
		print('#'*105)
		print ((output_script_2).decode('ascii'))
		print('#'*105)
		ssh_client.close()
		returnBack()
def DisplayScreen(): # Main Menu options.
	try:
		print('='*105)
		print(" ")
		print("           			Welcome to AutoVLAN 1.0                 ")
		print(" ")
		print('='*105)
		print('')
		print('Please specify an option from the below list:')
		print('')
		print('0] Instructions Manual')
		print('1] Add a single VLAN for the first time.')
		print('2] Add a desired VLAN range for the first time.')
		print('3] Free VLAN(s) off production.')
		print('4] Allow a single VLAN to a trunk/access interface.')
		print('5] Remove a single VLAN from a trunk/access interface.')
		print('')
		print("To exit the program anytime, press 'CTRL + C'.")
		print('')
		print('Your choice is: ')
		request_A=input()
		if request_A == '0':
			print(str(instruma))
			input('Press any key to return to the main screen..')
			DisplayScreen()
		elif request_A == '1':
			Option1()
		elif request_A == '2':
			Option2()
		elif request_A == '3':
			Option3()
		elif request_A == '4':
			Option4()
		elif request_A == '5':
			Option5()
		else:
			print('Wrong selection, please select a valid option from the below list!')
			print('='*66)
			DisplayScreen()
	except KeyboardInterrupt:
		print(" ")
		print("Program Terminated, Goodbye ! ._. ")
		exit()	
def WelcomeScreen(): # Welcome Authentication.
	try:
		print('='*105)
		print("Please enter your credentials in order to proceed further, or press 'CTRL + C' to exit program: ")
		print('='*105)
		userAuth()
	except KeyboardInterrupt:
		print(" ")
		print("Program Terminated, Goodbye ! ._. ")
		exit()	
def singleVLANCheck(): #Checking the input of a single VLAN from user.
	global vlanver, rVLAN, rVLANlength, newVLAND, vlanstate
	vlanintegerloop = False
	while not vlanintegerloop:
		if vlanstate == 'new':
			try:
				newVLAND = str(input("Please enter desired VLAN Description: "))
				rVLAN = int(input("Please enter desired VLAN-ID to be added: "))
				break
			except ValueError:
				print("This is an invalid VLAN input!")
		elif vlanstate == 'cur':
			try:
				rVLAN = int(input("Please enter desired VLAN-ID to be allowed: "))
				break
			except ValueError:
				print("This is an invalid VLAN input!")
		elif vlanstate == 'old':
			try:
				rVLAN = int(input("Please enter desired VLAN-ID to be removed: "))
				break
			except ValueError:
				print("This is an invalid VLAN input!")
	vlanintegerloop=True
	if int(rVLAN)>=4093:
		print("VLAN-ID is Invalid!")
		vlanver = 'KO'
	elif int(rVLAN) in (0,1,1002,1003,1004,1005):
		print("You're not authorized to add or modify this VLAN!")
		vlanver = 'KO'
	else:
		rVLANlength = len(str(rVLAN))
		vlanver = 'OK'
def rangeVLANCheck(): #Checking the input of a VLAN range from user.
	global vx, vy, newVLAND, vlanver
	vxloop = False
	newVLAND = input("Enter a unified ranged Desciption for the desired range: ")
	while not vxloop:
		vlanxintegerloop = False
		while not vlanxintegerloop:
			try:
				vx = int(input("Please enter the desired start range: "))
				break
			except ValueError:
				print("This is an invalid VLAN input!")
				vlanver = 'KO'
		vlanxintegerloop=True
		if int(vx)>=4093:
			print("VLAN start range is Invalid!")
			vlanver = 'KO'
		elif int(vx) in (0,1,1002,1003,1004,1005):
			print("VLAN end range is Reserved!")
			vlanver = 'KO'
		else:
			vxloop = True
			vyloop = False
			while not vyloop:
				vlanyintegerloop = False
				while not vlanyintegerloop:
					try:
						vy = int(input("Please enter the desired end range: "))
						break
					except ValueError:
						print("This is an invalid VLAN input!")
						vlanver = 'KO'
				vlanyintegerloop=True
				vlanrange = list(range(vx, vy+1))
				restrange = list([1,1002,1003,1004,1005,4093,4094,4095])
				overlap = any(elem in restrange for elem in vlanrange)
				if overlap:
					print('Desired VLAN range contains invalid VLANs!')
					vlanver = 'KO'
				elif int(vx) > int(vy):
					print("Invalid Range!")
					vlanver = 'KO'
				elif int(vy - vx) > 30:
					print('Only 30 VLANs are allowed as MAX per one configuration request.')
					vlanver = 'KO'
				else:
					vlanver = 'OK'
					vyloop = True
def initSSHCall(): # Call definded host using SSH paramiko library.
	global remote_connection, ssh_client
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=ip_address,username=username,password=password)
	remote_connection = ssh_client.invoke_shell()
def returnBack(): # Return to main screen.
	shiftchoice = input("Press 'm' to return to main screen, or 'CTRL + C' to quit program, or just any key to resume the current option : ")
	if shiftchoice in ['m', 'M']:
		DisplayScreen()
	else:
		print('Resuming..')
def userAuth(): # User Authentication.
	global username, password
	username = input("Username: ")
	password = getpass.getpass()
	DisplayScreen()
def switchVendor(): # Determining switch vendor.
	global vendortype, ip_address
	ip_address = input("Please enter the desired switch IP address: ")
	vendortype = 'n'
	ipbasecheck = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
	if (re.search(ipbasecheck, ip_address)):	
		try:	
			print('Swich IP address received, Determining Vendor..')
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(hostname=ip_address,username=username,password=password)
			remote_connection = ssh_client.invoke_shell()
			remote_connection.send('show version\n' + '  ')
			time.sleep(2)
			ssh_client.close()
			output_script2 = remote_connection.recv(65532)
			output2 = str((output_script2).decode('ascii'))
			if "Cisco" in output2:
				print("The " + str(ip_address) + " is a Cisco Device")
				vendortype = 'c'
			elif "JUNOS" in output2:
				print("The " + str(ip_address) + " is a Juniper Device")
				vendortype = 'j'
			else:
				print("The " + str(ip_address) + " is neither Cisco nor Juniper Device.")
				vendortype = 'n'
				switchVendor()
		except KeyboardInterrupt:
			print(" ")
			print("Program Terminated, Goodbye ! ._. ")
			exit()
		except paramiko.ssh_exception.AuthenticationException:
			print(" ")
			print("Authentication failed, please try again!")
			userAuth()
		except:
			print(" Failed to connect to the requested Switch, please check your network settings and try again!")
			switchVendor()			
	else:
		print('The Switch IP address that you have entered is invalid!')
		switchVendor()
# Instructions #
instruma = """
AutoVLAN Instructions Manual:
=============================
General Instructions:
# Effectively from the 6th of March 2021, the script name has been changed from "VLAN Dialogue" to "AutoVLAN".
# The script is based on Python 3 or later versions, aside from other low-level libraries, which are Paramiko*, re, time, and getpass [Paramiko* must be installed first].
# The core function of this script is built over Paramiko* SSH library. So in order to work, a direct SSH connection between the script location and the switch destination is required. This vesrion of the script is designed to run anywhere remotely [client-to-host fashion].
# This version of the script uses management IP addresses for switches in order to have reachability and execute changes.
# When adding VLANs, it's required from you to evaluate this VLAN first on the production network. If this VLAN already exists, it can't be overwritten by the script as a safety mechanism. Only non existent VLAN will be created on the production network.
# When adding a VLAN range, you must first evaluate your input in terms of allowed VLANs that could be used and restricted VLANs that are specific for FDDI/Token-Ring use. As an enforcement policy for standardization, VLAN ranges are created for both Juniper and Cisco with the same fashion [Max. 30 VLANs per configuration request] hence Juniper aggregated VLAN range style [along custom-named VLANs] are NOT allowed to be created by this script. However, the script allows you to delete them if requested.

Cisco Devices Instructions:
# The script will evaluate the privilege level according to the given credentials. In order to run the script effectively, at least an exec privilege level with a complete support to VLANs and interfaces commands set should be granted. If only user privilege is granted, the script will notify you.

Juniper Devices Instructions:
# The script will differentiate between two VLAN modes, custom-naming and standard-naming** modes [e.g. for standard-naming**: VLAN names for IDs 57 and 103 are VLAN0057 and VLAN0103]. This script will only allow the creation of the Juniper standard-naming VLAN(s). If you want to create Juniper VLAN(s) [Option 1 or 2] on the switch database, while this VLAN already have a custom-name that doesn't comply with the Juniper standard-naming defined, an informing message will be popped to the user screen elaborating that this VLAN already exists. However, if you tried to allow an already existing custom-named VLAN ID or Range to a switchport with Option 4, a question field will pop up instead, which ensures that the custom-name you provide MUST match the same one within production. This approach is followed as an extra layer of satefy check. The same scenario should occur if you used Option 3 or 5 to delete/remove an already existing custom-named VLAN ID/Range.

Thanks for your understanding.
"""
# Main Functions #
def Option1(): # Task 1 Function.
	global optionstate, vlanstate, confstate, vlanT, jvlantname
	optionstate = 'option_1'
	switchVendor()
	vlanstate = 'new'
	if vendortype == 'c':
		print("Please enter VLAN parameters: ")
		#Cisco Add VLAN
		cvlanloop = False
		while not cvlanloop:
			singleVLANCheck()
			if vlanver == 'OK':
				print("Checking the requested VLAN for this specific switch...")
				print('#'*80)
				initSSHCall()
				remote_connection.send('show vlan id ' + str(rVLAN) + '\n')
				time.sleep(3)
				output_script = remote_connection.recv(65535)
				print('#'*80)
				ssh_client.close()
				if ">" in str(output_script):
					print("Couldn't gain the required exec privilege level to perform such action. Please revise your credentials and/or check switch available vty lines and try again.")
					returnBack()
				elif "not found in current VLAN database" in str(output_script):
					confstate = 'preview'
					CiscoConfig()
					Approval=input()
					if Approval in ['Y', 'y']:
						confstate = 'execute'
						CiscoConfig()
					else:
						print("Flushing parameters..")
						returnBack()
				else:
					print('VLAN already existed, please try again with a valid input!')
					print('#'*80)
					returnBack()
			else:
				returnBack()
		cvlanloop = True
	elif vendortype == 'j':
		print("Please enter VLAN parameters: ")
		#Juniper Add VLAN
		jvlanloop = False
		while not jvlanloop:
			singleVLANCheck()
			if vlanver == 'OK':
				print("Checking the requested VLAN for this specific switch...")
				print('#'*80)
				initSSHCall()
				remote_connection.send('show vlans ' + str(rVLAN) + '\n')
				time.sleep(3)
				output_script = remote_connection.recv(65535)
				print('#'*80)
				ssh_client.close()
				if "error: vlan with tag" in str(output_script):
					jvlantname = False
					confstate = 'preview'
					vlanT = 'standard'
					JuniperConfig()
					Approval=input()
					if Approval in ['Y', 'y']:
						confstate = 'execute'
						JuniperConfig()						
					else:
						print("Flushing parameters..")
						returnBack()
				else:   
					print('VLAN already existed, please try again with a valid input!')
					print('#'*80)
					returnBack()
			else:
				returnBack()
		jvlanloop = True
def Option2(): # Task 2 Function.
	global optionstate, vx, vy, vlanstate, confstate, vlanT, jvlantname
	optionstate = 'option_2'
	switchVendor()
	vendorloop = False
	while not vendorloop:
		if vendortype == 'c':
			print("Please enter VLANs range parameters: ")
			# Cisco Add Range
			cvlanloop = False
			while not cvlanloop:
				rangeVLANCheck()
				if vlanver == 'OK':
					print("Checking the requested range for this specific switch...")
					print('#'*80)
					initSSHCall()
					for n in range (vx, vy+1):
						remote_connection.send('show vlan id ' + str(n) + '\n')
					time.sleep(5)
					output_script = remote_connection.recv(65535)
					print('#'*80)
					ssh_client.close()
					if ">" in str(output_script):
						print("Couldn't gain the required exec privilege level to perform such action. Please revise your credentials and/or check switch available vty lines and try again.")
					elif "active" in str(output_script):
						print('One or more VLAN(s) already existed, please check the return output and try again with a valid input!')
						print('#'*80)
						print((output_script).decode('ascii'))
						print('#'*80)
						returnBack()
					else:
						confstate = 'preview'
						CiscoConfig()
						Approval=input()
						if Approval in ['Y', 'y']:
							confstate = 'execute'
							CiscoConfig()
						else:
							print("Flushing parameters..")
							returnBack()
				else:
					returnBack()
			cvlanloop = True
		elif vendortype == 'j':
			print("Please enter VLANs range parameters: ")
			# Juniper Add Range
			jvlanloop = False
			while not jvlanloop:
				rangeVLANCheck()
				if vlanver == 'OK':
					print("Checking the requested range for this specific switch...")
					print('#'*100)
					initSSHCall()
					for n in range (vx, vy+1):
						remote_connection.send('show vlans ' + str(n) + '\n')
					time.sleep(5)
					output_script = remote_connection.recv(65535)
					print('#'*100)
					ssh_client.close()
					if "Interfaces" in str(output_script):
						print('One or more VLAN(s) already existed, please check the below output and try again with a valid input: ')
						print('#'*100)
						print((output_script).decode('ascii'))
						print('#'*100)
						returnBack()
					else:
						jvlantname = False
						vlanT = 'standard'
						confstate = 'preview'
						JuniperConfig()  
						Approval=input()
						if Approval in ['Y', 'y']:
							confstate = 'execute'
							JuniperConfig()
						else:
							print("Flushing parameters..")
							returnBack()
				else:
					returnBack()
			jvlanloop = True
	vendorloop = True
def Option3(): # Task 3 Function.
	global vlanstate, confstate, vlanT, jvlantame, jvlantval, optionstate, allpipespurelist, allpipescombinedlist, combinedval, bad_chars
	optionstate = 'option_3'
	switchVendor()
	vlanstate = 'old'
	vendorloop = False
	while not vendorloop:
		if vendortype == 'c':
			print("Please enter VLAN parameters: ")
			#Cisco Remove VLAN
			cvlanloop = False
			while not cvlanloop:
				singleVLANCheck()
				if vlanver == 'OK':
					print("Checking the requested VLAN for this specific switch...")
					print('#'*80)
					initSSHCall()
					remote_connection.send('show vlan id ' + str(rVLAN) + '\n')
					time.sleep(5)
					output_script = remote_connection.recv(65535)
					output_readable = (output_script.decode('ascii'))
					output_str = str(output_readable)
					allpipes = [re.findall("F?a?G?i?[0-9]+\/[0-9]+\/?[0-9]?[0-9]?", output_str)]
					allpipespure = str(allpipes)
					bad_chars = ["'", "[", "]", "," , ""]
					for imps in bad_chars:
						allpipespure = allpipespure.replace(imps, '')
					allpipespurelist = list(allpipespure.split(" "))
					ssh_client.close()
					print('#'*80)
					initSSHCall()
					for eachpipe in allpipespurelist:
						if eachpipe == '':
							pass
						else:
							remote_connection.send('show running-config interface ' + str(eachpipe) + '\n')
					time.sleep(3)
					ssh_client.close()
					pipeoutput = remote_connection.recv(65535)
					pipe_readable = (pipeoutput.decode('ascii'))
					pipelist = list(pipe_readable.split('\n'))
					pipelist = ([s.strip('\r') for s in pipelist])
					wantedchar = [' switchport mode trunk', ' switchport mode access', ' switchport mode dot1q-tunnel' ]
					pipeval = [x for x in pipelist if x in wantedchar]
					combinedval = ([a+b for a, b in zip(allpipespurelist, pipeval)])
					if ">" in str(output_script):
						print("Couldn't gain the required exec privilege level to perform such action. Please revise your credentials and/or check switch available vty lines and try again.")
						returnBack()
					elif "not found in current VLAN database" in str(output_script):
						print('Could not find that specific VLAN, please try again with a valid input!')
						print('#'*80)
						returnBack()
					else :
						confstate = 'preview'
						CiscoConfig()
						Approval=input()
						if Approval in ['Y', 'y']:
							confstate = 'execute'
							CiscoConfig()
						else:
							print("Flushing parameters..")
							returnBack()
				else:
					returnBack()
			cvlanloop = True
		elif vendortype == 'j':
			print("Please enter VLAN parameters: ")
			#Juniper Remove VLAN
			jvlanloop = False
			while not jvlanloop:
				singleVLANCheck()
				if vlanver == 'OK':
					jvlantval = input("If this VLAN name/range already have a custom name which doesn't comply to the naming standard, please specify (case sensitive). Leave this field empty ONLY if otherwise: ")
					if re.match('[^0-9a-zA-Z]+', jvlantval):
						print('Invalid custom VLAN name!')
					elif jvlantval == '':
						print('No custom VLAN name received, entering standard name mode..')
						jvlantname = False
					else:
						jvlantname = True
						print('Custom VLAN name received, entering custom name mode..')
					print("Checking the requested VLAN for this specific switch...")
					print('#'*80)
					print('#'*80)
					initSSHCall()
					remote_connection.send('show vlans ' + str(rVLAN) + '\n')
					time.sleep(3)
					output_script = remote_connection.recv(65535)
					output_readable = (output_script.decode('ascii'))
					output_str = str(output_readable)
					alllagpipes = [re.findall("\De-[0-9]+\/[0-9]+\/[0-9]+\.[0-9]+", output_str)]
					allsinglepipes = [re.findall("ae[0-9]+\.[0-9]+", output_str)]
					allpipescombined = str(alllagpipes+allsinglepipes)
					bad_chars = ["'", "[", "]", "," , ""]
					for imps in bad_chars:
						allpipescombined = allpipescombined.replace(imps, '')
					allpipescombinedlist = list(allpipescombined.split(" "))
					print('#'*80)
					ssh_client.close()
					initSSHCall()
					remote_connection.send('show version\n')
					time.sleep(3)
					pri_script = remote_connection.recv(65534)
					ssh_client.close()
					if "error: vlan with tag" in str(output_script):
						print('Could not find that specific VLAN within the switch database, please try again with a valid input!')
						print('#'*80)
						returnBack()
					elif jvlantname == True:
						vlanT = 'custom'
						if not str(jvlantval + ' ') in str(output_script):
							print('Could not match custom VLAN name within the switch database, please try again with a valid input!')
							print('#'*80)
							returnBack()
						elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script):
							RVLANJ = input('The custom VLAN name entered belongs to a VLAN range, and not a single VLAN, do you want to remove this range completely? Press "Y" to continue or just any key to abort: ')
							if RVLANJ in ['Y', 'y']:
								print('Permission granted to delete the specifed VLAN range..')
								confstate = 'preview'
								JuniperConfig()
								Approval=input()
								if Approval in ['Y', 'y']:
									confstate = 'execute'
									JuniperConfig()
								else:
									returnBack()
							else:
								print("Flushing parameters..")
								returnBack()
						else:
							print('Custom VLAN name Identified, preparing deletion template..')
							confstate = 'preview'
							JuniperConfig()
							Approval=input()
							if Approval in ['Y', 'y']:
								confstate = 'execute'
								JuniperConfig()
							else:
								returnBack()
					elif jvlantname == False:
						oldVLANstr = str(rVLAN)
						vlanT = 'standard'
						if len(oldVLANstr) == 1 and str("VLAN000" + str(rVLAN)) not in str(output_script):
							print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
							print('#'*80)
							returnBack()
						elif len(oldVLANstr) == 2 and str("VLAN00" + str(rVLAN)) not in str(output_script):
							print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
							print('#'*80)
							returnBack()
						elif len(oldVLANstr) == 3 and str("VLAN0" + str(rVLAN)) not in str(output_script):
							print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
							print('#'*80)
							returnBack()
						elif len(oldVLANstr) == 4 and str("VLAN" + str(rVLAN)) not in str(output_script):
							print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
							print('#'*80)
							returnBack()
						else:
							confstate = 'preview'
							JuniperConfig()
							Approval=input()
							if Approval in ['Y', 'y']:
								confstate = 'execute'
								JuniperConfig()
							else:
								returnBack()
				else:		
					returnBack()
			jvlanloop = True
	vendorloop = True
def Option4(): # Task 4 Function.
	global ifname, vlanstate, optionstate, vlanT, allowstate, allowreq, confstate, jvlantval, newVLAND
	optionstate = 'option_4'
	vlanstate = 'cur'
	switchVendor()
	vendorloop = False
	while not vendorloop:
		if vendortype == 'c':
			print("Please enter VLAN and interface parameters: ")
			#Cisco Allow VLAN to Interface 
			cvlanloop = False
			while not cvlanloop:
				ifname = str(input("Please enter desired Cisco hardware interface name (case sensitive): "))
				if not re.match("^\w+(-\w+)?\d+(([\/:]\d+)+(\.\d+)?)?$", ifname):
					print('This is not a valid Cisco interface name!')
				else:
					singleVLANCheck()
					if vlanver == 'OK':
						print("Checking the requested Interface and VLAN for this specific switch...")
						print('#'*80)
						initSSHCall()
						remote_connection.send('show vlan id ' + str(rVLAN) + '\n')
						time.sleep(3)
						ssh_client.close()
						print('#'*80)
						output_script_A = remote_connection.recv(65533)
						initSSHCall()
						remote_connection.send('show running-config interface ' + str(ifname) + '\n')
						time.sleep(3)
						output_script_B = remote_connection.recv(65532)
						print('#'*80)
						ssh_client.close()
						if ">" in str(output_script_A):
							print("Couldn't gain the required exec privilege level to perform such action. Please revise your credentials and/or check switch available vty lines and try again.")
							returnBack()
						elif "Invalid input detected" in str(output_script_B):
							print("Couldn't find this interface name within the switch hardware inventory. Please check your input and try again.")
							returnBack()
						elif "not found in current VLAN database" in str(output_script_A) and "switchport mode trunk" in str(output_script_B):
							if 'switchport trunk allowed vlan' in str(output_script_B) and str(rVLAN) in str(output_script_B):
								print('This VLAN is already allowed on that interface!')
								returnBack()
							else:
								CVLANT = input("Couldn't find that specified VLAN within the switch database, would you like to create it ? Type 'Y' to procees, or just any key to abort: ")
								vlanstate = 'new'
								if CVLANT in ['y', 'Y']:
									newVLAND = input('Please enter the desired VLAN Description: ')
									CVLANQ1 = input('Preparing VLAN template, for Access configuration type "A", for Trunk configuration type "T" or just type any other key to abort: ')
									if CVLANQ1 in ['a', 'A']:
										print('This will override current interface Layer 2 configuration from Trunk to Acces port! ')
										allowstate = "novlan-trunk"
										allowreq = "access"
										confstate = 'preview'
										CiscoConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											CiscoConfig()
											vlanstate = 'cur'
										else:
											print('Flushing Configuration..')
											returnBack()
											vlanstate = 'cur'
									elif CVLANQ1 in ['t', 'T']:
										allowstate = "novlan-trunk"
										allowreq = "trunk"
										confstate = 'preview'
										CiscoConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											CiscoConfig()
											vlanstate = 'cur'
										else:
											print('Flushing Configuration..')
											vlanstate = 'cur'
											returnBack()
									else:
										print('Flushing configuration..')
										vlanstate = 'cur'
										returnBack()
								else:
									print('Flushing parameters..')
									vlanstate = 'cur'
									returnBack()
						elif "not found in current VLAN database" in str(output_script_A) and ("switchport mode access" in str(output_script_B) or "switchport mode dot1q-tunnel"in str(output_script_B)):
							if str(rVLAN) in str(output_script_B):
								print('This VLAN is already allowed on that interface!')
								returnBack()
							else:
								CVLANA = input("Couldn't find that specified VLAN within the switch database, would you like to create it ? Type 'Y' to procees, or just any key to abort: ")
								if CVLANA in ['y', 'Y']:
									newVLAND = input('Please enter the desired VLAN Description: ')
									CVLANQ1 = input('Preparing VLAN template, for Access configuration type "A", for Trunk configuration type "T" or just type any other key to abort: ')
									vlanstate = 'new'
									if CVLANQ1 in ['a', 'A']:
										allowstate = "novlan-access"
										allowreq = "access"
										confstate = 'preview'
										CiscoConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											CiscoConfig()
											vlanstate = 'cur'
										else:
											print('Flushing Configuration..')
											vlanstate = 'cur'
											returnBack()
									elif CVLANQ1 in ['t', 'T']:
										print('This will override current interface Layer 2 configuration from Access to Trunk port! ')
										allowstate = "novlan-access"
										allowreq = "trunk"
										confstate = 'preview'
										CiscoConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											CiscoConfig()
											vlanstate = 'cur'
										else:
											print('Flushing Configuration..')
											vlanstate = 'cur'
											returnBack()
									else:
										print('Flushing configuration..')
										vlanstate = 'cur'
										returnBack()
								else:
									print('Flushing parameters..')
									vlanstate = 'cur'
									returnBack()
						elif "not found in current VLAN database" in str(output_script_A):
							CVLANT = input("Couldn't find that specified VLAN within the switch database, would you like to create it ? Type 'Y' to procees, or just any key to abort: ")
							if CVLANT in ['y', 'Y']:
								newVLAND = input('Please enter the desired VLAN Description: ')
								CVLANQ1 = input('Preparing VLAN template, for Access configuration type "A", for Trunk configuration type "T" or just type any other key to abort: ')
								vlanstate = 'new'
								if CVLANQ1 in ['a', 'A']:
									print('This will override current interface configuration! ')
									allowstate = "novlan-blank"
									allowreq = "access"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
										vlanstate = 'cur'
									else:
										print('Flushing Configuration..')
										vlanstate = 'cur'
										returnBack()
								elif CVLANQ1 in ['t', 'T']:
									print('This will override current interface configuration! ')
									allowstate = "novlan-blank"
									allowreq = "trunk"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
										vlanstate = 'cur'
									else:
										print('Flushing Configuration..')
										vlanstate = 'cur'
										returnBack()
								else:
									print('Flushing configuration..')
									vlanstate = 'cur'
									returnBack()
							else:
								print('Flushing parameters..')
								vlanstate = 'cur'
								returnBack()
						elif str(rVLAN) in str(output_script_A) and "switchport mode trunk" in str(output_script_B):
							if 'switchport trunk allowed vlan' in str(output_script_B) and str(rVLAN) in str(output_script_B):
								print('This VLAN is already allowed on that interface!')
								returnBack()
							else:
								CVLANQ1 = input("VLAN found within the switch database, type 'A' to configure it as Access or to type 'T' configure it as Trunk, or just any key to abort: ")
								if CVLANQ1 in ['a', 'A']:
									print('This will override current interface Layer 2 configuration from Trunk to Access port! ')
									allowstate = "vlan-trunk"
									allowreq = "access"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
									else:
										print('Flushing Configuration..')
										returnBack()
								elif CVLANQ1 in ['t', 'T']:
									allowstate = "vlan-trunk"
									allowreq = "trunk"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
									else:
										print('Flushing Configuration..')
										returnBack()
								else:
									print('Flushing configuration..')
									returnBack()
						elif str(rVLAN) in str(output_script_A) and ("switchport mode access" in str(output_script_B) or "switchport mode dot1q-tunnel"in str(output_script_B)):
							if str(rVLAN) in str(output_script_B):
								print('This VLAN is already allowed on that interface!')
								returnBack()
							else:
								CVLANQ1 = input("VLAN found within the switch database, type 'A' to configure it as Access or 'T' to configure it as Trunk. Or just any key to abort: ")
								if CVLANQ1 in ['a', 'A']:
									allowstate = "vlan-access"
									allowreq = "access"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
									else:
										print('Flushing Configuration..')
										returnBack()
								elif CVLANQ1 in ['t', 'T']:
									print('This will override current interface Layer 2 configuration from Access to Trunk port! ')
									allowstate = "novlan-access"
									allowreq = "trunk"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
									else:
										print('Flushing Configuration..')
										returnBack()
								else:
									print('Flushing configuration..')
									returnBack()
						elif str(rVLAN) in str(output_script_A) and "ip address" in str(output_script_B):
							CVLANQ1 = input("Caution: This will override current L3 configuration! VLAN found in switch database, type 'A' to configure it as Access or type 'T' to configure it as Trunk, or just any key to abort: ")
							if CVLANQ1 in ['a', 'A']:
								allowstate = "vlan-blank"
								allowreq = "access"
								confstate = 'preview'
								CiscoConfig()
								Approval=input()
								if Approval in ['Y', 'y']:
									confstate = 'execute'
									CiscoConfig()
								else:
									print("Flushing Configuration..")
									returnBack()
							elif CVLANQ1 in ['t', 'T']:
								allowstate = "vlan-blank"
								allowreq = "trunk"
								confstate = 'preview'
								CiscoConfig()
								Approval=input()
								if Approval in ['Y', 'y']:
									confstate = 'execute'
									CiscoConfig()
								else:
									print("Flushing Configuration..")
									returnBack()
							else:
								print('Flushing configuration..')
								returnBack()
						elif str(rVLAN) in str(output_script_A):
							CVLANQ1 = input("VLAN found in switch database, type 'A' to configure it as Access or type 'T' to configure it as Trunk, or just any key to abort: ")
							if CVLANQ1 in ['a', 'A']:
								allowstate = "vlan-blank"
								allowreq = "access"
								confstate = 'preview'
								CiscoConfig()
								Approval=input()
								if Approval in ['Y', 'y']:
									confstate = 'execute'
									CiscoConfig()
								else:
									print("Flushing Configuration..")
									returnBack()
							elif CVLANQ1 in ['t', 'T']:
								allowstate = "vlan-blank"
								allowreq = "trunk"
								confstate = 'preview'
								CiscoConfig()
								Approval=input()
								if Approval in ['Y', 'y']:
									confstate = 'execute'
									CiscoConfig()
								else:
									print("Flushing Configuration..")
									returnBack()
							else:
								print('Flushing configuration..')
								returnBack()
					else:
						returnBack()
			cvlanloop = True
		elif vendortype == 'j':
			print("Please enter VLAN and interface parameters: ")
			#Juniper Allow VLAN to Interface 
			jvlanloop = False
			while not jvlanloop:
				ifname = str(input("Please enter the desired Juniper hardware interface name, including unit (case sensitive): "))
				if not any([re.match("^\De-[0-9]+\/[0-9]+\/[0-9]+\.[0-9]+$", ifname), re.match("^ae[0-9]+\.[0-9]+$", ifname)]):
					print('This is not a valid Juniper interface name!')
				else:
					singleVLANCheck()
					if vlanver == 'OK':
						jvlantval = input("If this VLAN name/range already have a custom name which doesn't comply to the naming standard, please specify (case sensitive). Leave this field empty ONLY if otherwise: ")
						if re.match('[^0-9a-zA-Z]+', jvlantval):
							print('Invalid custom VLAN name!')
						elif jvlantval == '':
							print('No custom VLAN name entered, entering standard name mode..')
							jvlantame = False
						else:
							jvlantame = True
							print('Entering custom name mode..')
						print("Checking the requested Interface and VLAN for this specific switch...")
						print('#'*80)
						initSSHCall()
						remote_connection.send('show vlans ' + str(rVLAN) + '\n')
						time.sleep(5)
						output_script_A = remote_connection.recv(65535)
						ssh_client.close()
						print('#'*80)
						initSSHCall()									
						remote_connection.send('show configuration interfaces ' + str(ifname) + '\n')
						remote_connection.send('show interfaces ' + str(ifname) + '\n')
						time.sleep(5)
						output_script_B = remote_connection.recv(65534)
						print('#'*80)
						ssh_client.close()
						newVLANstr = str(rVLAN)
						if str("error: device") in str(output_script_B) or str("error: interface") in str(output_script_B):
							print("Couldn't find this interface name within the switch hardware inventory. Please check your input and try again.")
							returnBack()
						elif "error: vlan with tag" in str(output_script_A) and "port-mode trunk;" in str(output_script_B):
							JVLANT = input("Couldn't find that specified VLAN within switch database, would you like to create it? Type 'Y' to procees, or just any key to abort: ")
							if JVLANT in ['y', 'Y']:
								JVLANQ1 = input('For Access configuration type "A", for Trunk configuration type "T" or just type any other key to abort: ')
								if JVLANQ1 in ['a', 'A']:
									newVLAND = input('Enter new VLAN Desciption: ')
									print('This will override current interface Layer 2 configuration from Trunk to Access ! ')
									allowstate = 'novlan-trunk'
									allowreq = 'access'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								elif JVLANQ1 in ['t', 'T']:
									newVLAND = input('Enter new VLAN Desciption: ')
									allowstate = 'novlan-trunk'
									allowreq = 'trunk'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print('Flushing configuration..')
									returnBack()
							else:
								print('Flushing parameters..')
								returnBack()
						elif "error: vlan with tag" in str(output_script_A) and "port-mode access;" in str(output_script_B):
							JVLANA = input("Couldn't find that specified VLAN within switch database, would you like to create it? Type 'Y' to procees, or just any key to abort: ")
							if JVLANA in ['y', 'Y']:
								JVLANQ1 = input("For access mode type 'A' , and for trunk type 'T' or just any key to abort:  ")
								if JVLANQ1 in ['a', 'A']:
									newVLAND = input('Enter new VLAN Desciption: ')
									allowstate = 'novlan-access'
									allowreq = 'access'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								elif JVLANQ1 in ['t', 'T']:
									newVLAND = input('Enter new VLAN Desciption: ')
									print('This will override current interface Layer 2 configuration from Access to Trunk !')
									allowstate = 'novlan-access'
									allowreq = 'trunk'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print('Flushing parameters..')
									returnBack()
						elif str(rVLAN) in str(output_script_A) and "port-mode trunk;" in str(output_script_B):
							if jvlantame == True:
								if str(jvlantval + ' ') in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This Custom-named VLAN is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This VLAN range is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str(jvlantval + ' ') not in str(output_script_A):
									print('Could not match custom VLAN name within the switch database, please try again with a valid input!')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A):
									print('Custom VLAN range Identified, preparing allowance template..')
									allowstate = 'vlan-trunk'
									allowreq = 'trunk'
									vlanT = 'custom'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'preview'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print('Custom VLAN name Identified, preparing allowance template..')
									print('#'*80)
									JVLANQ1 = input("VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort: ")
									if JVLANQ1 in ['a', 'A']:
										print('This will override current interface Layer 2 configuration from Trunk to Access! ')
										allowstate = 'vlan-trunk'
										allowreq = 'access'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
									elif JVLANQ1 in ['t', 'T']:
										allowstate = 'vlan-trunk'
										allowreq = 'trunk'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
							elif jvlantame == False:
								newVLANstr = str(rVLAN)
								if len(newVLANstr) == 1 and str("VLAN000" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 2 and str("VLAN00" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 3 and str("VLAN0" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 4 and str("VLAN" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif str(ifname) not in str(output_script_A):
									JVLANQ1 = input("Standard-named VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort:  ")
									if JVLANQ1 in ['a', 'A']:
										print('This will override current interface Layer 2 configuration from Trunk to Access! ')
										allowstate = 'vlan-trunk'
										allowreq = 'access'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									elif JVLANQ1 in ['t', 'T']:
										allowstate = 'vlan-trunk'
										allowreq = 'trunk'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									else:
										print('Flushing parameters..')
										returnBack()
								else:
									print('Standard-named VLAN already allowed on the specifed interface')
									returnBack()
							else:
								print('Flushing parameters..')
								returnBack()
						elif str(rVLAN) in str(output_script_A) and "port-mode access;" in str(output_script_B):
							if jvlantame == True:
								if str(jvlantval + ' ') in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This Custom-named VLAN is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This VLAN range is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str(jvlantval + ' ') not in str(output_script_A):
									print('Could not match custom VLAN name within the switch database, please try again with a valid input!')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A):
									allowstate = 'vlan-access'
									allowreq = 'trunk'
									vlanT = 'custom'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print('Flushing Configuration...')
										returnBack()
								else:
									print('Custom VLAN name Identified, preparing allowance template..')
									print('#'*80)
									JVLANQ1 = input("VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort: ")
									if JVLANQ1 in ['a', 'A']:
										allowstate = 'vlan-access'
										allowreq = 'access'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
									elif JVLANQ1 in ['t', 'T']:
										print('This will override current interface Layer 2 configuration from Access to Trunk! ')
										allowstate = 'vlan-access'
										allowreq = 'trunk'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
							elif jvlantame == False:
								newVLANstr = str(rVLAN)
								if len(newVLANstr) == 1 and str("VLAN000" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 2 and str("VLAN00" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 3 and str("VLAN0" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 4 and str("VLAN" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif str(ifname) not in str(output_script_A):
									JVLANQ1 = input("VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort:  ")
									if JVLANQ1 in ['a', 'A']:
										allowstate = 'vlan-access'
										allowreq = 'access'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									elif JVLANQ1 in ['t', 'T']:
										print('This will override current interface Layer 2 configuration from Access to Trunk! ')
										allowstate = 'vlan-access'
										allowreq = 'trunk'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									else:
										print('Flushing parameters..')
										returnBack()
								else:
									print('Standard-named VLAN already allowed on the specified interface.')
									returnBack()
							else:
								print('Flushing parameters..')
								returnBack()
						elif "error: vlan with tag" in str(output_script_A) :
							JVLANA = input("Couldn't find that specified VLAN within switch database, would you like to create it? Type 'Y' to proceed, or just any key to abort: ")
							if JVLANA in ['y', 'Y']:
								JVLANQ1 = input("For access mode type 'A' , and for trunk type 'T' or just any key to abort:  ")
								if JVLANQ1 in ['a', 'A']:
									newVLAND = input('Enter new VLAN Desciption: ')
									allowstate = 'novlan-blank'
									allowreq = 'access'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								elif JVLANQ1 in ['t', 'T']:
									newVLAND = input('Enter new VLAN Desciption: ')
									allowstate = 'novlan-blank'
									allowreq = 'trunk'
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print('Flushing parameters..')
									returnBack()
						elif str(rVLAN) in str(output_script_A):
							if jvlantame == True:
								if str(jvlantval + ' ') in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This Custom-named VLAN is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A) and str(ifname) in str(output_script_A):
									print('This VLAN range is already allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str(jvlantval + ' ') not in str(output_script_A):
									print('Could not match custom VLAN name within the switch database, please try again with a valid input!')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A):
									print('Custom VLAN range Identified, preparing allowance template..')
									allowstate = 'vlan-blank'
									allowreq = 'trunk'
									vlanT = 'custom'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print('Flushing Configuration...')
										returnBack()
								else:
									print('Custom VLAN name Identified, preparing allowance template..')
									print('#'*80)
									JVLANQ1 = input("VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort: ")
									if JVLANQ1 in ['a', 'A']:
										allowstate = 'vlan-blank'
										allowreq = 'access'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									elif JVLANQ1 in ['t', 'T']:
										print('This will override current interface Layer 2 configuration from Access to Trunk! ')
										allowstate = 'vlan-blank'
										allowreq = 'trunk'
										vlanT = 'custom'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
							elif jvlantame == False:
								newVLANstr = str(rVLAN)
								if len(newVLANstr) == 1 and str("VLAN000" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 2 and str("VLAN00" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 3 and str("VLAN0" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 4 and str("VLAN" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif str(ifname) not in str(output_script_A):
									JVLANQ1 = input("VLAN found in switch database, for access mode type 'A' , and for trunk type 'T' or just any key to abort:  ")
									if JVLANQ1 in ['a', 'A']:
										allowstate = 'vlan-blank'
										allowreq = 'access'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									elif JVLANQ1 in ['t', 'T']:
										print('This will override current interface Layer 2 configuration from Access to Trunk! ')
										allowstate = 'vlan-blank'
										allowreq = 'trunk'
										vlanT = 'standard'
										confstate = 'preview'
										JuniperConfig()
										Approval=input()
										if Approval in ['Y', 'y']:
											confstate = 'execute'
											JuniperConfig()
										else:
											print("Flushing Configuration..")
											returnBack()
									else:
										print('Flushing parameters..')
										returnBack()
								else:
									print('Standard-named VLAN already allowed on the specified interface.')
									returnBack()
							else:
								print('Flushing parameters..')
								returnBack()
					else:
						returnBack()
			jvlanloop = True
		vendorloop = True
def Option5(): # Task 5 Function.
	global ifname, vlanstate, optionstate, vlanT, allowstate, allowreq, confstate, jvlantval
	optionstate = 'option_5'
	switchVendor()
	vlanstate = 'old'
	vendorloop = False
	while not vendorloop:
		if vendortype == 'c':
			print("Please enter VLAN and interface parameters: ")
			#Cisco Disallow VLAN to Interface 
			cvlanloop = False
			while not cvlanloop:
				ifname = str(input("Please enter desired Cisco hardware interface name (case sensitive): "))
				if not re.match("^\w+(-\w+)?\d+(([\/:]\d+)+(\.\d+)?)?$", ifname):
					print('This is not a valid Cisco interface name!')
				else:
					singleVLANCheck()
					if vlanver == 'OK':
						print("Checking the requested Interface and VLAN for this specific switch...")
						print('#'*80)
						initSSHCall()
						remote_connection.send('show vlan id ' + str(rVLAN) + '\n')
						time.sleep(3)
						ssh_client.close()
						print('#'*80)
						output_script_A = remote_connection.recv(65535)
						initSSHCall()
						remote_connection.send('show running-config interface ' + str(ifname) + '\n')
						time.sleep(3)
						output_script_B = remote_connection.recv(65535)
						print('#'*80)
						ssh_client.close()
						if ">" in str(output_script_A):
							print("Couldn't gain the required exec privilege level to perform such action. Please revise your credentials and/or check switch available vty lines and try again.")
							returnBack()
						elif "Invalid input detected" in str(output_script_B):
							print("Couldn't find this interface name within the switch hardware inventory. Please check your input and try again.")
							returnBack()
						elif "not found in current VLAN database" in str(output_script_A):
							print("Couldn't find that specified VLAN within the switch database! ")
							returnBack()
						elif str(rVLAN) in str(output_script_A) and "switchport mode trunk" in str(output_script_B):
							if 'switchport trunk allowed vlan' in str(output_script_B) and str(rVLAN) not in str(output_script_B):
								print('This VLAN is NOT allowed on that interface!')
								returnBack()
							else:
								CVLANQ1 = input("VLAN found within the switch database! Remove it from this specific Trunk interface? Type 'Y' to proceed ot any key to abort: ")
								if CVLANQ1 in ['Y', 'y']:
									print('This will override current interface Layer 2 configuration! ')
									allowstate = "vlan-trunk"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
								else:
									print('Flushing configuration..')
									returnBack()
						elif str(rVLAN) in str(output_script_A) and ("switchport mode access" in str(output_script_B) or "switchport mode dot1q-tunnel"in str(output_script_B)):
							if str(rVLAN) not in str(output_script_B):
								print('This VLAN is NOT allowed on that interface!')
								returnBack()
							else:
								CVLANQ1 = input("VLAN found within the switch database! Remove it from this specific Access interface? Type 'Y' to proceed ot any key to abort: ")
								if CVLANQ1 in ['Y', 'y']:
									allowstate = "vlan-access"
									confstate = 'preview'
									CiscoConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										CiscoConfig()
								else:
									print('Flushing configuration..')
									returnBack()
						elif str(rVLAN) in str(output_script_A) and "ip address" in str(output_script_B):
							print("This is not a switchport interface, hence no VLANs are allowed by default! ")
							returnBack()
						elif str(rVLAN) in str(output_script_A):
							print("This interface is neither configured as trunk, nor access ! ")
							returnBack()
					else:
						returnBack()
			cvlanloop = True
		elif vendortype == 'j':
			print("Please enter VLAN and interface parameters: ")
			#Juniper Disallow VLAN to Interface 
			jvlanloop = False
			while not jvlanloop:
				ifname = str(input("Please enter the desired Juniper hardware interface name (case sensitive): "))
				if not any([re.match("^\De-[0-9]+\/[0-9]+\/[0-9]+\.[0-9]+$", ifname), re.match("^ae[0-9]+\.[0-9]+$", ifname)]):
					print('This is not a valid Juniper interface name!')
				else:
					singleVLANCheck()
					if vlanver == 'OK':
						jvlantval = input("If this VLAN name/range already have a custom name which doesn't comply to the naming standard, please specify (case sensitive). Leave this field empty ONLY if otherwise: ")
						if re.match('[^0-9a-zA-Z]+', jvlantval):
							print('Invalid custom VLAN name!')
						elif jvlantval == '':
							print('No custom VLAN name entered, entering standard name mode..')
							jvlantame = False
						else:
							jvlantame = True
							print('Entering custom name mode..')
						print("Checking the requested Interface and VLAN for this specific switch...")
						print('#'*80)
						initSSHCall()
						remote_connection.send('show vlans ' + str(rVLAN) + '\n')
						time.sleep(5)
						output_script_A = remote_connection.recv(65535)
						ssh_client.close()
						initSSHCall()
						remote_connection.send('show configuration interfaces ' + str(ifname) + '\n')
						remote_connection.send('show interfaces ' + str(ifname) + '\n')
						time.sleep(5)
						output_script_B = remote_connection.recv(65534)
						ssh_client.close()
						print('#'*80)
						newVLANstr = str(rVLAN)
						if str("error: device") in str(output_script_B) or str("error: interface") in str(output_script_B):
							print("Couldn't find this interface name within the switch hardware inventory. Please check your input and try again.")
							returnBack()
						elif "error: vlan with tag" in str(output_script_A):
							print("Couldn't find that specified VLAN within the switch database! ")
							returnBack()
						elif str(rVLAN) in str(output_script_A):
							if jvlantame == True:
								if str(jvlantval + ' ') not in str(output_script_A):
									print('Could not match custom VLAN name within the switch database, please try again with a valid input!')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A) and str(ifname) not in str(output_script_A):
									print('VLAN Range found, but not allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str(jvlantval + ' ') in str(output_script_A) and str(ifname) not in str(output_script_A):
									print('Custom VLAN name found, but not allowed on the specifed interface.')
									print('#'*80)
									returnBack()
								elif str("__" + jvlantval + "_" + str(rVLAN) + "__") in str(output_script_A):
									print('Custom VLAN range Identified, preparing disallowance template..')
									vlanT = 'custom'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print('Custom VLAN name Identified, preparing disallowance template..')
									vlanT = 'custom'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print('Flushing parameters..')
										returnBack()
							elif jvlantame == False:
								newVLANstr = str(rVLAN)
								if len(newVLANstr) == 1 and str("VLAN000" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 2 and str("VLAN00" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 3 and str("VLAN0" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif len(newVLANstr) == 4 and str("VLAN" + str(rVLAN)) not in str(output_script_A):
									print('The standard VLAN entered is actually a custom VLAN. Please try again with the right custom-naming.')
									print('#'*80)
									returnBack()
								elif str(ifname) in str(output_script_A):
									print("Standard VLAN found in switch database, preparing disallowance template..")
									vlanT = 'standard'
									confstate = 'preview'
									JuniperConfig()
									Approval=input()
									if Approval in ['Y', 'y']:
										confstate = 'execute'
										JuniperConfig()
									else:
										print("Flushing Configuration..")
										returnBack()
								else:
									print("Standard VLAN name found, but not allowed on the specifed interface.")
									print('#'*80)
									returnBack()
							else:
								print('Flushing parameters..')
								returnBack()
					else:
						returnBack()
			jvlanloop = True
#Program Start #
#Disclaimer Message #
print(" ")
print("Disclaimer:")
print("="*11)
print("AutoVLAN is a comprehensive piece of work that aims to ease up the overwhelming load of VLAN")
print("management and provisioning tasks over a typical Service Provider/Datacenter environment for Cisco and") 
print("Juniper platforms. Please bear in mind that this tool was originally intended to aid network engineers")
print("in the first place. You're still responsile for your inputs, therefore you should NOT bypass basic") 
print("engineering concepts and/or essencial procedures.")
print("I hope this helps..")
print(" ") 
print("Credits: ") 
print('Mina G. Nasry')
print('')
try:
	WelcomeScreen()
	userAuth()
except KeyboardInterrupt:
	print(" ")
	print("Program Terminated, Goodbye ! ._. ")
	exit()
except paramiko.ssh_exception.AuthenticationException:
	print(" ")
	print("Couldn't access the remote-host. Authentication failed, please try again!")
	userAuth()
except TimeoutError or EOFError or OSError or paramiko.ssh_exception.NoValidConnectionsError or paramiko.ssh_exception.SSHException:
	print(" ")
	print("Couldn't establish an SSH connection to the remote-host. Please check your network settings and try again!")
	DisplayScreen()
#Program End #
