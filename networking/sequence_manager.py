class sequence_manager:
    def __init__(self) -> None:
        self.__messages : dict = {}
    def delete_addr(self,address):
        if(address in self.__messages.keys()):
            del self.__messages[address]
    def add_addr(self,address):
        if(address not in self.__messages.keys()):
            self.__messages[address] = {}
    def add_seq(self,address,seqno,result):
        client_messages = self.__messages[address]
        if(seqno not in client_messages.keys()):
            client_messages[seqno] = result
        else:
            client_messages[seqno] += result
    def get_result(self,address,seqno):
        try:
            result = self.__messages[address][seqno]
            del self.__messages[address][seqno]
            return result
        except:
            return None