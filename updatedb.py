#!/usr/bin/python3.6

import pymysql, datetime, requests, json

connection = pymysql.connect(host = "djones8055.mysql.pythonanywhere-services.com",
                             user = "djones8055",
                             password = input("what is the password?"),
                             db = "djones8055$testdb",
                             charset = 'utf8')
cursor = connection.cursor()

# set database to use utf8?
# i added this when troubleshootinh something
# im not sure if i still need it, maybe one
# day i will try removing it and see if anything changes
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print()
print("database version : %s " % data)
print()

def movetable():
    """ move the current table to a timestamped backup"""
    # get a list of the tables
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    # the tables are tuples nested in touples so i use
    # a nested loop to find and rename the top100 list
    for r in tables:
        if "top100" in r:
            print("found table")
            print("renaming table")

            # timestamp and back up the current top 100 table
            # time stamps for now instead of when the table was made
            # figure out how to fix that maybe?
            cursor.execute("ALTER TABLE top100 RENAME TO " + formattime() + ";")
            connection.commit()



def formattime():
    """ format date and time to be used as a timestamp filename"""

    # I came back through the code to comment everything
    # really well. This function is still shit.

    # get the time and date, split into two pieces
    gettime = str(datetime.datetime.now()).split(" ")

    # there has to be a better way to do this...
    year = str(gettime[0]).split("-")[0]
    month = str(gettime[0]).split("-")[1]
    day = str(gettime[0]).split("-")[2]

    hour = str(gettime[1]).split(":")[0]
    minute = str(gettime[1]).split(":")[1]
    second = str(gettime[1]).split(":")[2].split(".")[0]

    filetime = month + day + year + "_" + hour + minute + second
    return filetime

def newtable():
    """ make the new table for the new top100 list, but does not
    add anything to it """

    # creates the table. I figured out how to break the one
    # long line into a few smaller ones. i didnt have to tell
    # you that but i had a comment here to do it and i did.
    cursor.execute("CREATE TABLE top100 (`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`artistname` varchar(512) COLLATE utf8_bin NOT NULL,"
        "`songname` varchar(512) COLLATE utf8_bin NOT NULL,"
        "`value` int(11) NOT NULL,"
        "`prevpos` int(11) NOT NULL,"
        "PRIMARY KEY(`ID`))"
        "DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT = 1;")

    # save everything. Incase everything goes to
    # shit after this.
    connection.commit()

    # why not let me know how far i have gotten with no errors
    print("made new table")

def gettop110():
    """get a list of the top 110 songs on itunes"""
    # the url that serves the info i want from apple
    # the number of results can be changed by changing
    # the number after the /all/ and before  /explicit/
    # tags..... just sayin`...
    url = "https://rss.itunes.apple.com/api/v1/us/apple-music/hot-tracks/all/110/explicit.json"

    # throw an error if i cant get the data
    response = requests.get(url)
    response.raise_for_status()

    # load data with json and store it in music data
    musicdata = json.loads(response.text)

    # goes down two levels into json data and retrieve the
    # bit that i actually want and return that list
    return musicdata['feed']['results']


# the only part of the code that does anything
# rename the top100 table to a datecode
movetable()

# make new top100 table in database
newtable()

# make a list of the data gathered in gettop100 function
top110 = gettop110()

# loop over every item in top100 and write it to top100 table
for i in top110:

    # the position is always the index + 1 so name it that
    pos = top110.index(i) + 1

    # stupid value system for now, just to show idea
    # add a lot more math stuffs here
    value = (110 - pos)

    # format to send to the sql wrapper
    data = (pos,i['artistName'], i['name'], value)

    # print it, because, why not?
    #print(data)

    # send it to the database!! The only part that really
    # matters.
    cursor.execute('INSERT INTO top100 (prevpos, artistname, songname, value)'
        'VALUES (%s , %s, %s, %s);', data)

    # commit the changes to the db, write it, blah blah blah
    connection.commit()

# close the connection to the database
# maybe this should be somewhere else?
connection.close
print()
print('Database updated')
print('Everything went o.k.')
