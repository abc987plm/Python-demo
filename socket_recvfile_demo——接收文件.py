from socket import *

fd = socket(AF_INET, SOCK_STREAM, 0)
fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
fd.bind(('192.168.235.132', 9000))
fd.listen(5)
while True:
    conncet, addr = fd.accept()
    data = conncet.recv(128)
    file = open(data.decode(),'wb')
    num = 1
    while data:
        data = conncet.recv(1024)
        print(data)
        if data:
            file.write(data)
            conncet.send('接收{}行'.format(num).encode())
            num += 1
    conncet.close()
    file.close()
# fd.close()