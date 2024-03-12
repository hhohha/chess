import os
import socket

class EngineProtocol:
    def __init__(self):
        self.pathToBinary = "./c_engine/engine"
        self.config = ""
        self.host = "127.0.0.1"
        self.port = 8080
        if not os.path.exists(self.pathToBinary):
            raise FileNotFoundError(f"Engine not found: {self.pathToBinary}")
        self.start_engine()

    def start_engine(self) -> None:
        os.system(f"{self.pathToBinary} &") # TODO - send the port number

    def get_moves(self) -> str:
        return self.send_req("get_moves")

    def load_fen(self, fen: str) -> None:
        self.send_req(f"load_fen {fen}")

    def clear(self) -> str:
        return self.send_req("clear")

    def send_req(self, req: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(req.encode())
            data = s.recv(1024)
        return data.decode()

