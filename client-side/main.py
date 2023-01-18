import os
import sys
import datetime
import argparse
import configparser
import paramiko
from glob import glob

def cli():
	parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')
	subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

	configParser = subparsers.add_parser('config', help='Configuration settings')

	configParser.add_argument('-s', '--server', help = 'the server to upload the post to', required=True)
	configParser.add_argument('-p', '--port', help = 'the ssh port on the web server', required=True)
	configParser.add_argument('-u', '--user', help = 'your ssh username on the web server', required=True)

	postParser = subparsers.add_parser('post', help="Post an update to the server")
	
	args = parser.parse_args()
	return args

def createSSHTransport(server, port, username, privatekey, password):
	transport = paramiko.Transport((server, int(port)))
	if privatekey != None:
		privatekeyfile = paramiko.RSAKey.from_private_key_file(privatekey)
		transport.connect(username=username, pkey=privatekeyfile)
	else:
		transport.connect(username=username, password=password)
	return transport

def config():
	configFile = configparser.ConfigParser()
	configFile.add_section('SSHSettings')
	configFile.set('SSHSettings', 'server', server)
	configFile.set('SSHSettings', 'port', port)
	configFile.set('SSHSettings', 'user', user)
	configFile.set('SSHSettings', 'password', password)
	configFile.set('SSHSettings', 'privateKey', privateKey)
	with open('grio.conf', 'w') as configFileObj:
		configFile.write(configFileObj)
		configFileObj.flush()
		configFileObj.close()

def post(user, content, transport):
	channel = transport.open_session()
	time = str(datetime.datetime.now())
	with open('grioblog.csv', 'a') as file:
		file.write(time + ','  + content + '\n')
	channel.put('grioblog.csv', remote_path='/home/' + user + '/grio/grioblog.csv')
	channel.exec_command("if [[ ! -d '/home' + user + '/grio/service/' ]]; then mkdir -p '/home/' + user + '/grio/service/'; fi")
	channel.exec_command("export GRIO_USER=user")
	channel.close()
	transport.close()

def main():
	configParser = configparser.ConfigParser()
	args = cli()
	if args.subcommand == 'post':
		content = input("What's on your mind? ")
		if os.path.exists('grio.conf'):
			configParser.read('grio.conf')
			server = configParser['SSHSettings']['server']
			port = configParser['SSHSettings']['port']
			user = configParser['SSHSettings']['user']
			password = configParser['SSHSettings']['password']
			privateKey = configParser['SSHSettings']['privateKey']
			sshTransport = createSSHTransport(server, port, user, password, privateKey)
			post(user, content, sshTransport)
		else:
			print('No config file found, run "grio config" to setup')
			sys.exit()
	elif args.subcommand == 'config':
		if os.path.exists('grio.conf'):
			os.remove('grio.conf')
		password = ""
		privateKey = ""
		configParser['SSHSettings'] = {}
		configParser['SSHSettings']['server'] = args.server
		configParser['SSHSettings']['port'] = args.port
		configParser['SSHSettings']['user'] = args.user
		keyPrompt = input("Does your web server require an SSH key? (Y/n)")
		if keyPrompt == 'Y' or keyPrompt == 'y' or keyPrompt == '\n':
			defaultLocation = os.path.expanduser("~/.ssh/")
			privateKeys = glob(defaultLocation + "id_*")
			if privateKeys:
				print("Found the following private keys in the default location:")
				for i, key in enumerate(privateKeys):
					print(f"{i+1}. {key}")
				userChoice = input("Select the private key you want to use (1-{}): ".format(len(privateKeys)))
				privateKey = privateKeys[int(userChoice) - 1]
			else:
				privateKey = input("No private keys found in the default location. Please provide the path to your private key: ")
		elif keyPrompt == 'n':
			password = input("Enter your SSH password:")
		configParser['SSHSettings']['password'] = password
		configParser['SSHSettings']['privateKey'] = privateKey
	with open('grio.conf', 'w') as configFile:
		configParser.write(configFile)
		print("Grio is configured, use \"grio post\" to post")

if __name__ == "__main__":
	main() 
