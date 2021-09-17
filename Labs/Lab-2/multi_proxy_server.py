import socket, time, sys
from multiprocessing import Process

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )

    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(conn, addr, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)

    print(f"Sending Data to google")

    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    Recvdata = proxy_end.recv(BUFFER_SIZE)

    print(f"Sending Data  to client")

    conn.send(Recvdata)

def main():
    host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as proxy_start:
        print("Starting Server ...")

        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print(f"Connected to:", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print(f"Connecting to Google")
                
                remote_ip = get_remote_ip(host)
                proxy_end.connect((remote_ip, port))
                Process(target = handle_request, args=(conn, addr, proxy_end)).start()
                
                print(f"Starting to multi-processes")
                
            conn.close()
if __name__ == "__main__":
    main()