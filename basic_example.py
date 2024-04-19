"""
Just a basic test of server and client
"""

import netpywork as networking

def server_receive(msg,proto,self:networking.server):
    if(proto == networking.protocol.UDP):
        msg: networking.udp_msg = msg
        print("Server UDP:",msg.length,msg.data,msg.address)
    if(proto == networking.protocol.TCP):
        msg: networking.tcp_msg = msg
        print("Server TCP:",msg.length,msg.data,msg.address)
def server_connect(address,self: networking.server):
    print(f"Client with ip {address} connected")
    print(f"All clients: {self.get_clients()}")
def server_disconnect(address,self: networking.server):
    print(f"Client with ip {address} disconnected")
    print(f"All clients: {self.get_clients()}")
def client_connected(address,self: networking.client):
    print(f"Client conncted to {address}")
def client_receive(msg,proto,self: networking.client):
    if(proto == networking.protocol.UDP):
        msg: networking.udp_msg = msg
        print("Client UDP:",msg.length,msg.data,msg.address)
    if(proto == networking.protocol.TCP):
        msg: networking.tcp_msg = msg
        print("Client TCP:",msg.length,msg.data,msg.address)
def main():
    server = networking.server(12345)
    server.on_receive = server_receive
    server.on_connect = server_connect
    server.on_disconnect = server_disconnect
    client = networking.client('localhost',12345)
    client.on_connect = client_connected
    client.on_receive = client_receive
    
    server.run()
    client.connect()

    server.send_all("HIII".encode())
    server.send_all("HIII2".encode(),exceptions=[client.address])
    client.send_reliable("Hello :)".encode())
    client.send_unreliable(("Hello!!!").encode())
    client.send(("Hello!!!222").encode(),networking.protocol.UDP)
    #TCP is used by default
    client.send(("Hello!!!333").encode())
    server.send_reliable("Hi1".encode(),client.address)
    server.send_unreliable("Hi2".encode(),client.address)
    

    client.close()
    server.close()
    
    input("Press any key to exit...")
if __name__ == "__main__":
    main()