import webapp2
import os
import jinja2
from allergy import Allergy
from recipe import Recipe

theJinjaEnvironment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True)

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
    ('/banking', BankingPage),
    ('/transactions', TransactionsPage),
], debug=True)
