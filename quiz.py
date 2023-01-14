import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address= '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()

list_of_clients = []
nicknames=[]
answers = ["pasty","farhenheit"]
questions = [
" What is the italian word for PIE? \n a)Mozeralla\n b)Pasty\n c)pizza\n d)patty\n",
"Water boils at 212 units at which scale? \na)Kelvin\n b)Celcius\n c)Farhenheit\n d)Rankine"


]

def clientThread(conn,addr):
    score = 0
    conn.send("Welcome to the quiz game!".encode("utf-8"))
    conn.send("You will recieve a question. The answer will be in option a,b,c or d\n\n".encode("utf-8"))
    conn.send("Good luck!\n".encode("utf-8"))
    answer =""
    index,question = get_random_question_answer(conn,answer)

    while True:
        try:
            msg = conn.recv(2048).decode("utf-8")
            if msg:
            
                if msg.lower()==answer:
                    score+=1
                    conn.send("Bravo your answer is correct. Your score is {score}\n\n".encode("utf-8"))
                else:
                    conn.send("Incorrect answer!! Better luck next time!".encode("utf-8")) 
                    conn.send("the anwer is: {answer}".encode("utf-8"))
                    remove_nickname(nickname)   
            else:
                remove(conn)        
            remove_question(index)   
            index,question = get_random_question_answer(conn)   
        except:
            continue



def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

    
def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def get_random_question_answer(conn,answer):
    random_index = random.randint(0,len(questions)-1)
    random_question= questions[random_index]
    random_answer = answers[random_index]
    random_answer = answer
    
    conn.send(random_question.encode("utf-8"))
    return random_index,random_question




while True:
    conn,addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
   
    print(nickname+" connected")

    new_thread = Thread(target=clientThread,args=(conn,addr))
    new_thread.start()