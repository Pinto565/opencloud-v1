import subprocess
import random

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

print("  Welcome to OpenCloud  ")
cmd = subprocess.run("pwd",capture_output=True,text=True,shell=True)
directory = cmd.stdout.strip()
directory = f"{directory}/deployments"
cmd = subprocess.run(f"mkdir {directory}",capture_output=True,text=True,shell=True)
print("Directory Created")
git_url = input("Enter the Git URL > ")
print("Cloning the Github Repository")
try:
    cmd = subprocess.run(f"cd {directory} && git clone {git_url}",capture_output=True,text=True,shell=True)
    print("Repository Cloned")
    words = git_url.split('/')
    folder = (words[len(words)-1].replace(".git",""))
    git_directory = (f"{directory}/{folder}")
except:
    print("Repository Cloning Failed")
print("Creating Virtual Python Environment")
try:
    cmd = subprocess.run(f"cd {git_directory} && python3 -m venv venv",capture_output=True,text=True,shell=True)
    print("Virtual Environment Created..")
except:
    print("Virtual Environment Failed")
print("Activating Virtual Environment..")
try:
    cmd = subprocess.run(f"cd {git_directory} && source venv/bin/activate",capture_output=True,text=True,shell=True)
    print("Virtual Environment Activated...")
except:
    print("Activation of Virtual Environment Failed..")
print("Installing Dependencies..")
try:
    cmd = subprocess.run(f"cd {git_directory} && {git_directory}/venv/bin/pip3 install -r {git_directory}/requirements.txt",capture_output=True,text=True,shell=True)
except:
    print("Installation Failed..")
try:
    with open(f"{git_directory}/entrypoint") as file:
        list = file.read().split()
        print(len(list))
        if len(list) == 2:
            arg1 = list[0].replace(list[0],f"{git_directory}/venv/bin/{list[0]}")
            arg2 = list[-1]
            entrypoint = (f"{arg1} {arg2}")
        if len(list) == 4:
            arg1 = list[0].replace(list[0],f"{git_directory}/venv/bin/{list[0]}")
            arg2 = list[-1]
            if checkport(5995) == True:
                entrypoint = (f"{arg1} {list[1]} {list[2]} {arg2}")
                entrypoint = (f"cd {git_directory} && {entrypoint} --daemon")
                print("Starting Your Application...")
                print("Your Application Will be Running On 192.168.1.105:5995")
                cmd = subprocess.run(entrypoint,shell=True)
            else:
                port = str(randomport())
                entrypoint = (f"{arg1} {list[1]} {list[2]} {arg2}").replace("5995",port)
                entrypoint = (f"cd {git_directory} && {entrypoint} --daemon")
                print("Starting Your Application...")
                print(f"Your Application Will be Running On 192.168.1.105:{port}")
                cmd = subprocess.run(entrypoint,shell=True)
except:
    print("Application Failed..")