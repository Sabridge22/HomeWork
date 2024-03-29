class Data:
    def __init__(self, data, ip) -> None:
        self.data = data
        self.ip = ip

    data = ""
    ip = 0


class Server:
    ip = 0
    IP = 0

    def __new__(cls, *args, **kwargs):
        cls.IP += 1
        return super().__new__(cls)

    def __init__(self):
        self.ip = Server.IP
        self.buffer = []

    def send_data(self, data: Data):
        self.router.buffer.append(data)

    def get_data(self):
        return self.buffer

    def get_ip(self):
        return self.ip

    buffer = []
    router = []


class Router:
    def link(self, server: Server):
        self.servers.append(server)
        server.router.append(self)

    def unlink(self, server: Server):
        if server in self.servers:
            self.servers.remove(server)

    def send_data(self):
        for i in self.servers:
            i.buffer += self.buffer
        self.buffer.clear()

    servers = []

    buffer = []
