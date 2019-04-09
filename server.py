import socket
import http.server
import socketserver
from os import curdir, sep
import time


class DiffController(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/"):
            self.getPage()

        elif (self.path):
            self.getStatic(self.path)

        else:
            self.notFound()

    def do_POST(self):
        if (self.path == "/"):
            self.postGoal()

        else:
            self.notFound()

    def getStatic(self, path):
        try:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
            if self.path.endswith(".html"):
                self.send_header("Content-Type", "text/html")

            elif self.path.endswith(".css"):
                self.send_header("Content-Type", "text/css")

            elif self.path.endswith(".js"):
                self.send_header("Content-Type", "text/javascript")

            f = open(curdir + sep + "web" + sep + path, "rb")
            response = f.read()
            self.send_header("Content-Length", f.tell())
            self.end_headers()
            self.wfile.write(response)
            self.wfile.flush()
            f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % path)

    def getPage(self):
        self.getStatic("/controller.html")

    def notFound(self):
        self.send_error(http.HTTPStatus.NOT_FOUND)

    def postGoal(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.send_header("Content-Type", "text/html")
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)
        Server.callback(body)
        response = b"No Response"
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)


class Server:
    def __init__(self, port, callback):
        Server.callback = callback
        print("server")

        with http.server.HTTPServer(("", port), DiffController) as httpd:
            print("serving at port", port)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.server_close()