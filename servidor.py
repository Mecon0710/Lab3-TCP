import hashlib
import os
import queue
import socket
import threading
import os
import time
from datetime import datetime
absolute_path = os.path.dirname(__file__)
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
number_threads=queue.Queue()
counter_threads=queue.Queue()
counter_threads.put(0)
data_q=queue.Queue()
barrier = threading.Barrier(10)
barrier_2 = threading.Barrier(10)
n = 1
def producer():
    data = "OK@"
    data += "LIST: List all the files from the server.\n"
    data += "SEND: <number of threads> <relative path example: carpeta/archivo.txt>"
    #data += "HELP: List all the commands."
    while True:
            data = input("> ") 
            data = data.split(" ")
            global cmd
            cmd = data[0]
            if cmd == "SEND":
                try:
                    data_q.put(data)
                    n_threads=int(data[1])
                    global path 
                    path = ""
                    add_path=SERVER_DATA_PATH+"/"+data[2]

                    path = os.path.join(absolute_path, add_path)
                    #Iniciando el archivo
                    now = datetime.now()
                    name_filelog=f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}-log.txt"
                    texto_log=os.path.getsize(path)
                    global path_log 
                    path_log=os.path.join(absolute_path, "logs")
                    path_log=os.path.join(path_log, name_filelog)
                    print(path_log,"path_log")
                    with open(path_log, "a") as f: 
                        f.write(f"El Tamaño del archivo es:{texto_log*1e-6} MB\n")
                    global barrier 
                    barrier= threading.Barrier(n_threads+1)
                    global barrier_2
                    barrier_2= threading.Barrier(n_threads+1)
                    number_threads.put(n_threads)
                    counter_threads.get()
                    counter_threads.put(n_threads)
                    barrier.wait()
                    data_q.get()
                    number_threads.get()
                    counter_threads.get()
                    counter_threads.put(0)
                    barrier_2.wait()       
                except Exception:
                    size_data_error=os.path.getsize(path)
                    with open(path_log, "a") as f: 
                            f.write("SERVER-CLIENT CONECTION ERROR: The file managed to send " + str(size_data_error*1e-6)+ " MB para el cliente "+str(threading.get_ident())+"\n")                
            elif cmd == "LIST":

                files = os.listdir(SERVER_DATA_PATH)
                send_data = ""
                if len(files) == 0:
                    send_data += "The server directory is empty"
                else:
                    send_data += "\n".join(f for f in files)
                print(send_data)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))
    
    while True:
        #data = conn.recv(SIZE).decode(FORMAT)
        #data = data.split("@")
        data= data_q.get() # esto es porque la q esta sincronizada por eso lo puede h hacer
        data_q.put(data)
        
        if cmd=="SEND":
                    try:
                        thread_num=number_threads.get()
                        number_threads.put(thread_num)
                        if thread_num<=threading.active_count() - 2:
                            contador=counter_threads.get()
                            if  contador==0:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                counter_threads.put(0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                            else:
                                counter_threads.put(contador)
                                count=counter_threads.get()
                                count-=1
                                counter_threads.put(count)
                                filename = os.path.basename(path)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                                conn.send(cmd.encode(FORMAT))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                #Envio el filename                                                                                                                                                          
                                conn.send(filename.encode(FORMAT))
                                print("Enviando archivo: ", filename)
                                conn.recv(SIZE).decode(FORMAT) 
                                time.sleep(0.1)
                                #Envio el hash
                                with open(path, 'r') as f:
                                    text = f.read()
                                    sha256_hash = hashlib.sha256()
                                    sha256_hash.update(text.encode('utf-8'))

                                conn.send(f"{sha256_hash.hexdigest()}".encode(FORMAT))

                                time.sleep(0.1)

                                #Envio prueba
                                #conn.send(f"{thread_num}".encode(FORMAT))
                                with open(f"{path}", 'rb') as f:
                                    while True:
                                        block = f.read(SIZE)
                                        conn.send(block)
                                        if not block:
                                            conn.send("FIN".encode(FORMAT))
                                            break                                                           
                                lastmsg= conn.recv(SIZE).decode(FORMAT)
                                lastmsg=lastmsg.split("@")
                                with open(path_log, "a") as f: 
                                    for msg in lastmsg:
                                        f.write(f"{msg}\n")

                                barrier.wait()
                                barrier_2.wait()
                    except Exception:
                        size_data_error=os.path.getsize(path)
                        with open(path_log, "a") as f: 
                            f.write("SERVER-CLIENT CONECTION ERROR: The file managed to send " + str(size_data_error*1e-6)+ " MB para el cliente "+str(threading.get_ident())+"\n")
                            
        elif cmd == "LOGOUT":
            break
        elif cmd == "STOP":      
                print("Disconnected server.")
                os._exit(os.EX_OK) 

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()
    
def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    threadi = threading.Thread(target=producer)
    threadi.start()
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-2}") # -2 porque hay 2 threads que no son clientes?? Que son los threads de producer y main?

if __name__ == "__main__":
    main()