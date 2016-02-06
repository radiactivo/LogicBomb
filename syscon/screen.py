import SocketServer
import socket
import sys
from os import environ
import base64

class pyscreenlistener(SocketServer.StreamRequestHandler):
	def handle(self):
		#print "waiting for screenshot..."
		self.data = self.rfile.readline().strip()
		self.dx = self.data.split("?")
		if self.dx[0] == "0":
		    print "screenshot received..."
		    dta = base64.b64decode(self.dx[1])
		    print "data decoded..."
		    pth = pyscreenmanager.path + "\\client_screen" + str(pyscreenmanager.imgnum) + ".jpg"
		    print "write data to " + pth
		    fobj = open(pth, "w+b")
		    fobj.write(dta)
		    fobj.close()
		    print "data written..."
		    pyscreenmanager.imgnum += 1
		else:
		    dbg = pyscreenmanager.debug_mode
		    self.data = self.rfile.readline().strip()
		    pth = environ.get("TEMP") + "\\screen.jpeg"
		    if dbg == True: print "recvd:" + self.data
		    dta = base64.b64decode(self.dx[1])
		    if dbg == True: print "encdd"
		    fobj = open(pth, "w+b")
		    fobj.write(dta)
		    if dbg == True: print "wrttn"
		    fobj.close()

class pyscreenmanager:
	global imgnum
	global path
	global debug_mode



if __name__ == "__main__":
	HOST, PORT = socket.gethostname(), 56000
	pth = environ.get("APPDATA")
	if len(sys.argv) > 1:
		#PORT = int(sys.argv[1])
		pth = sys.argv[1]
	else:
		# no args given:
		#PORT = int(raw_input("Enter port number: "))
		pth = raw_input("Enter path (screenshot command)[raw string]: ")
	if len(sys.argv) > 2:
		pth = sys.argv[1]
		PORT = sys.argv[2]
	
	pyscreenmanager.debug_mode = False
	if pth[0] == "?":
		pth = pth[1:]
		pyscreenmanager.debug_mode = True
	pyscreenmanager.imgnum = 0
	pyscreenmanager.path = pth
	
	server = SocketServer.TCPServer((HOST, PORT), pyscreenlistener)
	
	print HOST, PORT, pyscreenmanager.imgnum, pyscreenmanager.path
	
	server.serve_forever()
