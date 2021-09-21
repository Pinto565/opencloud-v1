import random , string

conf_file = "/etc/haproxy/haproxy.cfg"

def random_code():
    characters = string.ascii_letters
    code = ''.join(random.choice(characters) for i in range(8))
    return code

def write_conf(port,device,dev_port):
  file = open(conf_file, "a")
  id = random_code()
  # file.truncate(0)
  file.write(f"\n\nfrontend front_{id}")
  file.write(f"\n   bind {id}.node.opencloud.world:{port}")
  file.write(f"\n   default_backend back_{id}")
  file.write(f"\nbackend back_{id}")
  file.write(f"\n   balance      roundrobin")
  file.write(f"\n   server {id}      {device}:{dev_port} check\n")
  file.close()