import argparse, socket, sys, os
import pickle, json

class Server:
    MAX_BYTES = 65535

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port


    @staticmethod
    def change_text(text_data, json_data):
        some_dict = json.loads(json_data)
        for key, value in some_dict.items():
            text_data = text_data.replace(key, value)
        return text_data

    @staticmethod
    def encode_decode(text_data, key):
        return "".join([chr(ord(a) ^ ord(b)) for a, b in zip(text_data, key)])


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print('Listening at', sock.getsockname())
        while True:
            sc, sockname = sock.accept()

            print("We have accepted a connection from", sockname)
            print(" Socket name", sc.getsockname())
            print(" Socket peer", sc.getpeername())

            data = sc.recv(self.MAX_BYTES)
            recvd_obj = pickle.loads(data)
            mode, file1_data, file2_data = recvd_obj.mode, recvd_obj.file1_data, recvd_obj.file2_data
            
            mode = mode.decode("utf-8")
            if mode == "change_text":
                changed_text = self.change_text(file1_data.decode("utf-8"), file2_data.decode("utf-8"))
                sc.sendall(changed_text.encode("utf-8"))

            elif mode == "encode_decode":
                encoded_decoded_text = self.encode_decode(file1_data.decode("utf-8"), file2_data.decode("utf-8"))
                sc.sendall(encoded_decoded_text.encode("utf-8"))

            sc.close()
            print(" Reply sent, socket closed")
    

class Client:
    MAX_BYTES = 65535

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
       
    
    def run(self, mode, file1_name, file2_name):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.hostname, self.port))
        print("Client has been assigned socket name", sock.getsockname())
 
        file1 = open(file1_name, "rb")  # no need to encode as we read in bytes
        file1_data = file1.read()

        file2 = open(file2_name, "rb")
        file2_data = file2.read()

        temp = pickle.dumps(EmbeddedData(mode.encode("utf-8"), file1_data, file2_data))
        sock.sendall(temp)

        file1.close()
        file2.close()

        processed_data = sock.recv(self.MAX_BYTES)
        print("Reply from Server : ", processed_data.decode("utf-8"))

        sock.close()


class EmbeddedData:
    def __init__(self,mode, file1_data, file2_data):
        self.mode = mode
        self.file1_data = file1_data
        self.file2_data = file2_data


def main():
    choices = {'client':Client, 'server':Server}
    parser = argparse.ArgumentParser('Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')

    if sys.argv[1] == "client":
        parser.add_argument('--mode', type = str, help = "change_text/encode_decode option")
        parser.add_argument('file1', type = str, help = "file1 name")
        parser.add_argument('file2', type = str, help = "file2 name")

    args = parser.parse_args()
    clss = choices[args.role]
    
    if args.role == "client":
        clss(args.host, args.p).run(args.mode, args.file1, args.file2)
    else:
        clss(args.host, args.p).run()


if __name__ == "__main__":
    main()
    