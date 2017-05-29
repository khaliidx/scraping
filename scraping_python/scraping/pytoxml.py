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

soup = BeautifulSoup(page)

#all the titles
p= soup.findAll('p', class_="title")





############## saving data in an XML file


import xml.etree.cElementTree as ET
tree = ET.parse("posts.xml");
root = tree.getroot();

#posts = ET.Element("posts")
# to do :: create element 'posts' if file is empty
#       :: delete old posts 


i=0
while i<26 : # for some reason this cant get beyond 26...
	link= p[i].find('a').get('href')
	thread_title= p[i].find('a').string
	flag=0;

	if "youtu.be" in link or ".mp4" in link or "streamable.com" in link: # filtering goals here	
		# checking if the post already exists in the .xml file		
		for pst in root.findall("post"):
			if pst.find("title").text==thread_title:
				flag=1
				break
		
		#if not we add the post
		if flag==0:
			post = ET.Element("post")
			ET.SubElement(post,"title").text = thread_title			
			ET.SubElement(post, "link").text = link
			#if link[i]=='/': # if the link is a post on self.soccer add reddit link
				#print ("https://www.reddit.com"+p0)
			#	ET.SubElement(post, "link").text = "https://www.reddit.com"+link
			#else:
			

			root.insert(0,post)		

	i=i+1

tree.write("posts.xml")
#if permissions get fucked chown khalid:www-data /var/www/html/posts.xml






	#posts = ET.Element("posts")
	#post=ET.SubElement(posts, "post");
	#ET.SubElement(post, "title").text = "this is value1"
	#ET.SubElement(post, "link").text = "this is value2"





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



