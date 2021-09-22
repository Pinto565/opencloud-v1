import random
import subprocess

def port_allocation():

    def randomport():
        num = random.randint(5999,6999)
        if checkport(num) == True:
            return num
        else:
            randomport()

    def checkport(port):
        cmd = f"netstat -an | grep {port}"
        process = subprocess.run(cmd,shell=True,capture_output=True,text=True)
        op = process.stdout.split()
        if len(op) == 0:
            return True
        else:
            return False

    allocated_port = randomport()
    return allocated_port