import datetime
import configparser

from scp import SCPClient
from paramiko import SSHClient

def config():
    import configparser

    configFile = configparser.ConfigParser()
    configFile.add_section('SSHSettings')

    configFile.set('SSHSettings', 'server', server)
    configFile.set('SSHSettings', 'port', port)

    with open('grio.conf', 'w') as configFileObj:
        configFile.write(configFileObj)
        configFileObj.flush()
        configFileObj.close()

def cli():
    import argparse

    parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')

    parser.add_argument('post', metavar = 'post', help = 'the content of the post', required=True)
    parser.add_argument('-c', '--config', metavar = 'config', help = 'set up configuration file', default=False, required=False)
    parser.add_argument('-s', '--server', metavar = 'server', help = 'the server to upload the post to', required=False)
    parser.add_argument('-p', '--port', metavar = 'port', help = 'the ssh port on the web server', required=False)

    args = parser.parse_args()

def main():
    timestamp = datetime.now()

    open("grioblog.txt", "a")

    with open('grioblog.txt') as f:
        post = f.readlines()
        t.append(timestamp + post)

    with open('grioblog.txt', 'w') as f:
        f.writelines(t)

    #ssh = SSHClient()
    #ssh.load_system_host_keys()
    #ssh.connect('rio.pink')

    #scp = SCPClient(ssh.get_transport())

if __name__ == "__main__":
    main()
