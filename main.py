import datetime
import argparse

from scp import SCPClient
from paramiko import SSHClient

timestamp = datetime.now()
parser = argparse.ArgumentParser(description='Post short updates to a microblog on a remote server')

parser.add_argument('post', metavar = 'post', help = 'the content of the post', required=True)

args = parser.parse_args()

with open('grioblog.txt') as f:
    t = f.readlines()
    t.append(post)

with open('grioblog.txt', 'w') as f:
    f.writelines(t)

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('rio.pink')

scp = SCPClient(ssh.get_transport())
