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
		path = self.path.replace("%20", ' ').lower();
		path = path.split('?p=')[1];
		suggestions = query_suggest.get_suggestions(path)
		#print path
		#print suggestions
		self.wfile.write(json.dumps(suggestions))

	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,
		self.wfile.write('''<html>
<head>
<link href="http://netdna.bootstrapcdn.com/bootswatch/3.1.1/spacelab/bootstrap.min.css" rel="stylesheet">
</head>

<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<meta charset=utf-8 />
<title></title>
  
<script>
  var suggestions;
  var displayNum = 14;
  var querySelector = 0;
  var displaySelector = 0;
  function getQueries(instring){
           var tagparts = instring.split(',');
           var tag = tagparts[tagparts.length-1];
           if (tag[0] == ' ') tag = tag.substring(1,tag.length);
           if (tag[0] == '' && tagparts.length > 1) tag = tagparts[tagparts.length-2]; 
           $.ajax({type:'POST', url:'?p='+tag, success:function(result){
                suggestions = eval('(' + result + ')');
                displayNum = 14;
                if (displayNum > suggestions.length)
                   displayNum = suggestions.length;
        
                displaySelector = 0;
                var sugstring = '';
                var ensp = "&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;";

                for (var i = 0; i < Math.floor(displayNum/2); i++){
                   sugstring += '<tr><td>'+suggestions[i]+ensp+'</td><td>';
                   var ind = Math.ceil(displayNum/2)+i;
                   if (ind < suggestions.length)
                     sugstring += suggestions[ind]+'</td>';
                   sugstring+='</tr>'
                }
                if (displayNum % 2 != 0 && suggestions[0] != '--'){
                   sugstring += '<tr><td>'+suggestions[suggestions.length-1]+ensp+'</td><td>';
                   sugstring += '<td>'+ensp+'</td><\tr>';
                } 
                $("#sugtable").html(sugstring); 
  }} ); }


  function updateQueries(){
                displaySelector+=displayNum;
                if (displaySelector >= suggestions.length)
                   displaySelector = 0;
                querySelector  = displaySelector;
                var sugstring = '';
                var ensp = "&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;";
                for (var i = displaySelector; i < displaySelector+Math.floor(displayNum/2); i++){
                   if (i >= suggestions.length) break;

                   sugstring += '<tr><td>'+suggestions[i]+ensp+'</td><td>';
                   var ind = Math.ceil(displayNum/2)+i;
                   if (ind < suggestions.length)
                     sugstring += suggestions[ind]+'</td>';
                   sugstring+='</tr>'
                  
                }
                $("#sugtable").html(sugstring);   
  }       


  $(document).ready(function(){
     $("#query").keypress(function(e){ 
            if (e.keyCode !=9 && e.keyCode != 8)
            { 
              displaySelector = 0; querySelector = 0;
              query = $("#query").val()+String.fromCharCode(e.keyCode);
              getQueries(query); 
            }
      });

     $("#query").keydown(function(e){
        if (e.keyCode==8){
           query = $("#query").val();
           query = query.substring(0, query.length-1);
           getQueries(query);
        }

        else if (e.keyCode==9){
           e.preventDefault();
           end = suggestions.length-1
           if (querySelector > end) {
             querySelector = 0;
             displaySelector = 0;
             updateQueries;
           }

           if (querySelector >= displaySelector+displayNum)
             updateQueries();
   
           if (suggestions[querySelector] != '--'){
             query = $('#query').val()
             if (query[query.length-1]==',')
               query = query.substring(0,query.length-1);

             query = query.split(',');
             query[query.length-1] = suggestions[querySelector];
             $("#query").val(query.join(',')+',');
           }
           querySelector++;
        }
       else if (e.keyCode==16){
           updateQueries();
        }
     });

	$('.spotify').click(function(){

		var record_track = $(this).parent().parent().children().eq(1).text();
		var record_artist = $(this).parent().parent().children().eq(2).text();
		var get_url = 'http://ws.spotify.com/search/1/track.json?q=' + encodeURIComponent(record_track);
                console.log(get_url);
		$.get(get_url, function( data ) {
			target_artist = record_artist.toLowerCase().substring(0,8);
			var match = false;
                        console.log(data['tracks']);
			console.log(data['tracks'][0]['href']);
			for (var i = 0; i < data['tracks'].length; i++){
				if (!match) {
					var artist = data['tracks'][i]['artists'][0]['name'].toLowerCase().substring(0,8);
					if (artist == target_artist) {
						redirect = data['tracks'][i]['href'];
						redirect_data = redirect.split(':')
						redirct_url = 'https://play.spotify.com/track/' + redirect_data[2];
						window.open(redirct_url);
						match = true;
					}
				}
			}
			if (!match)
  				$('#error').html("Sorry! We looked high and low but we could not find the track on spotify").show();
		});
	});

  });

</script>
</head>

<body>

	<div class="container col-md-12">

		<form name="input" action="" method="get">
			<table class="table ">
				<tr>
				
					<td>
                                        <p id="error" class="bg-danger" hidden></p>
					<h1 id="asdf">Million Song Database - Search By Tags</h1>
                                        <div id='instructions'> <b>Input your search terms below. Search suggestions will pop up beneath this banner; press tab to iterate through the list and press shift to suggest more tags.</b> <br><br> </div>

                                        <table id = 'sugtable'> </table>

					<input type="text" autocomplete="off" size="100" class="input input-lg" id="query" name="q"> <br><br>
				
				
					<input type="submit" class="btn btn-primary" value="Submit">
				</tr>
			</table>
		</form> 

''')
		
		path = self.path.encode('utf-8').replace("+", "%20").lower()
		decoded_path = urllib.unquote(path.encode('utf-8'))
		try:
			query = decoded_path[decoded_path.index(query_split) + len(query_split):]		
		except:
			return
		query = query.split(',')

		mainlist = postings.getlist(query[0].strip())
		for i in xrange(1, len(query)):
                        if (query[i] == ''):
				continue;
			mainlist = postings.intersectlists(mainlist, postings.getlist(query[i].strip()))
		tracks = postings.tracknames(mainlist)
		outstring = ""
		self.wfile.write('<table class="table table-bordered"> <tr><th>Rank</th><th>Track Title</th><th>Artist</th><th>Score</th><th>TrackID</th><th>Listen</th></tr> ')
		
		for i in xrange(0, len(tracks)):
			split = tracks[i].split('|')
			outstring = '<tr><td>'+str(i+1)+'</td><td>'+split[0]+'</td><td>'+split[1]+'</td><td>'+split[2]+'</td><td>'+split[3]+'<td><button class="btn btn-success spotify">Spotify</button></td>'+'</tr>'
			self.wfile.write(outstring)
	
		self.wfile.write('</table></div></body>')


def main():	
	port = int(sys.argv[1])
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()

main()
