from datetime import datetime
import hashlib
import os
import socket
import threading
import time

absolute_path = os.path.dirname(__file__)
SERVER_DATA_PATH = "client_data"
absolute_path = os.path.join(absolute_path,SERVER_DATA_PATH)

IP = socket.gethostbyname(socket.gethostname()) #'192.168.64.2'
print(IP)
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def thread_cod(i,data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    now = datetime.now()
    name_filelog=f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}-log.txt"
    global path_log 
    path_log=os.path.join(os.path.dirname(__file__), "logs_cliente")
    path_log=os.path.join(path_log, name_filelog)
    while True:
        data = client.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd=data[0]

        if cmd == "OK":
            msg=data[1]
            print(f"{msg}")

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            data = client.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]
            if cmd == "DISCONNECTED":
                msg=data[1]
                print(f"[SERVER]: {msg}")
                break
        
        elif cmd == "SEND":
            try:
                start_time = time.time()
                print(name_filelog)
                name= client.recv(SIZE).decode(FORMAT) # recibe el path
                client.send("filename".encode(FORMAT))
                prueba_num= client.recv(SIZE).decode(FORMAT)
                name_file="Cliente"+str(i)+"-Prueba-"+str(prueba_num)+"."+name.split(".")[1]
                hash_s= client.recv(SIZE).decode(FORMAT)
                complete_path=os.path.join(absolute_path,name_file)
                if os.path.exists(complete_path):
                        os.remove(complete_path)
                while True:
                        incomming_msg=client.recv(SIZE).decode(FORMAT)
                        if incomming_msg!="FIN":
                            with open(complete_path, "a") as f: 
                                f.write(incomming_msg)
                        else:
                            with open(complete_path, 'r') as f:
                                text = f.read()
                                sha256_hash = hashlib.sha256()
                                sha256_hash.update(text.encode('utf-8'))
                                hash_c=sha256_hash.hexdigest()
                            if hash_s==hash_c:
                                print("Hash verificado")
                                print("Hash servidor", hash_s)
                                print("Hash cliente", hash_c)
                            else:
                                print("Hash no verificado")
                                print("Hash servidor", hash_s)
                                print("Hash cliente", hash_c)
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            # Log: archivo recibido con exito
                            size_data=os.path.getsize(complete_path)
                            with open(path_log, "a") as f:
                                f.write(f"File {name} received successfully for the Client-{i}\n{elapsed_time} segundos\nFile of {size_data*1e-6} MB\n ") 
                                f.write("\n")
                            send_data = f"OK@File {name} received successfully.@For the Client-{i}@{elapsed_time} segundos"
                            client.send(send_data.encode(FORMAT))
                            break
            except Exception:
                    size_data_error=os.path.getsize(complete_path)
                    with open(path_log, "a") as f: 
                            f.write("SERVER-CLIENT CONECTION ERROR: The file managed to send " + str(size_data_error*1e-6)+ " MB para el cliente "+str(i)+"\n")
        if cmd == "STOP":      
            print("Disconnected from the server.")
            client.close()
            os._exit(os.EX_OK)
    client.close()
def main():
    print("Ponga la cantidad de clientes que desea conectar")
    while True:
            data = int(input())
            data+=1
            for i in range(1,data):
                thread = threading.Thread(target=thread_cod, args=(i,data))
                thread.start()
if __name__ == "__main__":
    main()