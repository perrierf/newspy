import web, datetime

db = web.database(dbn='mysql', host='localhost', database='newspy', user='root', password='Fadges12')

def get_articles():
    return db.query("select distinct source, iconURL from articles where source is not null order by source")


def get_sources(source):
    try:
        return db.select('articles', where="source=$source", order="created DESC", limit=25, vars=locals())
    except IndexError:
        return None

def get_allsourcearts(source):
    try:
        return db.select('articles', where="source=$source", order="created DESC", vars=locals())
    except IndexError:
        return None

def get_input():
    i = web.input()
    userinput = i.description
    splitmultiple = userinput.split()
    joinmultiple = ' '.join(splitmultiple)
    querystring = f"SELECT *, MATCH (title,description,source, authors, keywords, url) AGAINST ('+{joinmultiple}' IN BOOLEAN MODE) as score FROM articles where match(title,description,source,authors,keywords,url) against('+{joinmultiple}' IN BOOLEAN MODE) > 0 order by score DESC LIMIT 100"
    return db.query(querystring)