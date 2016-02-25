import socket

print "[*] STARTING SERVER [*]"
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
print "\t host: " + host
print "\t port: ", port
serversocket.bind((host, port))
private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIBOQIBAAJAZnbBl0a6kuXVcKumeREIpa92v/B9yJVLPnFjdZ+SeTwB30s5ElUH\nGSY2NQDN9kcTm9aJIIya1WxfOa3Ovn/RiwIDAQABAkAXZnGp0a5UVAbdt2XKalh2\nNk9BYHPpdib7+LtFJo81/nNUI1tol3JZoyOlx0OhyP8O5PZQJbr9NmOFNj/eo+7x\nAiEApb1vG5cyAyywqEQPUEwnbylzOpQP9h7/T9zFUUIIrIkCIQCeQ7bwLC+SJPsD\nsEYDZvYdplVUPh1AGynyg8pIWFPQcwIgLTMxZvPf9s+sSedtybdLFdzXCQWyKKwh\nctVBlryMgwkCIG0L8yyhBVYJLPtppZQKiWH8jaax9a2KCekTbXlTgsyJAiEAiR+o\nc0IjnGXYsUB1q11aMqTa614FXq8wxGioJtgN/90=\n-----END RSA PRIVATE KEY-----'
serversocket.listen(5)
while 1:
    (clientsocket, address) = serversocket.accept()
    print ("[+] client connected [+]")
    data = clientsocket.recv(1024).decode()
    if data == 'a':
        r='-----BEGIN PUBLIC KEY-----\nMFswDQYJKoZIhvcNAQEBBQADSgAwRwJAZnbBl0a6kuXVcKumeREIpa92v/B9yJVL\nPnFjdZ+SeTwB30s5ElUHGSY2NQDN9kcTm9aJIIya1WxfOa3Ovn/RiwIDAQAB\n-----END PUBLIC KEY----'
        clientsocket.send(r.encode())
    elif data == 'b':
        clientsocket.send(private_key.encode())
