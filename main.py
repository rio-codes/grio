import datetime
import argparse
import os
import configparser

from scp import SCPClient
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
    subparsers = parser.add_subparsers(help = 'post or configure grio')

    postParser = subparsers.add_parser('post')
    configParser = subparsers.add_parser('config')

    postParser.add_argument('post', metavar = 'post', help = 'the content of the post', required=False)

    configParser.add_argument('config', metavar = 'config', help = 'set up configuration file', default=False, required=False)
    configParser.add_argument('-s', '--server', metavar = 'server', help = 'the server to upload the post to', required=False)
    configParser.add_argument('-p', '--port', metavar = 'port', help = 'the ssh port on the web server', required=False)

    args = parser.parse_args()

    return args

def main():
    timestamp = datetime.now()

    if os.path.exists('grio.conf'):
        config = configparser.ConfigParser()
        config.read('grio.conf')
        server = config['SSHSettings']['server']
        port = config['SSHSettings']['server']
    else:
        print('No config file found, run "grio config" to setup')
        exit

    args = cli()
    newPost = args.post

#    if args.server:
#        server = args.server
#    else:

    with open('grioblog.txt', 'r') as f:
        with open('grioblog_new.txt', 'w') as n:
            lines = f.readlines()
            n.write(timestamp + newPost)
            for line in lines:
                n.write(line)
            n.close()
        f.close()

#ssh = SSHClient()
    #ssh.load_system_host_keys()
    #ssh.connect('rio.pink')

    #scp = SCPClient(ssh.get_transport())

if __name__ == "__main__":
    main() 
