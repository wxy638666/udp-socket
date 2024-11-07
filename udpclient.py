import socket
def send_file_request(client_socket, client_ip, client_port, fileName):
    client_socket.sendto(fileName.encode(), (client_ip, client_port))#首先将传入的文件名 fileName 通过 encode() 方法编码为字节流形式，然后使用客户端套接字 client_socket 的 sendto() 方法将编码后的文件名发送到指定的服务器地址（由 client_ip 和 client_port 组成的元组）.
    client_T, sendAddress = client_socket.recvfrom(2048)#发送完文件名后，通过客户端套接字 client_socket 的 recvfrom() 方法接收服务器发送回来的响应数据,最多接收 2048 字节的数据.
    re = int(client_T.decode())#将接收到的以字节流形式的服务器响应数据先通过 decode() 方法解码为字符串形式，然后再使用 int() 函数将其转换为整数类型.
    return re
def receive_file(client_socket, fileName):
    recv_data, serverAddress = client_socket.recvfrom(2048)
    with open(fileName, "wb") as f:#使用 with 语句以二进制只写模式（wb）打开本地文件，文件名由传入的 fileName 指定.
        print("开始接收")
        f.write(recv_data)#通过文件对象 f 的 write() 方法将接收到的文件数据写入到打开的本地文件中.
        print("-----接受成功-----")
if __name__ == "__main__":
    client_ip = '172.26.150.115'#定义了服务器的 IP 地址
    client_port = 12000#定义了服务器的端口号
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fileName = input("文件名字：")
    response = send_file_request(client_socket, client_ip, client_port, fileName)#调用 send_file_request 函数，向服务器发送文件名请求，并接收服务器关于文件是否存在的响应，将响应值赋给变量 response。
    if response == 0:
        print("找不到该文件")
    else:
        receive_file(client_socket, fileName)

    client_socket.close()