import random , string

conf_file = "/etc/haproxy/haproxy.cfg"

def random_code():
    characters = string.ascii_lowercase
    code = ''.join(random.choice(characters) for i in range(8))
    return code

def write_http_conf(device,dev_port):
  file = open(conf_file, "a")
  id = random_code()
  # file.truncate(0)
  public_add = f"{id}.node.opencloud.world"
  file.write(f"\nbackend {public_add}")
  file.write(f"\n   server {id}      {device}:{dev_port}\n")
  file.close()
  return public_add

def write_ssh_conf(device,dev_port):
  file = open(conf_file, "a")
  id = random_code()
  # file.truncate(0)
  public_add = f"{id}.node.opencloud.world"
  file.write(f"\n\nfrontend front_{id}")
  file.write(f"\n   mode tcp")
  file.write(f"\n   bind {public_add}:8022")
  file.write(f"\n   use_backend back_{id}")
  file.write(f"\nbackend back_{id}")
  file.write(f"\n   server {id}      {device}:{dev_port}\n")
  file.close()
  return public_add