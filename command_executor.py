import subprocess

def comm(cmd):
    process = subprocess.run(cmd,capture_output=True,text=True,shell=True)
    if process.returncode == 0:
        op = process.stdout.strip()
        return op