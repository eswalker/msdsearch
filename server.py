import SocketServer
import SimpleHTTPServer
import sys
import urllib

query_split = "?q="

class Reply(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,
		path = self.path.encode('utf-8').replace("+", "%20")
		decoded_path = urllib.unquote(path.encode('utf8'))	
		query = decoded_path[decoded_path.index(query_split) + len(query_split):]			
		self.wfile.write("%s" % query.encode('utf-8'))

def main():	
	port = 8080
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()

main()