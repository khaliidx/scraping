#!/usr/bin/env python
import cgi,cgitb
cgitb.enable() # for errors

print ("Content-type: text/html;charset=utf-8")
print ()


############## extracting data from redddit :

from bs4 import BeautifulSoup
try: # for python3
	import urllib.request as urlreq
except ImportError: # else back to python2's urllib2
	import urllib2 as urlreq
 

site = "https://www.reddit.com/r/soccer"

hdr = { 'User-Agent' : 'just testing thx' }
req = urlreq.Request(site, headers=hdr)
page = urlreq.urlopen(req)

soup = BeautifulSoup(page,"lxml")

#all the titles
p= soup.findAll('p', class_="title")





############## saving top 5 in /r/soccer data in the database


import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()


i=0
while i<26 : # for some reason cant get beyond 26 posts...
	link= p[i].find('a').get('href')
	thread_title= p[i].find('a').string
	flag=0;

	if "youtu.be" in link or ".mp4" in link or "streamable.com" in link: # filtering goals here	
		# checking if the post already exists in the database		

		cursor.execute("SELECT title FROM POSTS WHERE title=?",(thread_title,))		
		exist = cursor.fetchone()
		if exist is None:
			cursor.execute(" INSERT INTO POSTS values(?,?)",(thread_title,link))
			conn.commit()			
	i=i+1


#################################################################
#### iNSERTING IN XML FILE

import xml.etree.cElementTree as ET
tree = ET.parse("posts.xml");
root = tree.getroot();


results = conn.execute("SELECT * FROM POSTS")
for row in results:
	flag=0;
	t = row[0]
	l = row[1]
	
	# checking if the post already exists in the .xml file		
	for pst in root.findall("post"):
		if pst.find("title").text==t:
			flag=1
			break	
	
	if flag==0:
		post = ET.Element("post")
		ET.SubElement(post,"title").text = t			
		ET.SubElement(post, "link").text = l
		root.insert(0,post)



tree.write("posts.xml")




conn.close() 








print("""
<html> 
	 <head> 
	   <meta http-equiv="refresh" content="0;url=website/reddit.html" /> 
	   <title>You are going to be redirected</title> 
	 </head> 
	  <body> 
	   Redirecting...
	 </body> 
</html>
""")














#######################################################################
### tried to modify html from here but i dont think its worth it.gonna try js now


#current = open("/var/www/test/website/reddit.html","r").read()

#soup = BeautifulSoup(current,"lxml")
#posts= soup.find("div", {"id":"posts"})
#print (posts)
#posts=str(posts)

#soup_b = BeautifulSoup(posts,"lxml")

#new_tag = soup_b.new_tag(name="a",href=link)
#new_tag.string= thread_title
#print(new_tag)
#soup_b.append(new_tag)
#posts2= BeautifulSoup(posts,"lxml")
#posts2.append(soup_b)
#print(posts2)






#cursor.execute("select * from POSTS")

#for row in cursor:
#	print ("title : "+ row[0]+" link : "+ row[1]+"\n")











