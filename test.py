import networking

def server_receive(msg,proto):
    if(proto == networking.protocol.UDP):
        msg: bytes = msg
        print("Server UDP:",msg)
    if(proto == networking.protocol.TCP):
        msg: networking.tcp_msg = msg
        print("Server TCP:",msg.data)
def server_connect(address):
    print(f"Client with ip {address} connected")
def server_disconnect(address):
    print(f"Client with ip {address} disconnected")
def client_connected(address):
    print(f"Client conncted to {address}")
def client_receive(msg,proto):
    if(proto == networking.protocol.UDP):
        msg: bytes = msg
        print("Client UDP:",msg)
    if(proto == networking.protocol.TCP):
        msg: networking.tcp_msg = msg
        print("Client TCP:",msg.data)
server = networking.server(12345)
server.on_receive = server_receive
server.on_connect = server_connect
server.on_disconnect = server_disconnect
server.run()
client = networking.client('localhost',12345)
client.on_connect = client_connected
client.on_receive = client_receive
client.connect()
port = client.my_port
client.send_reliable("Hello :)".encode())
client.send_unreliable(("Hello!!!").encode())
address = ('127.0.0.1',port)
server.send_reliable("Hi1".encode(),address)
server.send_unreliable("Hi2".encode(),address)
client.close()
server.close()
print("Hi")