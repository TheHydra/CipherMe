'''
Coder: The-Hydra
Script: CipherMe.py
'''
# Import needed Modules
import os
from Crypto.Cipher import AES
from time import sleep
from colorama import *
import sqlite3
from getpass import getpass
from hashlib import md5
from msvcrt import getch
import random
import sys
init()
print Style.BRIGHT
#
global chars
chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","!","@","#","$","%","^","&","*","(",")"]
#
# LOGIN
os.system('title Cipher Me                                                                                                 ^| Coder (c) The-Hydra')
def Speak(string):
	f = open('voice.vbs', 'a')
	f_string = string.replace(" ",", ")
	f.write("Set sapi = CreateObject(\"sapi.spvoice\")\n")
	f.write("Set fso = createobject(\"scripting.filesystemobject\")\n")
	f.write("sapi.Speak \""+string+"\"\n")
	f.write("fso.deletefile wscript.scriptfullname ")
	f.close()
	os.system('voice.vbs')
# -------------------------------------------------------- #
def Login():
	open_db()
	os.system('cls')
	print '\n'*2
	print Fore.CYAN+'                                  Cipher Me!\n'
	print Fore.WHITE+'                   (En/De)crypting Files & Folders Program'
	print Fore.YELLOW+'\t\t   _______________________________________'+Fore.WHITE
	print Fore.YELLOW+'\t\t              |              |'
	print Fore.YELLOW+'\t\t              | '+Fore.WHITE+'Login Screen '+Fore.YELLOW+'|'
	print Fore.YELLOW+'\t\t              |______________|\n\n'
	print Fore.WHITE+'   ---------------'
	print '  | 1. Sign in    |'
	print '  | 2. Sign up    |'
	print '  | 3. About      |'
	print '   ---------------'
	print '  | 0. Terminate  |'
	print '   ---------------'
	try:
		ch = input(Fore.GREEN+'\n => Option: '+Fore.MAGENTA)
	except: Login()
	if ch == 1:
		sign_in()
	elif ch == 2:
		sign_up()
	elif ch == 3:
			About()
	elif ch == 0:
		sys.exit()
	else: Login()
#######################################################################
def sign_in():
	os.system('cls')
	print '\n'*6
	login = raw_input(Fore.CYAN+'\n\n >>> ID: '+Fore.WHITE)
	enc_login = md5(login).hexdigest()
	print Fore.CYAN+'\n >>> Password:'+Fore.WHITE,
	paswd = getpass(' ')
	enc_pwd = md5(paswd).hexdigest()
	final_input = enc_login+":"+enc_pwd
	read_users = curs.execute('''SELECT * FROM USERS''')
	check_list = []
	for user in read_users:
		 check_list.append(user[0]+":"+user[1])
	if final_input in check_list:
		Target_User = md5(login).hexdigest()
		read_users = curs.execute('''SELECT * FROM USERS''')
		for user in read_users:
			if user[0] == Target_User:
				global WantedKey
				WantedKey = user[2]
		Speak('Welcome')
		while 1: Main()
	else:
		print Fore.RED
		print '   ------------------------------------------------------------------------'
		print '  | Wrong inputs, you are not allowed to use this program, please sign up! |'
		print '   ------------------------------------------------------------------------',
		Speak('Wrong Inputs, You Are Not Allowed To Use This Program, Please Sign Up')
		sleep(1)
		Login()
def sign_up():
	os.system('cls')
	print '\n'*4+Fore.WHITE
	User_ID = raw_input(Fore.CYAN+' >>> User ID: '+Fore.WHITE)
	enc_User_ID = md5(User_ID).hexdigest()
	print Fore.CYAN+'\n >>> Password: '+Fore.WHITE,
	pass_wd = getpass(' ')
	print Fore.CYAN+'\n >>> Re-Type Password: '+Fore.WHITE,
	re_pass_wd = getpass(' ')
	enc_pass_wd = md5(pass_wd).hexdigest()
	if pass_wd != re_pass_wd:
		print Fore.RED
		print '\t\t\t  ---------------------------'
		print '\t\t\t | Passwords does not match! |'
		print '\t\t\t  ---------------------------',
		Speak('Passwords Does Not Match')
		sleep(1)
		Login()
	# ------------------- KEY PART ------------------#
	try:
		key_length = input(Fore.CYAN+"\n >>> Choose Encryption Key Length (16/24/32): "+Fore.WHITE)
	except: Login()
	if key_length not in (16,24,32) :
		print Fore.RED
		print '\t\t      ------------------------------------'
		print '\t\t     | Key Length must be 16 or 24 or 32! |'
		print '\t\t      ------------------------------------',
		Speak('Key Length must be 16 or 24 or 32')
		sleep(1)
		Login()
	else:
		key = ""
		for x in range(0,key_length):
			key += random.choice(chars)
		print Fore.RED+" \n [+] Key Generated: "+Fore.WHITE+key
		sleep(1)
	# ------------------- /KEY PART -----------------#
	if pass_wd == re_pass_wd:
		record_owner = User_ID.replace(' ','_')
		try:
			curs.execute(''' CREATE TABLE  '''+record_owner+'''(record TEXT, login TEXT, password TEXT, key TEXT)''')
			curs.execute(''' INSERT INTO USERS (id, pwd, key) VALUES (?,?,?) ''',(enc_User_ID,enc_pass_wd, key))
			CreateDB.commit()
			print Fore.GREEN
			print '      ------------------------------------------------------------------'
			print '     | Congratulations, Now you have the permission to use the program! |'
			print '      ------------------------------------------------------------------'
			Speak('Congratulations, Now You Have The Permission To Use The Program')
			sleep(1)
			Login()
		except:
			print Fore.RED
			print '\t  ------------------------------------------------------'
			print '\t | Error, There is an existing user with the same name! |'
			print '\t  ------------------------------------------------------',
			Speak('Error, There Is An Existing User With The Same Name')
			sleep(1)
			enc_User_ID = ""
			enc_pass_wd = ""
			Login()
