import socket
from threading import Thread

ip_address = "127.0.0.1"
port = 8000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

nickname = input("Choose your nickname: ")
client.connect((ip_address,port))
print("Connected to the server")
def receive():
    while True:
        try:
            msg=client.recv(2048).decode("utf-8")
            if msg=="NICKNAME":
                client.send(nickname.encode("utf-8"))
            else:
                print(msg)
        except:
            print("An error occured!")            
            client.close()
            break

def write():
    while True:
        msg="{}:{}".format(nickname,input(""))
        client.send(msg.encode("utf-8"))

recv_thread = Thread(target=receive)
recv_thread.start()
write_thread = Thread(target=write)
write_thread.start()