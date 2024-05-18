class Data:
    def __init__(self, data, ip) -> None:
        self.data = data
        self.ip = ip

class Server:
    ip = 0
    IP = 0

    def __new__(cls, *args, **kwargs) -> None:
        cls.IP += 1
        return super().__new__(cls)

    def __init__(self) -> None:
        self.ip = Server.IP
        self.buffer = []
        self.router = None

    def send_data(self, data: Data) -> None:
        self.router.buffer.append(data)
        self.buffer.clear()

    def get_data(self) -> list:
        data = self.buffer.copy()
        self.buffer.clear()
        return data

    def get_ip(self) -> int:
        return self.ip

    buffer = []
    router = None


class Router:
    def link(self, server: Server) -> None:
        self.servers.append(server)
        server.router = self

    def unlink(self, server: Server) -> None:
        if server in self.servers:
            self.servers.remove(server)

    def send_data(self) -> None:
        for data in self.buffer:
            for server in self.servers:
                if server.get_ip() == data.ip:
                    server.buffer.append(data)
        self.buffer.clear()

    servers = []

    buffer = []
