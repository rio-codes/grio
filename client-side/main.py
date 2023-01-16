import datetime
import argparse
import os
import sys
import configparser
import scp
import paramiko
import interactive
from scp import SCPClient
from paramiko import SSHClient

def cli():
	parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')
	postParser = subparsers.add_parser('post')
	configParser = subparsers.add_parser('config')
	configParser.add_argument('-s', '--server', help = 'the server to upload the post to', required=True)
	configParser.add_argument('-p', '--port', help = 'the ssh port on the web server', required=True)
	configParser.add_argument('-u', '--user', help = 'your ssh username on the web server', required=True)
	configParser.add_argument('-k', '--hostkey', help = 'the path to your public key on the web server', required=False)
	configParser.add_argument('-P', '--password', help = 'your ssh password on the web server', required=False)

	authGroup = parser.add_mutually_exclusive_group(required=True)
	authGroup.add_argument('-k', '--hostkey', help = 'the path to your public key on the web server', action='store_true')
	authGroup.add_argument('-P', '--password', help = 'your ssh password on the web server', action='store_true')

	args = parser.parse_args()
	return args

#def createSSHConnection(host, user, connect_kwargs={'key_filename': args.pkey} as connection)

def createSSHClient(server, port, user, password):
	client = paramiko.SSHClient()
	client.load_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server, port, user, password)
	return client

def config():
	configFile = configparser.ConfigParser()
	configFile.add_section('SSHSettings')
	configFile.set('SSHSettings', 'server', server)
	configFile.set('SSHSettings', 'port', port)
	configFile.set('SSHSettings', 'user', user)
	configFile.set('SSHSettings', 'password', password)
	with open('grio.conf', 'w') as configFileObj:
		configFile.write(configFileObj)
		configFileObj.flush()
		configFileObj.close()

#def defineGriodService():
	# add code to modify service and path files with username for upload

def post(user, content, ssh):
	
	
	scp = SCPClient(ssh.get_transport())
	ime = str(datetime.datetime.now())
	with open('grioblog.csv', 'a') as file:
		file.write(time + ','  + content + '\n')
	scp.put('grioblog.csv', remote_path='/home/' + user + '/grio/grioblog.csv')
	scp.close()
	
	channel = ssh.get_transport().open_session()
	channel.invoke_shell()
	interactive.interactive_shell(channel)
	if [[ ! -d '/home' + user + '/grio/service/' ]]; then 
		mkdir -p '/home/' + user + '/grio/service/' 
	fi
	export GRIO_USER=user
	
	#_stdin, _stdout,_stderr = ssh.exec_command(echo "\'if [[ ! -d \'/home\' + user + \'/grio/service/\' ]]; then mkdir -p \'/home/\' + user + \'/grio/service/\'; fi")
	#_stdin, _stdout,_stderr = ssh.exec_command(echo "\'export GRIO_USER=\' + user")
	ssh.close()


##### import ssh key
# from paramiko import RSAKey
# from paramiko.py3compat import decodebytes

# client = SSHClient()

# # known host key
# know_host_key = "<KEY>"
# keyObj = RSAKey(data=decodebytes(know_host_key.encode()))

# # add to host keys
# client.get_host_keys().add(hostname=HOST, keytype="ssh-rsa", key=keyObj)

# # login to ssh hostname
# client.connect(hostname=HOST, port=PORT, username=USER)...
#####

def main():

	configParser = configparser.ConfigParser()
	args = cli()

	if args.command == 'post':
		if os.path.exists('grio.conf'):
			configParser.read('grio.conf')
			server = configParser['SSHSettings']['server']
			port = configParser['SSHSettings']['port']
			user = configParser['SSHSettings']['user']
			password = configParser['SSHSettings']['password']
			hostkey - configParser['SSHSettings']['hostkey']
			hostString = user + '@' + server + ':' + port

			ssh = createSSHClient(server,port,user,auth)
			if os.path.exists('grioblog.txt'):
				post(user, args.post, ssh)
			else:
				open('grioblog.txt', "a")
				post(user, args.post, ssh)
		else:
			print('No config file found, run "grio config" to setup')
			sys.exit()
	elif args.command == 'config':
		configParser['SSHSettings'] = {}
		configParser['SSHSettings']['server'] = args.server
		configParser['SSHSettings']['port'] = args.port
		configParser['SSHSettings']['user'] = args.user
		configParser['SSHSettings']['password'] = args.password
		configParser['SSHSettings']['hostkey'] = args.hostkey

	with open('grio.conf', 'w') as configFile:
		configParser.write(configFile)

if __name__ == "__main__":
	main() 
