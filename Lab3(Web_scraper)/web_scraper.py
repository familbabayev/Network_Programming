import argparse, socket
import sys, requests
from bs4 import BeautifulSoup


class Server:
    MAX_BYTES = 65535

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    def get_image_count(self, link_html):
        return len(link_html.find_all('img'))

    def get_leaf_p_count(self, link_html):
        n = 0
        for p in link_html.find_all('p'):
            if not p.find_all('p'):
                n += 1
        return n

    def scrape_link(self, url):
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.text, "html.parser")
        img_count = self.get_image_count(soup)
        p_count = self.get_leaf_p_count(soup)
        return (img_count, p_count)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print("Listening at", sock.getsockname())
        while True:
            sc, sockname = sock.accept()
            print("We have accepted a connection from", sockname)
            print(" Socket name", sc.getsockname())
            print(" Socket peer", sc.getpeername())

            data = sc.recv(self.MAX_BYTES)
            url = data.decode("utf-8")

            scraped_link = self.scrape_link(url)
            img_count, p_count = scraped_link[0], scraped_link[1]

            response = f"{img_count} {p_count}"
            sc.sendall(response.encode("utf-8"))

            sc.close()
            print(" Reply sent, socket closed")



class Client:
    MAX_BYTES = 65535

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def run(self, url):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.hostname, self.port))

        sock.sendall(url.encode("utf-8"))

        server_reply = (sock.recv(self.MAX_BYTES)).decode("utf-8")
        img_count, p_count = server_reply.split()

        print("Reply from Server:")
        print("Number of images : ", img_count)
        print("Number of leaf paragraphs : ", p_count)


def main():
    choices = {'client':Client, 'server':Server}
    parser = argparse.ArgumentParser('Scrape web pages')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                       ' host the client sends to')
    parser.add_argument('-port', metavar='PORT', type=int, default=1060,
                       help='TCP port (default 1060)')

    if sys.argv[1] == "client":
        parser.add_argument('-p', metavar='PAGE', type = str, help = "link to the webpage")

    args = parser.parse_args()
    clss = choices[args.role]
    
    if args.role == "client":
        if "http://" in args.p or "https://" in args.p:
            clss(args.host, args.port).run(args.p)
        else:
            clss(args.host, args.port).run(f"http://{args.p}")
    else:
        clss(args.host, args.port).run()


if __name__ == "__main__":
    main()

