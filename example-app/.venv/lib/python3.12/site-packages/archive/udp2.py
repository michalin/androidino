import socket

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '0.0.0.0'
port = 50007

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))


while True:
    data, address = ServerSocket.recvfrom(2048)
    data_str = data.decode('utf-8')
    try:

        # print(f"data : {data_str}, address : {address}")
        print(f'data received: {data_str}')

    except:
        print(f"invalid value, data : {data_str}, address : {address}")

    if not data:
        print("no data")
        break

connection.close()
