import socket
import struct
from threading import Thread

class Multicast(Thread):

    MCAST_GRP = "224.1.1.1"
    MCAST_PRT = 5007

    def __init__(self, srv_q):
        Thread.__init__(self)
        self.srv_q = srv_q

    def run(self):
        self.receive()

    def receive(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.MCAST_PRT))
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            new_srv = sock.recv(10240)
            print("{0} join the group !".format(new_srv))
            self.srv_q.put(new_srv)

    def send(self, srv):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(str.encode(srv), (self.MCAST_GRP, self.MCAST_PRT))
