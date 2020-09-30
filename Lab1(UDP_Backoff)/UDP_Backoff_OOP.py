import argparse, random, socket, sys
from datetime import datetime, time


class Server:
    MAX_BYTES = 65535

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.interface, self.port))
        print('Listening at', sock.getsockname())

        while True:
            data, address = sock.recvfrom(self.MAX_BYTES)

            if random.random() < 0.5:
                print(f'Pretending to drop packet from {address}')
                continue

            text = data.decode('ascii')
            print(f'The client at {address} says "{text}"')

            message = f'Your data was {len(data)} bytes long'
            sock.sendto(message.encode('ascii'), address)


class Client:
    MAX_BYTES = 65535

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def get_coeff_and_delay(self):
        curr = datetime.now().time()
        if time(12) <= curr <= time(17):
            return (2, 2)
        elif time(17) <= curr <= time(23, 59):
            return (3, 4)
        else:
            return (2, 1)


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.hostname, self.port))
        print(f'Client socket name is {sock.getsockname()}')

        text = f'This is another message. Sent at {datetime.now()}'
        data = text.encode('ascii')
        
        delay = 0.1
        while True:
            sock.send(data)
            print(f'Waiting up to {round(delay, 2)} seconds for a reply')
            sock.settimeout(delay)

            try:
                data = sock.recv(self.MAX_BYTES)
            except socket.timeout:
                coeff, max_delay = self.get_coeff_and_delay()
                delay *= coeff
                if delay > max_delay:
                    raise RuntimeError('I think the server is down')
            else:
                break

        print(f"The server says {data.decode('ascii')}")


def main():
    choices = {'client': Client, 'server': Server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     'pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    clss = choices[args.role]
    clss(args.host, args.p).run()


if __name__ == '__main__':
    main()