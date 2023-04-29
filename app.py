import socket
from select import select

CC_PORT = 8881
SERVICE_PORT = 8880
LISTEN_IP='127.0.0.1'

sock_cc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_cc.bind((LISTEN_IP,CC_PORT))

sock_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_serv.bind((LISTEN_IP,SERVICE_PORT))

sockets = (sock_cc, sock_serv)
for s in sockets:
    s.setblocking(0)

client_serv=None
client_cc=None

# loop forever forwarding packets between the connections
while True:
    avail, _, _ = select((sock_cc, sock_serv), (), (), 1)

    # send a keep alive message every timeout
    if not avail:
        continue

    for s in avail:
        # something from the local server, forward it on
        if s is sock_cc:
            msg = sock_cc.recvfrom(8192)
            client_cc=msg[1]
            if client_serv is not None:
                if msg[0] != b'keep alive':
                    sock_serv.sendto(msg[0], client_serv)

        # something from the remote server
        if s is sock_serv:
            msg = sock_serv.recvfrom(8192)
            client_serv=msg[1]
            if client_cc is not None:
                sock_cc.sendto(msg[0], client_cc)
