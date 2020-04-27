#!/usr/bin/python3

import sys
import newspaper
from newspaper import news_pool
import mysql.connector
from mysql.connector import Error
import requests
import favicon

firstarg = sys.argv[1]
secondarg = sys.argv[2]

print(firstarg, secondarg)


x = 0
allpapers = newspaper.popular_urls()
for n in allpapers:
    x += 1

if int(secondarg)<x:
    print("there are that many papers", x)
    sourcearts = []
    for paper in allpapers[int(firstarg):int(secondarg)]:
        sourcepaper = newspaper.build(paper)
        sourcearts.append(sourcepaper)

    poolset = news_pool.set(sourcearts, threads_per_source=3) # (3*2) = 6 threads total
    pooljoin = news_pool.join()
    iart = 0
    for iart in range(len(sourcearts)):
        print("newspaper {}: {}".format(iart + 1, sourcearts[iart].size()))

    iart = 0
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='newspy',
                                             user='root',
                                             password='Fadges12')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            for iart in range(len(sourcearts)):
                articlecount = 0
                for article in sourcearts[iart].articles:
                    try:
                        icons = favicon.get(paper)
                        icon = icons[0]
                        iconurlbig = icon[0]
                        newartsrc = sourcearts[iart].brand
                        article_number = sourcearts[iart].articles[articlecount]
                        article_number.download()
                        article_number.parse()
                        arttitle = article_number.title
                        arturl = article_number.url
                        artauthor = ', '.join(article_number.authors)
                        article_number.nlp()
                        artsum = article_number.summary
                        artimg = article_number.top_image
                        artkeys = ', '.join(article_number.keywords)
                        sqlinsert = "INSERT INTO articles (source, title, url, description, imgsrc, authors, keywords, iconURL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        valuessql = (newartsrc, arttitle, arturl, artsum, artimg, artauthor, artkeys, iconurlbig)
                        try:
                            result = cursor.execute(sqlinsert, valuessql)
                            print("successfully inserted data")
                            result = connection.commit()
                            print("successfully committed changes to table for {} on article number {}".format(arturl, articlecount))
                        except mysql.connector.Error as error:
                            print("Failed to insert into table in MySQL: {}".format(error))
                            articlecount += 1
                        articlecount += 1
                    except:
                        pass
                        e = sys.exc_info()[0]
                        print( "Error: %s" % e )
                        print('failed on article for {}'.format(articlecount))
                        articlecount += 1    
                iart += 1    
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    x += 1
else:
    print("second argument is greater than number of papers", x)
