#!/usr/bin/env python
# coding: utf-8
import unittest
import sqlite3



#importing required libraris for the project
import xml.etree.ElementTree as ET

#building a data base file and establishing the connection to the file


fname = input("Enter you apple music file name: ")
if len(fname) < 10:
    fname= "Library.xml"
handle = open(fname)
conn = sqlite3.connect('trackdb.sql')
cur =  conn.cursor()
cur.executescript('''
Drop table IF EXISTS Artist;
DROP TABLE IF EXISTS ALBUM;
DROP TABLE IF EXISTS Track;
CREATE TABLE Artist (id INTEGER not null primary key autoincrement unique,
name TEXT unique);

Create Table Album (id Integer not null primary key autoincrement unique,
Artist_id INTEGER,
Title TEXT);

Create Table Track (id Integer not null primary key autoincrement unique,
Title Text,
Album_id Integer,

len INTEGER, Rating INTEGER, Count Integer);
''')





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
    
    
stuff=ET.parse(handle)
all = stuff.findall('dict/dict/dict')
music_names = {}
for line in all:
    if (lookup (line, "Track ID") is None): continue
    name = lookup(line,'Name')
    artist= lookup(line,"Artist")
    genre= lookup(line, 'Genre')
    album= lookup(line, 'Album')
    rating= lookup(line, 'Rating')
    length = lookup(line, 'Total Time')
    count = lookup(line, 'Play Count')

    if name is None or artist is None or album is None:
        continue
    
    else:
        cur.execute('''Insert or ignore into Artist (name) Values (?)''', (artist, ))
        cur.execute('select id from Artist where name=?' , (artist, ))
        artist_id = cur.fetchone()[0]
        
        cur.execute('''Insert or ignore into album (title, artist_id) Values (?,?) ''',
        (album, artist_id))
        cur.execute('select id from Album where title=?' , (album, ))
        album_id = cur.fetchone()[0]

        cur.execute(''' Insert or replace into Track (title, album_id, len, rating, count)
        Values (?, ? , ?, ?, ?)''', (name, album_id, length, rating, count))

        conn.commit()


    