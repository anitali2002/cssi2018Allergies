from google.appengine.ext import ndb

class Allergy(ndb.Model):
    allergy = ndb.StringProperty(required = True)
    symptoms = ndb.StringProperty() #possible required = True later on when working with crowdsourced adding
    toAvoid = ndb.StringProperty() #possible required = True later on when working with crowdsourced adding

class Recipe(ndb.Model):
    title = ndb.StringProperty(required = True)
    link = ndb.StringProperty()
    image = ndb.StringProperty()
    allergensFree = ndb.StringProperty(repeated = True)
    ingredients = ndb.StringProperty(repeated = True)
    steps = ndb.StringProperty(repeated = True)
    otherTags = ndb.StringProperty(repeated = True)