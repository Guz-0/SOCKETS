import socket
import threading
import multiprocessing as mp
import errno

SERVER_IP = '192.168.1.3'
PORT = 5050
MSG_LEN = 1024
ADDRESS = (SERVER_IP,PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

thread_idx = 0
threads_list = []

def PrintThreadCount():
    threadCount = threading.active_count()
    print(f"[CURRENT NUMBER OF THREADS: {threadCount - 1} ]")

def JoinThread(thread):
    thread.join()

def HandleClient(communication, thread_idx):

    communication.setblocking(0)
    communication.send("[YOU CONNECTED TO THE SERVER]".encode('utf-8'))
    firstConnection = False

    while True:
        
        try:
            msg = communication.recv(1024).decode('utf-8')
            if(msg):
                print(msg)
            if(not msg):
                print("CONNECTION CLOSED")
        except socket.error as e:
            if e.errno == errno.WSAECONNRESET:
                communication.close()
                print("[CONNETCTION CLOSED WITH CLIENT]")
                PrintThreadCount()
                break
                



def ServerListen(thread_idx):

    while True:
        try:
            print("[SERVER WAITING]")
            communication, addr = server.accept()
            print(f"{addr} Just connected!")
            
            thread_idx = thread_idx + 1
            tSend = threading.Thread(target=HandleClient, args=(communication, thread_idx))
            tSend.start()
            

            threads_list.append(tSend)
            

            PrintThreadCount()
            
        except Exception as e:
            print(f"[ERROR_MAIN --> {e}]")

ServerListen(thread_idx)
