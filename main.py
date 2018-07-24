import webapp2
import os
import jinja2
from allergy import Allergy
from recipe import Recipe
# from google.appengine.api import urlfetch

theJinjaEnvironment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True)

# finds and returns the allergy entity (with the allergy information)
# in the database of all allergens
def allergySearch():
    allergyDatabase = Allergy.query().fetch()
    allergySearch = self.request.get("allergySearch")
    allergy = ""
    for i in range(len(allergyDatabase)):
        if (allergyDatabase[i].allergy == allergySearch):
            allergy = allergyDatabase[i]
    return allergy

# def recipeFetch():
#     urlfetch.fetch(url)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcomeTemplate = theJinjaEnvironment.get_template('templates/welcome.html')
        self.response.write(welcomeTemplate.render())

class RecipeSubmitPage(webapp2.RequestHandler):
    def get(self):
        recipeSubmitTemplate = theJinjaEnvironment.get_template('templates/recipeSubmit.html')
        self.response.write(recipeSubmitTemplate.render())

class GenInfoPage(webapp2.RequestHandler):
    def get(self):
        genInfoTemplate = theJinjaEnvironment.get_template('templates/genInfo.html')
        self.response.write(genInfoTemplate.render())

class AllergyInfoPage(webapp2.RequestHandler):
    def get(self):
        allergyInfoTemplate = theJinjaEnvironment.get_template('templates/allergyInfo.html')
        self.response.write(allergyInfoTemplate.render())

class AllergySubmitPage(webapp2.RequestHandler):
    def get(self):
        allergySubmitTemplate = theJinjaEnvironment.get_template('templates/allergySubmit.html')
        self.response.write(allergySubmitTemplate.render())

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/submitRecipe', RecipeSubmitPage),
    ('/genInfo', GenInfoPage),
    ('/allergyInfo', AllergyInfoPage),
    ('/submitAllergy', AllergySubmitPage),
], debug=True)
