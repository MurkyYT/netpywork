import socket
from threading import Thread
from .sequence_manager import sequence_manager
from .utils import *

class client:
    def __init__(self,ip: str,port: int) -> None:
        self.ip: str = ip
        self.port: int = port
        self.my_port: int = -1
        self.on_receive = None
        self.on_connect = None

        self.__tcp_socket: socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.__udp_socket: socket.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        self.__tcp_thread: Thread = None
        self.__udp_thread: Thread = None

        self.__seq_manager: sequence_manager = sequence_manager()
        self.__udp_seq = 0
        self.__is_running = False
    def connect(self):
        self.__is_running = True
        self.__tcp_thread = Thread(target=self.__run_tcp)
        self.__tcp_socket.connect((self.ip,self.port))
        self.__tcp_thread.start()
        self.my_port = self.__tcp_socket.getsockname()[1]
        server_address = self.__tcp_socket.getpeername()
        self.__seq_manager.add_addr(server_address)

        self.__udp_thread = Thread(target=self.__run_udp)
        self.__udp_socket.bind(('',self.my_port))
        self.__udp_socket.settimeout(1)
        self.__udp_thread.start()
        if(self.on_connect):
            self.on_connect(server_address)
    def close(self):
        self.__is_running = False
        server_address = self.__tcp_socket.getpeername()
        self.__tcp_socket.close()
        self.__tcp_thread.join()
        self.__seq_manager.delete_addr(server_address)

        self.__udp_thread.join()
        self.__udp_socket.close()
    def send_reliable(self,msg: bytes):
        utils.send_tcp(self.__tcp_socket,msg)
    def send_unreliable(self,msg: bytes):
        msg_len = len(msg)
        if(msg_len <= utils.MAX_UDP_PACKET_SIZE):
            utils.send_udp(self.__udp_socket,self.my_port,(self.ip,self.port),msg,self.__udp_seq,True)
        else:
            parts = []
            while (len(msg) > utils.MAX_UDP_PACKET_SIZE):
                parts.append(msg[0:utils.MAX_UDP_PACKET_SIZE])
                msg = msg[utils.MAX_UDP_PACKET_SIZE:]
            parts.append(msg)
            for i in range(len(parts)):
                utils.send_udp(self.__udp_socket,self.my_port,(self.ip,self.port),parts[i],self.__udp_seq, i == len(parts) - 1)
        self.__udp_seq += 1
    def __run_udp(self):
        while self.__is_running:
            try:
                message: udp_msg = utils.read_udp_msg(self.__udp_socket)
                self.__seq_manager.add_seq(message.address,message.seq_no,message.data)
                if(message.is_end):
                    # TODO : move to logging
                    # print("UDP",)
                    if(self.on_receive):
                        self.on_receive(self.__seq_manager.get_result(message.address,message.seq_no),protocol.UDP)
            except:
                continue
    def __run_tcp(self):
        while self.__is_running:
            try:
                message: tcp_msg = utils.read_tcp_msg(self.__tcp_socket)
                # TODO : move to logging
                #print("TCP",message.data)
                if(self.on_receive):
                        self.on_receive(message,protocol.TCP)
            except:
                continue