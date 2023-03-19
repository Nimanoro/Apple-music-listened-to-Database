#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing required libraris for the project
import xml.etree.ElementTree as ET

#building a data base file and establishing the connection to the file


fname = "Library.xml"
handle = open("Library.xml")




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
a=stuff.findall('dict/dict/dict/')

for line in a:
    name = lookup(line,"Name")
    artist= lookup(line,"Artist")
    genre= lookup(line, 'Genre')
    album= lookup(line, 'Album')
    
    
    
    

    song= []
    song.append(name)

print(song)
    
    
    
    
   


# In[ ]:




