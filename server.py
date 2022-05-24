import threading
import socket
from time import sleep
from sys import exit


class Server:
    def __init__(self):
        self.host = input("Enter Host: ")
        self.port = input("Enter Port: ")
        self.port = int(self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.connected_users = []
        self.connected_socks = []       
        self.start()
        
    def start(self):
        try:
            self.sock.bind((self.host, self.port))
            self.running = True
            print(f"[+] Server Started On {self.host} : {str(self.port)}")
            self.connection_handler()
        except:
            print("[!] Server Failed To Start! Terminating...")
            sleep(2)
            exit(0)
            
    def connection_handler(self):
        while self.running:
            try:
                self.sock.listen()
                conn, addr = self.sock.accept()
                self.connected_socks.append(conn)
                client_nickname = conn.recv(1024).decode('utf-8')
                self.connected_users.append(client_nickname)
                print(f"[+] {client_nickname} Connected From {addr}")
                greeting = f"[SERVER]: {client_nickname} has connected.\n".encode('utf-8')
                self.broadcast(greeting)
                threading.Thread(target=lambda: self.message_handler(conn)).start()
            except:
                print(f"[!] {client_nickname} | {addr} Has Disconnected")
                
    def broadcast(self, message):
        for conn in self.connected_socks:
            conn.sendall(message)
            
            
    def message_handler(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                
                if data:
                    print(data)
                    new_data = data.encode('utf-8')
                    self.broadcast(new_data)
            except:
                pass
                
                
if __name__ == '__main__':
    Server()