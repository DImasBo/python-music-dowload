import requests
from bs4 import BeautifulSoup

import vlc

import os

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

#https://myzcloud.club/search?searchText=
def searchForSong(song):
	print("------------------SEARCH SONG-------------------")
	print(str(song))
	url = "https://myzcloud.club/search?searchText=" + str(song)
	r = requests.get(url)
#	print(url)
#	with open("index.html","w") as f:
#		f.write(r.text)
	s = BeautifulSoup(r.text, "lxml")
	divs = s.find("div",class_="playlist--hover").find_all("div",class_="playlist__item")
	
	music = {}

	with open("index.html","w") as f:
		f.write(str(divs))
	print("-----result-------")
	for div in divs:
		music["name"] = div.get("data-name")
		music["artist"] = div.get("data-artist")
		music["title"] = div.div.get("data-title")
		url = "https://myzcloud.club" + div.div.get("data-url")
		print(music["title"])
		music["url"] = url
		p.set_mrl(url)
		p.play()
		t = ''
		while t != 'n' and t != 'y':
			t = input("Do you download the song?(y/n)")
		if t == "y":
			url = "https://myzcloud.club" + div.find("div",class_="playlist__details").a.get("href")
			r = requests.get(url)
			music["photo"] = BeautifulSoup(r.text, "lxml").find("img",class_="album-img").get("src")
			break
		print("-----------------------------------")
	return music

def dowloadMusic(music):
#	print(music['url'])
	r = requests.get(music["url"],stream = True)
	name = music["title"] + ".mp3"
	with open("dowload/" + name,"wb") as f:
		for chunk in r.iter_content(chunk_size=512 * 1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return name

def setImage(photo,source):
	r = requests.get(photo,stream = True)
	with open("cookie/1.jpg","wb") as f:
		for chunk in r.iter_content(chunk_size=512 * 1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)

	audio = MP3('dowload/' + source, ID3=ID3)


	audio.tags.add(
	    APIC(
	     encoding=3, 
	     mime='image/jpeg', 
	     type=3, 
	     desc=u'Cover', 
	     data=open("cookie/1.jpg", 'rb').read() 
	    ) 
	)
	audio.save("dowload/" + source , v2_version=3, v1=2) 

if __name__ == '__main__':
	search = [] 
	#clear directory dowload
	playlist = os.listdir("dowload")
	for l in playlist:
		os.remove("dowload/"+ l)

	#read lis song dowload
	with open("listMusic.txt") as f:
		search = f.read().split("\n")
	path_result = input("name playlist: ")

	#creat playlist
	file_path = "../" + path_result
	try:
		directory = os.mkdir(file_path)
	except:
		print("playlist exists")
	else:
		print("creat playlist true")
	# player
	p = vlc.MediaPlayer()
	
	result = []
	#dowload songs
	for s in  search:
		d = searchForSong(s)
		try:
			name = dowloadMusic(d)
		except:
			print("------------Dowload-------------")
			print("ERROR dowload")		
		else:	
			setImage(d["photo"],name)
			print("------------Dowload-------------")
			print("dowload true : " + name)		
			result.append("dowload true : " + name)
	
	#print result
	print("------------Dowload-------------")
	for s in result:
		print(s)

	#move songs in playlist
	playlist = os.listdir("dowload")
	for l in playlist:
		os.rename("dowload/"+ l, file_path+"/" + l)
