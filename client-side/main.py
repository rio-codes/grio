import datetime
import argparse
import os
import sys
import configparser
import scp
import paramiko

from scp import SCPClient
from paramiko import SSHClient

def cli():
	parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')
	subparsers = parser.add_subparsers(help = 'post or configure grio', dest='command')

	postParser = subparsers.add_parser('post')
	configParser = subparsers.add_parser('config')

	postParser.add_argument('post', action = 'store', nargs='?', help = 'the content of the post')
	configParser.add_argument('-s', '--server', help = 'the server to upload the post to', required=True)
	configParser.add_argument('-p', '--port', help = 'the ssh port on the web server', required=True)
	configParser.add_argument('-u', '--user', help = 'your ssh username on the web server', required=True)
	configParser.add_argument('-P', '--password', help = 'your ssh password on the web server', required=True)

	args = parser.parse_args()

	return args

def createSSHClient(server, port, user, password):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
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

def post(content, ssh):
	time = str(datetime.datetime.now())
	with open('grioblog.csv', 'a') as file:
		file.write(time+','+content+'\n')
	scp = SCPClient(ssh.get_transport())
	scp.put('grioblog.csv')

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
			ssh = createSSHClient(server,port,user,password)

			if os.path.exists('grioblog.txt'):
				post(args.post, ssh)
			else:
				open('grioblog.txt', "a")
				post(args.post, ssh)
		else:
			print('No config file found, run "grio config" to setup')
			sys.exit()
	elif args.command == 'config':
		configParser['SSHSettings'] = {}
		configParser['SSHSettings']['server'] = args.server
		configParser['SSHSettings']['port'] = args.port
		configParser['SSHSettings']['user'] = args.user
		configParser['SSHSettings']['password'] = args.password

	with open('grio.conf', 'w') as configFile:
		configParser.write(configFile)

	

if __name__ == "__main__":
	main() 
