from mbio.server.server import Server
from http.server import BaseHTTPRequestHandler, HTTPServer

port = 8081
def run():
    print('Starting server on port {}...'.format(port))

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    print('Server is running!')

    httpd.serve_forever()

if __name__=='__main__':
    run()
