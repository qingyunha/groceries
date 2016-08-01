import sys
import os
import time
import signal
import socket


benchtime = 5

client = 2

speed = 0
bytess = 0
failed = 0

stop = False

def bench(url):
    global speed, bytess, failed, stop
    host = url[url.find('/')+2:]
    req = "GET / HTTP1.1\r\nHost: {}\r\nUser-Agent: python\r\n\r\n".format(host)
    while not stop:
        try:
            s = socket.create_connection((host, 80))
            s.send(req)
            n = s.recv(1024)
            while n:
                bytess += len(n)
                n = s.recv(1024)
            s.close()
            speed += 1
        except Exception as e:
            print e
            failed += 1
        


def sig_handler(signum, frame):
    global stop
    stop = True


def main():
    r, w = os.pipe()
    url = sys.argv[1]

    for i in range(client):
        pid = os.fork()
        if pid == 0:
            signal.signal(signal.SIGALRM, sig_handler)
            signal.alarm(benchtime)
            bench(url)
            stats = "Speed=%d pages/min, %d bytes/sec.\nRequests: %d susceed, %d failed.\n" % ( (speed+failed)/(benchtime/60.0), bytess/float(benchtime),
                        speed, failed)
            os.write(w, stats)
            return
    print "waitting for child"
    for i in range(client):
        print os.read(r, 100)
    print "main done"

if __name__ == "__main__":
    main()
