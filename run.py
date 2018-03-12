import sys
from mbio.server.server import Server
from http.server import HTTPServer

dataset_path = sys.argv[1]

port = 8081
def run():
    print('Starting server on port {}...'.format(port))

    Server.DATASET_PATH = dataset_path

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    print('Server is running!')

    httpd.serve_forever()

if __name__=='__main__':
    run()
