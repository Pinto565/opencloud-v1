import subprocess
cmd = subprocess.run("ls",capture_output=True,shell=True,text=True)
print(cmd.stdout.strip())