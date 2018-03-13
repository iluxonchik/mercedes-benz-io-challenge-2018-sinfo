#!/usr/bin/env python3

import argparse
from mbio.server.server import Server
from http.server import HTTPServer

def run(dataset_path, server_port):

    print('Starting server on port {}...'.format(server_port))
    Server.DATASET_PATH = dataset_path

    # Server settings
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, Server)
    print('Server is running!')

    try:
        httpd.serve_forever()
    except Exception as e:
        print('[!!!] Fatal error occured. The application will end.')
        print('\t{}'.format(str(e)))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Mercedes-Benz IO TestDrive application. Developed as part of the MB IO challenge at SINFO 25.')
    parser.add_argument('-f', '--file', help='Path to the file containing the JSON dataset.', required=True)
    parser.add_argument('-p', '--port', help='Port on which to start the HTTP Server.', default=8081, type=int)
    args = parser.parse_args()
    run(args.file, args.port)
