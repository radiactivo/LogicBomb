import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
print (host)
print (port)
serversocket.bind((host, port))

serversocket.listen(5)
print ('server started and listening')
while 1:
    (clientsocket, address) = serversocket.accept()
    print ("[+] client connected [+]")
    data = clientsocket.recv(1024).decode()
    print (data)
    r='REceieve
    clientsocket.send(r.encode())
