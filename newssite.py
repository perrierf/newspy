import web
import model

urls = (
    '/', 'Index',
    '/specific/(.*)', 'Specific',
    '/specall/(.*)', 'SpecificAll',
    '/search', 'Search',
)

### Templates
t_globals = {"datestr": web.datestr}
render = web.template.render("templates", base="base", globals=t_globals)

class Index:
    def GET(self):
        article = model.get_articles()
        return render.index(article)

class Specific:
    def GET(self, source):
        """ View specific news source only 25"""
        specsource = model.get_sources(source)
        return render.specific(specsource)

class SpecificAll:
    def GET(self, source):
        """ View all articles from a specific news source """
        allarticles = model.get_allsourcearts(source)
        return render.specall(allarticles)

class Search:
    def POST(self):
        searchinput = model.get_input()
        return render.search(searchinput)


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()