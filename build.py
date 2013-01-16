#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import os
import sqlite3
import fnmatch

RESOURCES = "Contents/Resources/"
DOCUMENTS = RESOURCES + "Documents/"
PATH = DOCUMENTS + "silex.sensiolabs.org/"

SQL_INSERT = "INSERT INTO searchindex VALUES ( NULL, '%s', '%s', '%s')"

conn = sqlite3.connect('Contents/Resources/docSet.dsidx')

# DROP table
print "Dropping searchIndex"
conn.execute("drop table if exists searchIndex")

# CREATE table
print "Creating searchIndex"
conn.execute("create table if not exists searchIndex (id integer PRIMARY KEY AUTOINCREMENT, name string, type string, path string)")
conn.commit()

# GUIDES
files = glob.glob(PATH + "doc/*.html")
for filename in files:
    print "Parsing: " + filename
    soup = BeautifulSoup(open(filename).read())
    sections = soup.find_all("h1")[1]
    section = sections.get_text()[:-1]

    sql = SQL_INSERT % ( section, "Guide", filename[len(DOCUMENTS):] + "#" + sections.a['href'].split('#')[1] )
    conn.execute(sql)
    conn.commit()

    for item in soup.find_all('h2'):
        topic = item.get_text()[:-1]
        #print "\t" + topic
        anchor = item.a['href'].split('#')[1]
        entry = {
                'name': "%s - %s" % (section, topic),
                'docType': "Guide",
                'path': filename[len(DOCUMENTS):] + "#" + anchor
        }

        sql = SQL_INSERT % ( entry['name'], entry['docType'], entry['path'] )
        conn.execute(sql)
        conn.commit()

# Providers
files = glob.glob(PATH + "doc/providers/*.html")
for filename in files:
    if filename == PATH + "doc/providers/index.html":
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
                "path": filename[len(DOCUMENTS):] + "#" + anchor
        }
        sql = SQL_INSERT % ( entry['name'], entry['docType'], entry['path'] )
        conn.execute(sql)
        conn.commit()

# API
for root, dirnames, filenames in os.walk(PATH + "api/Silex"):
    for filename in fnmatch.filter(filenames, '*.html'):
        filePath = root + "/" + filename
        print "Parsing:",filePath
        htmlFile = root[len(DOCUMENTS):] + "/" + filename

        # parse the html
        soup = BeautifulSoup(open(filePath).read())
        name = soup.find_all("h1")[0].get_text()
        rawType = soup.find_all("div", class_ = "type")[0].get_text()

        # get the type
        if rawType == "Class":
            rawType = "Class"
            name = name.split('\\')[-1];
        elif rawType == "Interface":
            rawType = "Interface"
            name = name.split('\\')[-1];
        elif rawType == "Namespace":
            rawType = "Namespace"
        else:
            continue
        
        # Save the type to the db
        conn.execute(SQL_INSERT % (name, rawType, htmlFile))
        conn.commit()

        # process its methods
        methods = soup.select("h3")
        for method in methods:
            anchor = method["id"]
            methodName = method.select("code strong")[0]
            conn.execute(SQL_INSERT % (name + "::" + methodName.get_text(), "clm", htmlFile + "#" + anchor));

            conn.commit()

