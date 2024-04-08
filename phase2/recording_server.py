import http.server
import socketserver
import os

ip = '127.0.0.1'
PORT = 8888
DIRECTORY = "shared_recordings"

class Handler(http.server.SimpleHTTPRequestHandler):
  def __int__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)
  
# make sure that shared directory exist
if not os.path.exists(DIRECTORY):
  os.makedirs(DIRECTORY)

# set HTTP server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print(f"Server started at localhost:{PORT}")
  httpd.serve_forever()
