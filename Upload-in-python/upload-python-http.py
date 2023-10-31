import http.server
import socketserver
import cgi

class PostHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        self.send_response(200)
        self.end_headers()
        if 'file' in form:
            file_data = form['file'].file.read()
            with open(form['file'].filename, 'wb') as f:
                f.write(file_data)
                self.wfile.write(f"File {form['file'].filename} uploaded successfully".encode())
        else:
            self.wfile.write("No file in form".encode())

handler = PostHandler

with socketserver.TCPServer(("", 8000), handler) as httpd:
    print("serving at port", 8000)
    httpd.serve_forever()