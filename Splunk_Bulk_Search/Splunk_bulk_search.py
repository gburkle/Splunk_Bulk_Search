# Imports
import sys, os, re
from pprint import pprint
import socket
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Splunk SDK oneshot Search
from splunklib.client import connect
import splunklib.results as results

try:
    import utils
except ImportError:
    raise Exception("Add the SDK repository to your PYTHONPATH to run the examples "
                    "(e.g., export PYTHONPATH=~/splunk-sdk-python.")

##### Dependencies ###########


try:
	from termcolor import colored, cprint
except Exception as e:
	print("Please install module python-termcolor\n")
	sys.exit(0)

try:
	import getpass
except Exception as e:
	print("Please install module getpass\n")
	sys.exit(0)

####### YOUR SPLUNK SERVER AND PORT ###########
host = '127.0.0.1'
port = '8089'
scheme = 'https'
version = '5.0'
##############################################


def main():
	if len(sys.argv) == 2:   
		forthelolz()
	elif len(sys.argv) == 1: # Bring the Menu UP
		# MENU
		choise = menu()
		while choise != 4: 
			if choise == 1:
				help()
			elif choise == 2:
				bulksearch()
			elif choise == 3:
				bulksearchrawlogs()
			else:
				print ("Invalid number. Get some coffee and try again...")
			choise = menu()
	else:
		print ("Too many arguments!!\n")

	cls()

def cls(): 
	try:
		os.system('cls') # For windows
	except Exception as e: return
	try:
		os.system('clear') # For Linux
	except Exception as e: return

def menu():
	print ("""
___________________________________________________________________________
  / ____|       | |              | |                               
 | (___   _ __  | | _   _  _ __  | | __                            
  \___ \ | '_ \ | || | | || '_ \ | |/ /                            
  ____) || |_) || || |_| || | | ||   <                             
 |_____/ | .__/ |_| \__,_||_| |_||_|\_\                            
  ____   | |    _  _       _____                          _        
 |  _ \  |_|   | || |     / ____|                        | |       
 | |_) | _   _ | || | __ | (___    ___   __ _  _ __  ___ | |__     
 |  _ < | | | || || |/ /  \___ \  / _ \ / _` || '__|/ __|| '_ \    
 | |_) || |_| || ||   <   ____) ||  __/| (_| || |  | (__ | | | | _ 
 |____/  \__,_||_||_|\_\ |_____/  \___| \__,_||_|   \___||_| |_|(_)
____________________________________________________________________________

[1] Help .............................. Displays some help.
[2] Bulk Search ....................... Search a list of IPs AND/OR urls on Splunk (Slow).
[3] Bulk Search with raw logs.......... Search a list of IPs AND/OR urls and dump all raw logs into a file (VERY Slow).  
[4] Quit
""")
	try:
		ans = input('Enter your choise [1-4]: ')
		return ans
	except Exception as e: 
		print ("Was that even a number! come on man get it togheter!\n")
		pass


def help():
	print ("""
[+] Bulk Search: Search Splunk for a list of IPs/URLs. Move to the next IP/URL at the first hit. 
                 Two lists will be created "hits.txt" containing a list of IPs/URLs found on Splunk logs, 
                 and "already_checked.txt" containing a list of the IP's/URL' that you have already looked for in the list. (in case of crash).

[+] Bulk Search with raw logs: Search Splunk for a list of IP/URLs. Find everything about the IP/URL and dump raw logs into a file. 
""")
	raw_input()
	cls()

def bulksearch():
	print ("\n\n ---------- Bulk Search -----------\n")


	checked = open('already_checked.txt', 'w')
	hits = open ('hits.txt', 'w')

	creds = getconfig()
	file = (creds[0]['file'])

	# Splunk-sdk API takes a dictionary as arguments for authentication.
	arguments = {'host':host, 'port':port, 'username':creds[1]['user'], 'password':creds[2]['passwd'], 'scheme':scheme, 'version':version}
	# Splunk-sdk API takes separate "Flags" as arguments for options.
	flag = {'earliest_time':creds[3]['time']}

	try:
		with open(file, 'r') as f:
			reader = f.read().splitlines()
			for line in reader:
				#print (line)  # For testing
				search = 'search ' + line + ' | head 1'
				print "Searching => (", line, ") ..............",
				## OneShot search
				service = connect(**arguments)
				socket.setdefaulttimeout(None)
				response = service.jobs.oneshot(search, **flag)
				results = pretty(response)
				#print results
				if results != None:
					text = colored('FOUND', 'red', attrs=['blink'])
					print "[",text,"]\n"
					hits.write(line + '\n')
				else:
					print "[ Done ]\n"

				checked.write(line + '\n')
	except Exception as e: 
		print ('\nSomething went wrong!!! ', e)

	checked.close()
	hits.close()



def pretty(response):
	reader = results.ResultsReader(response)
	for result in reader:
		if isinstance(result, dict):
			return (result)
		else:
			return (0)

def getconfig():
	creds = []
	file = raw_input("Enter the name of the file containing you list of IP/URLs (must be on the same filder as this script): ")
	creds.append({'file': file})
	user = raw_input("Enter your Splunk username: ")
	creds.append({'user' : user})
	password = getpass.getpass("Enter your Splunk password: ")
	creds.append({'passwd' : password})

	print ("""
How far back do you want to search?
[1] 1 Day.
[2] 1 week.
[3] 1 month.
[4] 6 months
""")

	while True:
		try:
			backtime = int(raw_input("Option: "))
		except Exception as e: 
			print ("Was that even a number? \n")
			backtime = 0
		if backtime == 1:
			backtime = '-1d'
			break
		elif backtime == 2:
			backtime = '-1w'
			break
		elif backtime == 3:
			backtime = '-1mon'
			break
		elif backtime == 4:
			backtime = '-6mon'
			break
		else:
			print ("That doesn't seem to be an option. \n")


	creds.append({'time':backtime})  
	return (creds)

def bulksearchrawlogs():
	print ("\nThis function has not been implemented ask Gerardo to drink more coffee and get to it\n")
	raw_input()
	cls()

def forthelolz():
	print ("No need for arguments man!! This is interactive like PTs!")



if __name__ == '__main__':
	cls()
	main()
