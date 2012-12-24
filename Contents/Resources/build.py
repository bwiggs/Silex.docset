#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import sqlite3

conn = sqlite3.connect('docSet.dsidx')

# DROP table
print "Dropping searchIndex"
conn.execute("drop table if exists searchIndex")

# CREATE table
print "Creating searchIndex"
conn.execute("create table if not exists searchIndex (id integer PRIMARY KEY AUTOINCREMENT, name string, type string, path string)")
conn.commit()

# GUIDES
files = glob.glob("Documents/silex.sensiolabs.org/doc/*.html")
for filename in files:
    print "Parsing: " + filename
    soup = BeautifulSoup(open(filename).read())
    sections = soup.find_all("h1")[1]
    section = sections.get_text()[:-1]

    sql = "INSERT INTO searchindex VALUES ( NULL, '%s', '%s', '%s')" % ( section, "Guide", filename[10:] + "#" + sections.a['href'].split('#')[1] )
    conn.execute(sql)
    conn.commit()

    for item in soup.find_all('h2'):
        topic = item.get_text()[:-1]
        #print "\t" + topic
        anchor = item.a['href'].split('#')[1]
        entry = {
                'name': "%s - %s" % (section, topic),
                'docType': "Guide",
                'path': filename[10:] + "#" + anchor
        }

        sql = "INSERT INTO searchindex VALUES ( NULL, '%s', '%s', '%s')" % ( entry['name'], entry['docType'], entry['path'] )
        conn.execute(sql)
        conn.commit()

# Providers
files = glob.glob("Documents/silex.sensiolabs.org/doc/providers/*.html")
for filename in files:
    if filename == "Documents/silex.sensiolabs.org/doc/providers/index.html":
        continue
    print "Parsing: " + filename
    soup = BeautifulSoup(open(filename).read())
    sections = soup.find_all("h1")
    for section in sections[1:]:
        topic = section.get_text().strip()[:-1]
        #print "\t" + topic
        anchor = section.a['href'].split('#')[1]
        entry = {
                "name": topic,
                "docType": "Guide",
                "path": filename[10:] + "#" + anchor
        }
        sql = "INSERT INTO searchindex VALUES ( NULL, '%s', '%s', '%s')" % ( entry['name'], entry['docType'], entry['path'] )
        conn.execute(sql)
        conn.commit()

# API
files = glob.glob("Documents/silex.sensiolabs.org/doc/providers/*.html")
for filename in files:
    if filename == "Documents/silex.sensiolabs.org/doc/providers/index.html":
        continue
    print "Parsing: " + filename
    soup = BeautifulSoup(open(filename).read())
    sections = soup.find_all("h1")
    for section in sections[1:]:
        topic = section.get_text().strip()[:-1]
        #print "\t" + topic
        anchor = section.a['href'].split('#')[1]
        entry = {
                "name": topic,
                "docType": "Guide",
                "path": filename[10:] + "#" + anchor
        }
        sql = "INSERT INTO searchindex VALUES ( NULL, '%s', '%s', '%s')" % ( entry['name'], entry['docType'], entry['path'] )
        conn.execute(sql)
        conn.commit()

