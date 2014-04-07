import SocketServer
import SimpleHTTPServer
import sys
import urllib
import postings 

query_split = "?q="

class Reply(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,

		path = self.path.encode('utf-8').replace("+", "%20")
		decoded_path = urllib.unquote(path.encode('utf-8'))	
		query = decoded_path[decoded_path.index(query_split) + len(query_split):]		

		query = query.split(',')

		mainlist = postings.getlist(query[0])
		for i in xrange(1, len(query)):
			mainlist = postings.intersectlists(mainlist, postings.getlist(query[i]))
		tracks = postings.tracknames(mainlist)
		outstring = ""
		for i in xrange(0, len(tracks)):
			outstring = outstring+str(i)+'. '+tracks[i]+'\n'
		self.wfile.write("%s" % outstring)


def main():	
	port = int(sys.argv[1])
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()

main()
