from google.appengine.ext import ndb

class Allergy(ndb.Model):
    allergy = ndb.StringProperty(required = True)
    symptoms = ndb.StringProperty(repeated = True)
    toAvoid = ndb.StringProperty(repeated = True)
    images = ndb.StringProperty(repeated = True)
    commentNames = ndb.StringProperty(repeated = True)
    comments = ndb.StringProperty(repeated = True)

class Recipe(ndb.Model):
    title = ndb.StringProperty(required = True)
    link = ndb.StringProperty()
    allergenFree = ndb.StringProperty()
    basicIngredients = ndb.StringProperty()
    ingredients = ndb.StringProperty(repeated = True)
    steps = ndb.StringProperty(repeated = True)
    otherTags = ndb.StringProperty(repeated = True)

class Questions(ndb.Model):
    question = ndb.StringProperty()
    answerNames = ndb.StringProperty(repeated = True)
    answers = ndb.StringProperty(repeated = True)
