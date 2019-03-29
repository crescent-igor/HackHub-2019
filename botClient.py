import socket
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  client.connect(('localhost', 12344))
except ConnectionRefusedError as e:
  print("Server is down!\n")
  sys.exit()


sys.stdout.write("Command: ")
sys.stdout.flush()
socket_list = [sys.stdin, client]


# def parseInput(msg):
#   if str(msg).strip()=='exit':
#     print('Closing client!')
#     client.close()
#     sys.exit()


while True:
  ready, _, _ = select.select(socket_list, [], [], 0)
  for socket in ready:
    if socket is client:
      # print("Server is talking")
      # Incomming msg from server
      data = client.recv(1024)
      print(data.decode('ascii'))
      if not data:
        print("\nServer is disconnected!")
        sys.exit()
      else:
        print('\n[Server]: ', data.decode('ascii'))
        sys.stdout.write("Command: ")
        sys.stdout.flush()
    elif socket is sys.stdin:
      # stdin recieved an input
      msg = '3'
      #parseInput(msg)
      client.send(str(msg).encode('ascii'))
      sys.stdout.write("Command: ")
      sys.stdout.flush()
    else:
      pass


