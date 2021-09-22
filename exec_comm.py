import subprocess

def comm(cmd):
    process = subprocess.run(cmd,capture_output=True,text=True,shell=True)
    op = process.stdout.strip()
    return op