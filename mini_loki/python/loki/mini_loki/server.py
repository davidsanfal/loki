import socket


def server(ip="172.16.17.210", port=5033):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    client, _ = server.accept()
    client.settimeout(2)
    while True:
        try:
            client.send(bytes("Hello World!\n", 'UTF-8'))
            msg = client.recv(1024)
            print(msg)
        except socket.timeout:
            break
        except socket.error:
            break
        except KeyboardInterrupt:
            break
    server.close()

if __name__ == '__main__':
    server(ip='172.16.17.210')
