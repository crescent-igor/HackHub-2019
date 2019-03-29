import socket
import select

BUFFER = 1024
data_list_count = {'1':[],'2':[]} #dict to check count against id
data_list_cordinates = {'1':[],'2':[]} 
avg_dict = {'1':[],'2':[]} 
avg1, avg2 = 0,0
msg = {'1':"loc 1",'2':"loc 2"}

def Average(lst): 
    return sum(lst) / len(lst) 

socket_list = []
host = ''
port = 12345


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
                    d = data.decode('ascii')
                    if(d[0]=='1' or d[0]=='2'):
                        # data_list[d[0]]= d[1:]
                        recvData=d.split(':')
                        if(len(data_list_count[d[0]])>20):
                            data_list_count[d[0]].pop(0)
                        data_list_count[d[0]].append(int(recvData[1]))
                        # data_list_cordinates[d[0]].append(recvData[2])
                        print(recvData)
                        if d[0]=='1':
                            avg1 = Average(data_list_count[d[0]])
                        if d[0]=='2':
                            avg2 = Average(data_list_count[d[0]])
                        print(max(avg1,avg2))
                                        
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