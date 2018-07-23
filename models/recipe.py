from google.appengine.ext import ndb

class Recipe(ndb.Model):
    title = ndb.StringProperty(required = True)
    link = ndb.StringProperty()
    image = ndb.StringProperty()
    tags = ndb.StringProperty(repeated = True)
    allergens = ndb.StringProperty(repeated = True)
    ingredients = ndb.StringProperty(repeated = True)
    steps = ndb.StringProperty(repeated = True)
