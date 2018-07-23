from google.appengine.ext import ndb

class Allergy(ndb.Model):
    allergy = ndb.StringProperty(required = True)
    symptoms = ndb.StringProperty(repeated = True)
    toAvoid = ndb.StringProperty()
