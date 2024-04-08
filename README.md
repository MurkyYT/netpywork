# netpywork
**netpywork** is a library that makes using tcp and udp server and client easier

# Features
- Creating a server and client which uses `TCP` and `UDP`
- Callbacks for `On Receive`, `On Connect` and `On Disconnect` for server
- Callbacks for `On Receive` and `On Connect` for client
- Sending messages from server to client both with tcp and udp by specifing the address to send to `(see example below)`
- Sending *large* `UDP` messages

# Example
```Python
import netpywork as networking
def server_receive(msg,proto):
    if(proto == networking.protocol.UDP):
        msg: networking.udp_msg = msg
        print("Server UDP:",msg.length,msg.data,msg.address)
    if(proto == networking.protocol.TCP):
        msg: networking.tcp_msg = msg
        print("Server TCP:",msg.length,msg.data,msg.address)
def server_connect(address):
    print(f"Client with ip {address} connected")
def server_disconnect(address):
    print(f"Client with ip {address} disconnected")
def client_connected(address):
    print(f"Client conncted to {address}")
def client_receive(msg,proto):
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
    
    client.send_reliable("Hello :)".encode())
    client.send_unreliable(("Hello!!!").encode())
    server.send_reliable("Hi1".encode(),client.address)
    server.send_unreliable("Hi2".encode(),client.address)
    client.close()
    server.close()
    
    input()
if __name__ == "__main__":
    main()
```