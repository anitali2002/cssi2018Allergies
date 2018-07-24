from google.appengine.ext import ndb

class Allergy(ndb.Model):
    allergy = ndb.StringProperty(required = True)
    symptoms = ndb.StringProperty(repeated = True)
    toAvoid = ndb.StringProperty()

class Recipe(ndb.Model):
    title = ndb.StringProperty(required = True)
    link = ndb.StringProperty()
    image = ndb.StringProperty()
    allergensFree = ndb.StringProperty(repeated = True)
    ingredients = ndb.StringProperty(repeated = True)
    steps = ndb.StringProperty(repeated = True)
    otherTags = ndb.StringProperty(repeated = True)
