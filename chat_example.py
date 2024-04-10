import netpywork as networking

def client_on_receive(msg,proto,self: networking.client):
    print(msg.data.decode())
def client_on_connect(address,self:networking.client):
    print("Successfully connected")
def server_on_receive(msg,proto,self: networking.server):
    print(f"Received {msg.data}")
    self.send_all(msg.data,exceptions=[msg.address])
def server_on_connect(address,self:networking.server):
    print(f'{address} connected')
def server_on_disconnect(address,self:networking.server):
    print(f'{address} disconnected')
def run_server():
    server = networking.server(12345)
    server.on_receive = server_on_receive
    server.on_connect = server_on_connect
    server.on_disconnect = server_on_disconnect
    server.run()
def run_client():
    client = networking.client('localhost',12345)
    client.on_receive = client_on_receive
    client.on_connect = client_on_connect
    client.connect()
    name = input("Enter name: ")
    while True:
        message = input("")
        client.send(f"[{name}]: {message}".encode())
def main():
    if(input("Are you the server? (y\\n)").lower().strip() == "y"):
        run_server()
    else:
        run_client()
if (__name__ == "__main__"):
    main()