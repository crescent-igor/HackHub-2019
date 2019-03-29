import socket
import select

BUFFER = 1024
data_list = {'1':0,'2':0} #dict to check cound against id
msg = {'1':'Go to loc 1', '2':'Go to loc 2'}

socket_list = []
host = ''
port = 12344

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((host,port))
server.listen(5)

socket_list.append(server)

while socket_list:
    data = None
    readable,_,_ = select.select(socket_list,[],[],0)
    for socket in readable:
        if socket is server:
            connection,client_address = socket.accept()
            socket_list.append(connection)
            print(client_address, 'is connected!')
            connection.send('You are connected to the server!'.encode('ascii'))
        else:
            try:
                data = socket.recv(BUFFER)
                if data:
                    d = data.decode('ascii');
                    if(d[0]=='1' or d[0]=='2'):
                        data_list[d[0]]= int(d[1:])
                        print(data_list)
                    if(d[0]=='3'): 
                        keymax = max(data_list, key=data_list.get) 
                        socket.send(str(msg[keymax]).encode('ascii'))
                    #print(socket.getpeername()[1], ':', data.decode('ascii'), end = '')
                    #socket.send(data)
                else:
                    print(socket.getpeername(),'is disconnected!')
                    socket_list.remove(socket)
                    socket.close()
            except ConnectionResetError as e:
                print(socket.getpeername(), 'has closed the connection!')
                socket_list.remove(socket)
                socket.close()
