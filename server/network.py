import socket
class cod4server:
    def __init__(self,address, port, rcon_pw):
        self.UDP_Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       
        self.UDP_Client.settimeout(1.5)
        self.address = (address, port)
        self.rcon_pw = rcon_pw
    def send_message(self, message):
        try:
            # Send data
            in_message = b"\xFF\xFF\xFF\xFF" + f"rcon {self.rcon_pw} ".encode() + message.encode()
            self.UDP_Client.sendto(in_message, self.address)
            # Receive response       
            data = ''
            incomplete_data = True
            while incomplete_data:
                try:
                    out_message = self.UDP_Client.recv(2**12)
                    data += out_message.decode('utf-8', 'ignore')
                except socket.timeout:
                    incomplete_data = False
            print(f'{self.address[0]}:{self.address[1]} ~ \n {data[6:]}')
        except Exception as e:
            print(e)
    def execute(self, fname):
        path = "configs/" + fname[0] + "." + fname[1]
        f = open(path, "r")
        commands = f.read().splitlines() 
        for cmd in commands:
            self.send_message(cmd)

    @property
    def is_alive(self):
        in_message = b"\xFF\xFF\xFF\xFF" + f"rcon {self.rcon_pw} ".encode() + ''.encode()
        self.UDP_Client.sendto(in_message, self.address)
        try:
            out_message = self.UDP_Client.recv(2**12)
            return True
        except socket.timeout:
            return False
        except:
            print("Unknown error")