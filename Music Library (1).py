#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing required libraris for the project
import sqlite3
import xml.etree.ElementTree as ET

#building a data base file and establishing the connection to the file
conn=sqlite3.connect("musicdb.sqlite")
cur=conn.cursor()

#building data tables required for the project in the database
cur.executescript('''
DROP TABLE IF EXISTs Artist;
Drop Table if exists Genre;
Drop Table if exists Album;
Drop Table if exists Track;

Create Table Artist (
id integer NOT NULL primary key autoincrement unique,
name text unique);

Create table Album (
id integer not null primary key autoincrement unique,
title text unique,
Artist_id integer);

Create Table Genre (
id integer NOT NULL primary key autoincrement unique,
name text unique);

Create table Track (
Title text unique,
Artist_id integer,
Album_id integer,
Genre_id integer
);

''')

fname=input("")

if len(fname)<1:
    fname="library.xml"
handle= open(fname)



#key>Track ID</key><integer>369</integer><key>Name</key><string>Another One Bites The Dust</string>
#<key>Artist</key><string>Queen</string><key>Genre</key><string>Rock</string>
#<key>Composer</key><string>John Deacon</string><key>Album</key><string>Greatest Hits</string>

#defining the lookup function

def lookup(d,key):
    found= False
    for child in d:
        if found:
            return child.text 
        if child.tag=='key' and child.text ==key:
            found=True
    return None
    
stuff=ET.parse(handle)
a=stuff.findall('dict/dict/dict')

for line in a:
    name = lookup(line,"Name")
    artist= lookup(line,"Artist")
    genre= lookup(line, 'Genre')
    album= lookup(line, 'Album')
    
    if name is None or artist is None or genre is None or album is None:
        continue
   
    cur.execute('Insert or ignore into Genre(name) Values (?)',(genre,))
    cur.execute('select id from Genre where name ==?',(genre,))
    genre_id= cur.fetchone()[0]
    
    cur.execute('insert or ignore into Artist(name) values (?)',(artist,))
    cur.execute ('select id from Artist where name == ?', (artist,))
    artist_id= cur.fetchone()[0]
    
    cur.execute ('insert or ignore into album (title,artist_id) values (?,?)',(album,artist_id))
    cur.execute('select id from Album where title==?', (album,))
    album_id= cur.fetchone()[0]

    
    cur.execute ('''insert or ignore into track (title,artist_id, album_id, Genre_id) 
    values (?,?,?,?)''', (name,artist_id,album_id,genre_id))
    
    conn.commit()
    
    
   


# In[ ]:




