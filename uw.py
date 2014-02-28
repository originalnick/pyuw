from twill.commands import *
import paramiko

#Klasa do poruszania sie po usosie
class Usos():
	def __init__(self,login,password):
		self.login=login
		self.password=password
		self.loggedIn=False

	#metoda logujaca
	def logIn(self):
		go('https://logowanie.uw.edu.pl/cas/login')
		fv('1','username',self.login)
		fv('1','password',self.password)
		try:
			dummy=submit('3')
			self.loggedIn=True

			#Easier to ask for forgiveness than permission
			try:
				verbose
			except NameError:
				verbose=True
			if verbose:
				print 'Usos - zalogowano.'
		except:
			print 'Error 10: Logowanie nie powiodlo sie.'
	
	#metoda rejestrujaca na przedmiot
	def register(self, url):
		if self.loggedIn:
			go(url)
			submit('1')
		else:
			print 'Error 11: Uzytkownik niezalogowany.'


#Klasa do poruszania sie po serwerze mimuw
class Ssh():
	def __init__(self, login, password):
		self.login=login
		self.password=password
		self.host="students.mimuw.edu.pl"
		self.port=22
		self.loggedIn=False
		self.mailList=[]

		self.client=paramiko.SSHClient()
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(paramiko.WarningPolicy)

	def logIn(self):
		try:
			self.client.connect(self.host, username=self.login, password=self.password, port=self.port)
			self.loggedIn=True
			try:
				verbose
			except NameError:
				verbose=True
			if verbose:
				print "Ssh - zalogowano."
		except:
			print "Error 20: Logowanie nie powiodlo sie."

	def execute(self, command):
		if self.loggedIn:
			stdin, stdout, stderr = self.client.exec_command(command)
			if stderr:
				print stderr.read()
			if stdout:
				print stdout.read()
		else:
			print "Error 21: Uzytkownik niezalogowany."
	
	def checkMail(self):
		if self.loggedIn:
			stdin, stdout, stderr = self.client.exec_command('cd Mail/Maildir/new;ls')
			stdoutCopy=stdout.read()
			if stdoutCopy != '':
				try:
					verbose
				except NameError:
					verbose=True
				if verbose:
					print "Nowa poczta!"
				mailList=stdoutCopy.split('\n')
				mailCount=1

				for mail in mailList:
					if mail!='':
						print mailCount, mail
						self.mailList.append(mail)
					mailCount+=1

			else:
				try:
					verbose
				except NameError:
					verbose=True
				if verbose:
					print "Nie ma nowych wiadomosci"

	def displayMail(self):
		if self.loggedIn:
			if self.mailList==[]:
				try:
					verbose
				except NameError:
					verbose=True
				if verbose:
					print "Nie ma nowych wiadomosci"
			else:
				mailCount=1
				for mail in self.mailList:
					stdin, stdout, stderr = self.client.exec_command('cd Mail/Maildir/new;cat ' + mail)
					print "Wiadomosc nr ", mailCount, "/", len(self.mailList)
					print stdout.read()
					mailCount+=1
		else:
			print "Error 31: Uzytkownik niezalogowany"

#Skrypt
if __name__=="__main__":
	import argparse
	from os import remove

	parser=argparse.ArgumentParser()
	parser.add_argument("--usosLogin", "-ul")
	parser.add_argument("--sshLogin", "-sl")
	parser.add_argument("--password", "-pw")
	
	parser.add_argument("--verbose", "-v", action="store_true")
	parser.add_argument("--usos", "-u", action="store_true")
	parser.add_argument("--ssh", "-s", action="store_true")
	parser.add_argument("--mail", "-m", action="store_true")

	args=parser.parse_args()

	verbose=args.verbose

	redirect_output('dummy')

	if args.usos:
		try:
			UsosClient=Usos(args.usosLogin, args.password)
		except NameError:
			print "Error 42: Nie podano loginu lub hasla do usosa"
		UsosClient.logIn()
	if args.ssh:
		try:
			SshClient=Ssh(args.sshLogin, args.password)
		except NameError:
			print "Error 43: Nie podano loginu lub hasla do ssh"
		SshClient.logIn()
		if args.mail:
			SshClient.checkMail()
#			SshClient.displayMail()

	remove('dummy')