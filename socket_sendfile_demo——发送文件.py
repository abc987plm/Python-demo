from socket import *
from time import sleep
import sys

file = sys.argv[1]
opFile = open(file, 'rb')
sfd = socket(AF_INET, SOCK_STREAM, 0)
sfd.connect(('192.168.235.132', 9000))
sfd.send(file.encode())
sleep(1)
for i in opFile.readlines():
    sfd.send(i)
    re = sfd.recv(1024)
    print(re.decode())

while True:
    data = input('发送完成，请按回车键退出>>>')
    sfd.send(data.encode())
    if not data:
        break

sfd.close()
opFile.close()