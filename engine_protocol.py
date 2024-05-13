import os
import random
import socket

class EngineProtocol:
    def __init__(self, portNo: int):
        self.pathToBinary = "./c_engine/engine"
        self.config = ""
        self.host = "127.0.0.1"
        self.port = portNo
        # self.start_engine()

    def start_engine(self) -> None:
        if not os.path.exists(self.pathToBinary):
            raise FileNotFoundError(f"Engine not found: {self.pathToBinary}")
        self.port = random.randint(2000, 49151)
        os.system(f"{self.pathToBinary} {self.port} &")

    def get_moves(self) -> str:
        return self.send_req("get_legal_moves")

    def get_best_move(self) -> str:
        return self.send_req("get_best_move")

    def load_fen(self, fen: str) -> str:
        return self.send_req(f"load_fen {fen}")

    def undo_move(self) -> str:
        return self.send_req("undo_move")

    def clear(self) -> str:
        return self.send_req("clear")

    def perform_move(self, move: str) -> str:
        return self.send_req(f"perform_move {move}")

    def send_req(self, req: str) -> str:
        req += " " * (1023 - len(req))
        # print(f'trying to send req: {req}')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(req.encode())
            data = s.recv(1024)
            # print(f'response: {data.decode()}')
        return data.decode()

