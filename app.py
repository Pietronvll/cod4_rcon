from server.network import cod4server
from os import listdir
from os.path import isfile, join

def run():
    print("COD 4 Rcon Utility --- ")
    address = input("Address:")
    rcon_pw = input("Rcon Password:")
    address, port = address.split(":")
    port = int(port)
    server = cod4server(address,port, rcon_pw)
    if server.is_alive:
        print("Succesfully connected")
        configs = load_configs()
        config_idx = int(input("Which config you want to load? "))
        server.execute(configs[config_idx - 1])
        print("Have a nice game!")
        return
    else:
        print("Unable to connect")
        return
def load_configs():
    path = 'configs'
    cfg_files = [ f.split(".") for f in listdir(path) if isfile(join(path, f))]
    for idx, f in enumerate(cfg_files):
        print(f" [ {idx + 1} ] ~ {f[0]}")
    return cfg_files
if __name__ == "__main__":
    run()

