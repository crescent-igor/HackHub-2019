import socket
import select
import math
import time
from ast import literal_eval
BUFFER = 1024
data_list_count = {'1':[],'2':[]} #dict to check count against id
data_list_cordinates = {'1':[],'2':[]} 
avg_dict = {'1':[],'2':[]} 
avg1, avg2 = 0,0
msg = {'1':"Go to floor 1",'2':"Go to floor 2"}
#1:clean, 0: occupied and dirty, -1: dirty and to be cleaned
loc1 = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1} #initially all clean
loc2 = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1} 
req_list1 = [0,0,0,0,0,0,0,0,0]
frameCount = 0
old=[0,0,0,0,0,0,0,0,0]
def cleanOrOcc(req_list1,loc1):
    for i in range(len(req_list1)):
        if(req_list1[i]>400) :
            loc1[i+1]=0

def occOrDirty(old, new, df):
    for i in range(9):
        df[i] = new[i]-old[i]   
        if(df[i]==0 and loc1[i+1]==0):
            loc1[i+1] = -1 
            new[i]=0
    print(df)

def Average(lst): 
    return sum(lst) / len(lst) 

socket_list = []
host = ''
port = 12345

#=========================
#SECTION FOR IMAGE MAPPING
#=========================

test_point = [243,589,356,805]
centers = [(133.33,100),(400,100),(666.67,100),(133.33,300),(400,300),(666.67,300),(133.33,500),(400,500),(666.67,500)]

def calc_center(point_list):
    x_cent = (point_list[2]+point_list[3])/2
    y_cent = (point_list[0]+point_list[1])/2
    center = [x_cent,y_cent]
    return center

def calc_dist(p1,p2):
    dist = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    dist = round(dist,2)
    return dist

def point_dist_to_centers(point,centers):
    dist_vector = []
    for center in centers:
        dist_vector.append(calc_dist(center,point))
    return dist_vector

def find_area(test_point):
        point_center = calc_center(test_point)
        from_centers = point_dist_to_centers(point_center,centers)
        closest = from_centers.index(min(from_centers))
        return closest+1

#==============================

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
                        #print(recvData)
                        if(len(data_list_count[d[0]])>20):
                            data_list_count[d[0]].pop(0)
                        data_list_count[d[0]].append(int(recvData[1]))
                        if(len(data_list_cordinates[d[0]])>5):
                            data_list_cordinates[d[0]].pop(0)
                        if(recvData[1]!='0'):
                            data_list_cordinates[d[0]].append(recvData[2:])
                        #print(data_list_cordinates)
                        
                        for i in data_list_cordinates[d[0]]:
                            # print(i)
                            for j in i:
                                j=j[1:]
                                j=j[:-1]
                                j=j.split(',')
                                if(len(j)==5):
                                    if(j[4].strip()=="'person'"):
                                        y1 = int(j[0])
                                        y2 = int(j[1])
                                        x1 = int(j[2])
                                        x2 = int(j[3])
                                        coordList = [y1,y2,x1,x2]
                                        area = find_area(coordList)
                                        print(area)
                                        if(d[0]=='2'):
                        
                                            req_list1[area-1] = req_list1[area-1]+1
                                            frameCount = frameCount+1
                                            cleanOrOcc(req_list1,loc1)
                                            if(frameCount>40):
                                                df = [0,0,0,0,0,0,0,0,0]
                                                occOrDirty(old,req_list1,df)
                                                frameCount=0
                                                old=req_list1
                                        print('Request list:')
                                        print(req_list1)
                                        print('Clean, occupied or dirty')
                                        print(loc1)
                                        #print(area)
                                    
                                # if(j[4]=="'person'"):
                                    # print('yay')
                        
                            
                                    
                        # print(data_list_cordinates)
                        # print(data_list_cordinates)
                        if d[0]=='1':
                            avg1 = Average(data_list_count[d[0]])
                        if d[0]=='2':
                            avg2 = Average(data_list_count[d[0]])
                        print('AVG:')
                        print(round(max(avg1,avg2)))
                        print()
                                        
                    if(d[0]=='3'): 
                        if(max(avg1,avg2)==avg1):
                            socket.send(str(msg['1']).encode('ascii'))
                        else:
                            socket.send(str(msg['2']).encode('ascii'))
                        for i in range(9):
                            if(loc1[i+1]==-1):
                                msg1 = 'Clean segment '+ str(i+1)
                                socket.send(msg1.encode('ascii'))
                                break
                        # keymax = max(data_list_count, key=data_list_count.get)
                        # area = find_area(test_point)
                        # recvData = d.split(':')
                        # cid = recvData[1]
                        # instruction = 'bot '+str(cid)+' go to location '+str(area)
                        # socket.send(instruction.encode('ascii'))
                        # time.sleep(5) 
                        #socket.send(str(msg[keymax]).encode('ascii'))
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