#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl
import json

PORT_NUMBER = 8080
CONFIG_FILE = 'clean_response_config.json'

class CleanResponseServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.create_json_response('get')

    def do_PUT(self):
        self.create_json_response('put')

    def do_POST(self):
        self.create_json_response('post')

    def do_DELETE(self):
        self.create_json_response('delete')

    def set_response_headers(self, responseCode = 200):
        self.send_response(responseCode)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

    def default_response(self):
        return '{"error" : "url not found"}'

    def default_response_code(self):
        return 200

    def create_json_response(self, method):
        try:
            json_file = json.load(open(CONFIG_FILE))
            json_post_object = json_file[method]

            return_payload = self.default_response()
            return_code = self.default_response_code()

            search_path = self.path[1:]

            if search_path in json_post_object:
                json_object = json_post_object[search_path]
                if "fileResponse" in json_object:
                    txt = open(json_object["fileResponse"])
                    return_payload = txt.read()
                elif "response" in json_object:
                    return_payload = json_object["response"]
                if "code" in json_object:
                    return_code = json_file["code"]

            print " [OK] %s Return payload \n\n%s\n\n\n" % (method, return_payload)
            self.set_response_headers(responseCode = return_code)
            self.wfile.write(return_payload)
        except IOError:
            self.send_error(404, ' [FAIL] Path (%s.%s) not found in JSON' % (method, self.path))

if __name__ == "__main__":
    try:
        server = HTTPServer(('', PORT_NUMBER), CleanResponseServer)

        # comment if only run with HTTP
        server.socket = ssl.wrap_socket(server.socket,
                                        certfile='./fake-server.pem',
                                        server_side=True)
        print ' [OK] Clean Response Server started...\nPORT: %d\nConfig file: %s\n\n', (PORT_NUMBER, CONFIG_FILE)
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
    server.socket.close()
