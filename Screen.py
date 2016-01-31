import syscon.control

con = syscon.control.Connection("XYZ")
# This defines con as a connection with the Computer in the network which
# has the name XYZ over port 51000. If you want to use another port, use
# the second parameter, e.g. for port 9999:
# con = syscon.control.Connection("XYZ", 9999)
# In case you do this, you must start the client.pyw
# on the remote machine with the port number as parameter

# Now send orders with con.send (next section)
# Usage of con.send: con.send(command[, second_param[, third_param]])
con.send(download())

con.close()
# This immediately stops the connection and closes the client.pyw
# on the other computer. You could also use con.send("stopcontrol")
