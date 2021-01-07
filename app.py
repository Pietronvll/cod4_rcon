import socket
import multiprocessing
import time
from os import listdir
from os.path import isfile, join

_DEV = False
 
def run():
    print("COD 4 Rcon Utility --- ")
    #connect xx.xx.xx.xx:xxxxx; password xxxx; rcon login xxxxxxxx
    raw_str = input("Connection command:")
    address, port, rcon_pw = format_string(raw_str)
    server = UDP_handler(address,port,rcon_pw)
    configs = load_configs()
    config_idx = int(input("Which config you want to load? "))
    server.execute(configs[config_idx - 1])
    if _DEV:
        server.listen()
    return

def format_string(raw_str):
    cmds = raw_str.split(';')
    address, port = cmds[0].split(' ')[1].split(':')
    rcon_pw = cmds[2].split(' ')[3]
    port = int(port)
    return address, port, rcon_pw

def load_configs():
    path = 'configs'
    cfg_files = [ f.split(".") for f in listdir(path) if isfile(join(path, f))]
    for idx, f in enumerate(cfg_files):
        print(f" [ {idx + 1} ] ~ {f[0]}")
    return cfg_files

class UDP_handler:
    def __init__(self, address, port, rcon_pw):
        self.UDP_Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_Client.settimeout(10)
        self.address = (address, port)
        self.rcon_pw = rcon_pw
        self.bufferSize = 4086

    def send_message(self, message):
        try:
            # Send data
            in_message = b"\xFF\xFF\xFF\xFF" + f"rcon {self.rcon_pw} ".encode() + message.encode()
            self.UDP_Client.sendto(in_message, self.address)
        except Exception as e:
            print(e)

    def listen(self):
        while True:
            try:
                out_message = self.UDP_Client.recvfrom(self.bufferSize)
                print(out_message[0].decode('utf-8', 'ignore'))
            except socket.timeout:
                break

    def execute(self, fname):
        path = "configs/" + fname[0] + "." + fname[1]
        f = open(path, "r")
        commands = f.read().splitlines() 
        for cmd in commands:
            self.send_message(cmd)

if __name__ == "__main__":
    run()

