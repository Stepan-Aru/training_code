class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip
        

class Server:
    def __init__(self): 
        self.buffer = []
        self.ip = Router.take_ip()
        self.linked_router = None
        
    def take_data(self, data):
        self.buffer.append(data)
    
    def send_data(self, data):
        self.linked_router.take_data(data)
    
    def get_data(self):
        data = [x for x in self.buffer]
        self.buffer.clear()
        return data

    def get_ip(self):
        return self.ip


class Router:
    given_ip = 0
    def __init__(self):
        self.link_map = {}
        self.buffer = []
        
    def link(self, server):
        self.link_map[server.get_ip()] = server
        setattr(server, "linked_router", self)
    
    def unlink(self, server):
        self.link_map.remove[server.get_ip()]
        setattr(server, "linked_router", None)
    
    def take_data(self, data):
        self.buffer.append(data)
    
    def send_data(self):
        for d in self.buffer:
            self.link_map[d.ip].take_data(d)
        self.buffer.clear()
    
    @classmethod
    def take_ip(cls):
        ip = cls.given_ip
        cls.given_ip += 1
        return ip
