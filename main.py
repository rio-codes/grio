import datetime
import argparse
import os
import sys
import configparser

# from scp import SCPClient
from paramiko import SSHClient

def config():

    configFile = configparser.ConfigParser()
    configFile.add_section('SSHSettings')

    configFile.set('SSHSettings', 'server', server)
    configFile.set('SSHSettings', 'port', port)

    with open('grio.conf', 'w') as configFileObj:
        configFile.write(configFileObj)
        configFileObj.flush()
        configFileObj.close()

def cli():

    parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')
    subparsers = parser.add_subparsers(help = 'post or configure grio', dest='command')

    postParser = subparsers.add_parser('post')
    configParser = subparsers.add_parser('config')

#    postParser.add_argument('post', help = 'post to grio')
    postParser.add_argument('post', action = 'store', nargs='?', help = 'the content of the post')
    configParser.add_argument('config', help = 'set up configuration file')
    configParser.add_argument('-s', '--server', help = 'the server to upload the post to', required=True)
    configParser.add_argument('-p', '--port', help = 'the ssh port on the web server', required=True)

    args = parser.parse_args()

    return args

def post(content):

# insert post() function

def main():
    config = configparser.ConfigParser()

    args = cli()

    if args.command == 'post':
        if os.path.exists('grio.conf'):
            config.read('grio.conf')
            server = config['SSHSettings']['server']
            port = config['SSHSettings']['server']
            post(args.post)
        else:
            print('No config file found, run "grio config" to setup')
            sys.exit()
    elif args.command == 'config':
        config['SSHSettings'] = {}
        config['SSHSettings']['server'] = args.server
        config['SSHSettings']['port'] = args.port
        with open('grio.conf', 'w') as configFile:
            config.write(configFile)

#ssh = SSHClient()
    #ssh.load_system_host_keys()
    #ssh.connect('rio.pink')

    #scp = SCPClient(ssh.get_transport())

if __name__ == "__main__":
    main() 
