from pyvpn import *
from ip_addr import *
from op_python import *


print("  Welcome to OpenCloud  \n")
print("1.Add Your Device\n2.Get Available Devices\n3.Deploy a Flask Application")
option = int(input("Enter the option > "))
if option == 1:
    gen_cert()
elif option ==2 : 
    available_devices()
# else:
    # op_flask()