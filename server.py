import SocketServer
import SimpleHTTPServer
import sys
import urllib
import postings 
import query_suggest
import json

query_split = "?q="

class Reply(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		path = self.path.replace("%20", ' ');
		path = path.split('?p=')[1];
		suggestions = query_suggest.get_suggestions(path)
		print path;
		print suggestions
		self.wfile.write(json.dumps(suggestions))

	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,
		self.wfile.write('''<html>
<head>
<link href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
</head>

<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<meta charset=utf-8 />
<title></title>
  
<script>
  var suggestions;
  var selector = 0;
  function getQueries(instring){
           var tagparts = instring.split(',');
           var tag = tagparts[tagparts.length-1];
           tag = tag.replace(' ','');
           $.ajax({type:'POST', url:'?p='+tag, success:function(result){
                suggestions = eval('(' + result + ')');
                selector = 0;
                var sugstring = '';
                for (var i = 0; i < suggestions.length; i++)
                   sugstring += suggestions[i]+'<br>';
                $("#suggestions").html(sugstring); 
  }} ); }
  $(document).ready(function(){
     $("#query").keypress(function(e){ 
            query = $("#query").val()+String.fromCharCode(e.keyCode);
            getQueries(query); 
     });
 
     $("#query").keydown(function(e){
        if (e.keyCode==8){
           query = $("#query").val();
           query = query.substring(0, query.length-1);
           getQueries(query);
        }
        else if (e.keyCode==16){
           end = suggestions.length-1
           if (selector > end)
             selector = 0;
           if (suggestions[selector] != '--')
             $("#query").val(suggestions[selector]);
           selector++;
        }
     });
  });

</script>
</head>

<body>

	<div class="container col-md-12">

		<form name="input" action="http://localhost:8083" method="get">
			<table class="table ">
				<tr>
				
					<td>

					<h1 id="asdf">Million Song Database - Search By Tags</h1>
                                        <div id='suggestions'> suggestions go here!</div>


					<input type="text" autocomplete="off" size="100" class="input input-lg" id="query" name="q"> <br><br>
				
				
					<input type="submit" class="btn btn-primary" value="Submit">
				</tr>
			</table>
		</form> 

''')
		
		path = self.path.encode('utf-8').replace("+", "%20")
		decoded_path = urllib.unquote(path.encode('utf-8'))	
		query = decoded_path[decoded_path.index(query_split) + len(query_split):]		

		query = query.split(',')

		mainlist = postings.getlist(query[0])
		for i in xrange(1, len(query)):
			mainlist = postings.intersectlists(mainlist, postings.getlist(query[i]))
		tracks = postings.tracknames(mainlist)
		outstring = ""
		self.wfile.write('<table class="table table-bordered"> <tr><th>Rank</th><th>Track Title</th><th>Artist</th><th>Score</th><th>TrackID</th></tr> ')
		
		for i in xrange(0, len(tracks)):
			split = tracks[i].split('|')
			outstring = '<tr><td>'+str(i)+'</td><td>'+split[0]+'</td><td>'+split[1]+'</td><td>'+split[2]+'</td><td>'+split[3]+'</tr>'
			self.wfile.write(outstring)
	
		self.wfile.write('</table></div></body>')


def main():	
	port = int(sys.argv[1])
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()

main()
