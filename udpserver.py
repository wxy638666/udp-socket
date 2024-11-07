import socket
def handle_file_request(server_socket):
    print("接受文件名中")
    fileName, clientAddress = server_socket.recvfrom(2048)#通过传入的 UDP 套接字对象 server_socket 的 recvfrom() 方法接收客户端发送的数据。最多接收2048字节地数据。
    fileName_decode = fileName.decode("utf-8")#将接收到的以字节流形式的文件名进行解码，转换为字符串形式。
    print("寻找", fileName_decode, "文件")
    try:
        with open(fileName_decode, "rb") as f:#使用 with 语句以二进制只读模式（rb）打开客户端请求的文件，当文件成功打开后，会得到一个文件对象 f。
            server_socket.sendto(b"1", clientAddress)#在文件成功打开后，通过 UDP 套接字 server_socket 向客户端发送一个字节串 b"1"，这可以看作是给客户端发送一个信号，表示文件已经找到且准备好进行发送。
            data = f.read()#通过文件对象 f 的 read() 方法读取整个文件的内容。
            print("开始发送")
            server_socket.sendto(data, clientAddress)#将读取到的文件数据通过 UDP 套接字 server_socket 发送给客户端，发送的目标地址就是之前接收文件名时获取到的客户端地址 clientAddress。
            print("-----发送完成-----")
    except FileNotFoundError:
        print("-----找不到该文件-----")
        server_socket.sendto(b"0", clientAddress)#在文件不存在的情况下，通过 UDP 套接字 server_socket 向客户端发送一个字节串 b"0"
if __name__ == "__main__":
    server_port = 12000#定义服务器要监听的端口号为 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', server_port))#创建了一个基于 UDP 协议的套接字对象。

    while True:
        handle_file_request(server_socket)