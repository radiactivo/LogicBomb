# -*- coding: cp1252 -*-
import socket
import sys
import sysconx.crypto
import random

class Connection(object):
    def __init__(self, computername, port = 51000):
        self.__computer = computername
        self.__ip = socket.gethostbyname(computername)
        self.__port = port
        self.__key, self.__iv = self.getkey()
        #print "KY:", self.__key, "IV:", self.__iv
        print "AES encrypted Connection object to " + computername + " (IP " + socket.gethostbyname(computername) + ") on port " + str(port)
    def getkey(self):
        alphas = []
        onum = []
        alphaivs = []
        onumiv = []
        alpha = ""
        alphaiv = ""
        for i in range(16):
            x = random.randint(0, 127)
            y = random.randint(0, 127)
            alphas.append(int(sysconx.crypto.DHMSend(x, 7, 127)))
            alphaivs.append(int(sysconx.crypto.DHMSend(y, 7, 127)))
            onum.append(x)
            onumiv.append(y)
        for i in alphas:            
            alpha += str(i) + ";"
        alpha = alpha.rstrip(";")
        for i in alphaivs:            
            alphaiv += str(i) + ";"
        alphaiv = alphaiv.rstrip(";")
        send = "§§" + alpha + "&" + alphaiv
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__ip, self.__port))
        sock.send(send + "\n")
        #print "ownKey-ownIV-send:", alphas, "-", alphaivs, "-", send
        received = sock.recv(8192)
        #print "recdata:", received
        sock.close()
        beta, betaiv = received.split("&")
        betas = beta.split(";")
        betaivs = betaiv.split(";")
        #print "recKey-recIV:", betas, "-", betaivs
        Key = []
        IV = []
        for K in range(16):
                Key.append(int(sysconx.crypto.DHMReceive(betas[K], onum[K], 127)))
                IV.append(int(sysconx.crypto.DHMReceive(betaivs[K], onumiv[K], 127)))
        #for K in range(16):
        #        Key.append(int(syscon.crypto.DHMReceive(betas[K], alphas[K], 127)))
        #        IV.append(int(syscon.crypto.DHMReceive(betaivs[K], alphaivs[K], 127)))
        return (Key, IV)
    def send(self, command, path = None, url = None, output = True):
        if output == True:
            print "Sending " + command + " with arguments " + str(path) + " and " + str(url) + " to " + self.__computer
        cmd = str(self.getShortCommand(command))
        abort = False
        if int(cmd[0]) in [1,2,6,7]:
            if path is None:
                abort = True
            cmd += "@" + str(path)
        elif int(cmd[0]) == 4:
            if path is None or url is None:
                abort = True
            cmd += "@" + str(path) + "@" + str(url)
        if int(cmd[0]) == 6:
            if url <> None:
                cmd += "@" + str(url)
        if int(cmd[0]) > -1 and abort != True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.__ip, self.__port))
            textlst, olen = sysconx.crypto.aesencrypt(cmd, self.__key, self.__iv)
            text = ""
            for i in textlst:
                text += str(i) + ";"
            text = text.rstrip(";")
            send = text + "§" + str(olen)
            #print "Data to send: " + send
            sock.send(send + "\n")
            if int(cmd[0]) <> 5:
                received = sock.recv(8192)
                dta, origlen = received.split("&")
                data = dta.split(";")
                for i in range(len(data)):
                    data[i] = int(data[i])
                txt = sysconx.crypto.aesdecrypt(data, self.__key, self.__iv, origlen)
                if output == True:
                    print "Client answer: " + txt
            sock.close()
            if int(cmd[0])==6:
                return txt
    def sendMouseEvent(self, e):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__ip, self.__port))
        cmd = e.toString()
        textlst, olen = sysconx.crypto.aesencrypt(cmd, self.__key, self.__iv)
        text = ""
        for i in textlst:
            text += str(i) + ";"
        text = text.rstrip(";")
        send = text + "§" + str(olen)
        #print "Data to send: " + send
        sock.send(send + "\n")
        
    def getShortCommand(self, longcmd):
        cmdlist = ["shutdown","executefile","execpy","logoff","download","stopcontrol","screenshot", "returnvalue", "mouseevent", "newconnect"] #, "stoppyscreen"]
        return cmdlist.index(longcmd)
    def close(self):
        self.send("stopcontrol")
    def screenshot(self):
        self.send("screenshot", "56000")

class MouseEvent(object):
    def __init__(self, cmd, x, y):
        self.cmd = cmd
        self.x = x
        self.y = y
    
    def toString(self):
        return "8@" + self.cmd + ":" + str(self.x) + "," + str(self.y)

    #def fire(self, con):
    #    con.sendMouseEvent(self)
