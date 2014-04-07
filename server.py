import SocketServer
import SimpleHTTPServer
import sys
import urllib
import postings 

query_split = "?q="

class Reply(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,
		terms = self.path.split('/')
		decoded_path = urllib.unquote(self.path.encode('utf8'))	
		query = decoded_path[decoded_path.index(query_split) + len(query_split):]		
		query = query.split(',')

		mainlist = postings.getlist(query[0])
		for i in xrange(1, len(query)):
			mainlist = postings.intersectlists(mainlist, postings.getlist(query[i]))
		self.wfile.write("%s" % str(postings.sortedtracks(mainlist)).encode('utf-8'))

def main():	
	port = 8080
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()

main()