def open_db():
	global CreateDB, curs
	DBpath = str(os.environ['PROGRAMFILES']+'\\CipherMe')
	if os.path.exists(DBpath):
		CreateDB = sqlite3.connect(DBpath+'\\5r35u.db')
		curs = CreateDB.cursor()
		try: curs.execute(''' CREATE TABLE USERS (id TEXT, pwd TEXT, key TEXT)''')
		except: pass
	else:
		try:
			os.mkdir(DBpath)
			open_db()
		except:
			print Fore.RED+ "\n\n\n\n ** Run the Program as administrator:"
			print "\n >>> Right-Click on the program --choose--> Run as administrator "
			getch()
			sys.exit()
#
def About():
	os.system('cls')
	print Fore.RED+"\n\n [+] About the Program:"+Fore.WHITE+" _____________________________________________________\n"
	print "  | This program secures your important files, the files you don\'t want any- |"
	print "  | one to see them. So the program ENCRYPTs your files with AES encryption  |"
	print "  | algorithm and when you want them back again you can simply decrypt them. |"
	print "  | But to use the program you should be registered user.                    |"
	print "  | So, Sign up & Enjoy using the program!                                   |"
	print "  |                                                                          |"
	print "  | - The Hydra                                                              |"
	print "  |__________________________________________________________________________|"
	print Fore.RED
	print "  * Press any key to continue ..."
	getch()
	Login()
def EncryptFile(File):
	if os.path.exists(File) == True:
		AESObj = AES.new(WantedKey, AES.MODE_CFB)
		with open(File, 'rb') as f:
			Enc = AESObj.encrypt(f.read())
			HEX = Enc.encode("hex")
			f.close()
		with open(File, 'wb') as f:
			f.write(HEX)
			f.close()
	else:
		print Fore.RED + "\n [ERROR] File [",File,"] doesn\'t exist!"
		sleep(2)
		Main()
def DecryptFile(File):
	if os.path.exists(File) == True:
		AESObj = AES.new(WantedKey, AES.MODE_CFB)
		with open(File, 'rb') as f:
			HEX = f.read().decode("hex")
			DecFile = AESObj.decrypt(HEX)
			f.close()
		with open(File, 'wb') as f:
			f.write(DecFile)
			f.close()
	else:
		print Fore.RED + "\n [ERROR] File doesn\'t exist!"
		sleep(2)
		Main()
##############################
def ForFolders(path, Operation):
	if os.path.exists(path):
		FolderNum = FilesNum = 0
		AllFiles  = []
		for folder in os.walk(path):
			FolderNum += 1
			for File in folder[2]:
				FilesNum += 1
				REAL_FILE_PATH = folder[0]+'\\'+File
				AllFiles.append(REAL_FILE_PATH)
		if Operation == 'encrypt':
			for file in AllFiles:
				EncryptFile(file)	
		if Operation == 'decrypt':
			for file in AllFiles:
				DecryptFile(file)
		print Fore.RED+"\n [+] Sum"+Fore.WHITE+": "+Fore.RED+str(FilesNum)+Fore.WHITE+ " file(s) in "+Fore.RED+str(FolderNum)+Fore.WHITE+" Folder(s)\n"
		print Fore.WHITE+"  * Press any key to continue ..."
		getch()
		Main()
	else: 
		print Fore.RED + "\n [ERROR] Folder doesn\'t exist!"
		sleep(2)
		Main()
# ------------------------------
def Main():
	os.system('cls')
	print Fore.YELLOW+"*"*79
	print Fore.WHITE+"\t\t\t\t Cipher Me!"
	print Fore.YELLOW+"*"*79
	print Fore.RED+"\n [+] Choose:\n"+Fore.WHITE
	print "     1. Encrypt"
	print "     2. Decrypt"
	try:
		ch = input(Fore.GREEN+"\n => Option: "+Fore.MAGENTA)
	except: Main()
	if ch == 1:
		print Fore.WHITE+"\n"+"-"*79
		print Fore.YELLOW+"\n [+] Encrypt _________________________"
		print "  |                                   |"
		print "  |"+Fore.CYAN+"  1. File            2. Folder     "+Fore.YELLOW+"|"
		print "  |___________________________________|"
		ch = raw_input(Fore.GREEN+"\n => Opiton: "+Fore.MAGENTA)
		if ch in ("1","2"):
			path = raw_input(Fore.GREEN+"\n  >>> Enter Path: "+Fore.MAGENTA)
			if ch == '1':
				EncryptFile(path)
			elif ch == '2':
				ForFolders(path, 'encrypt')	
		else:
			print Fore.RED+'\n [ERROR] Wrong input! '
			sleep(2)
			Main()
		##################
	elif ch == 2:
		print Fore.WHITE+"\n"+"-"*79
		print Fore.YELLOW+"\n [+] Decrypt _________________________"
		print "  |                                   |"
		print "  |"+Fore.CYAN+"  1. File            2. Folder     "+Fore.YELLOW+"|"
		print "  |___________________________________|"
		ch = raw_input(Fore.GREEN+"\n => Opiton: "+Fore.MAGENTA)
		if ch in ("1","2"):
			path = raw_input(Fore.GREEN+"\n  >>> Enter Path: "+Fore.MAGENTA)
			if ch == '1':
				DecryptFile(path)
			elif ch == '2':
				ForFolders(path, 'decrypt')
		else:
			print Fore.RED+'\n [ERROR] Wrong input! '
			sleep(2)
			Main()
#
Login()
