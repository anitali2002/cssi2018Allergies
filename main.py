import webapp2
import os
import jinja2
import ast
from models import Recipe
from models import Allergy
from google.appengine.api import urlfetch

theJinjaEnvironment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True)

# formats a string to all lower case, spaces taken out, and separated (by comma) into a list
def formatString(string):
    formattedString = string.lower()
    formattedString = formattedString.replace("; ", ";")
    stringList = formattedString.split(";")
    return stringList

# Finds and returns the allergy entity (with the allergy information)
# in the database of all allergens
def allergySearch():
    allergyDatabase = Allergy.query().fetch()
    allergySearch = self.request.get("allergySearch")
    allergy = ""
    for i in range(len(allergyDatabase)):
        if (allergyDatabase[i].allergy == allergySearch):
            allergy = allergyDatabase[i]
    return allergy

# RecipePuppy API call. Returns a list of recipe dictionaries.
# All recipes have "title", "href", "ingredients", and "thumbnail"
def recipeFetch(ingredients = "", type = ""):
    ingredients = ingredients.lower()
    ingredients = ingredients.replace(" ", "")
    type = type.lower()
    recipeSearch = "http://www.recipepuppy.com/api/?i="+ ingredients + "&q=" + type
    searchResult = urlfetch.fetch(recipeSearch)
    searchResult = ast.literal_eval(searchResult.content)
    recipes = searchResult["results"]
    return recipes

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcomeTemplate = theJinjaEnvironment.get_template('templates/welcome.html')
        self.response.write(welcomeTemplate.render())

class RecipeSubmitPage(webapp2.RequestHandler):
    def post(self):
        recipeSubmitTemplate = theJinjaEnvironment.get_template('templates/recipeSubmit.html')
        title = self.response.get("title")
        link = self.response.get("link")
        image = self.response.get("image")
        allergensFree = self.response.get("allergensFree") #list
        allergensFree = formatString(allergensFree)
        ingredients = self.response.get("ingredients") #list
        ingredients = formatString(ingredients)
        otherTags = self.response.get("otherTags") #list
        otherTags = formatString(otherTags)
        steps = self.response.get("steps") #list
        steps = formatString(steps)

        recipe = Recipe(title = title, link = link, image = image)
        recipe.put()
        for allergen in allergensFree:
            recipe.allergensFree.append(allergen)
        for ingredient in ingredients:
            recipe.ingredients.append(ingredient)
        for otherTag in otherTags:
            recipe.otherTags.append(otherTag)
        for step in steps:
            recipe.steps.append(step)

# class GenInfoPage(webapp2.RequestHandler):
#     def get(self):
#         genInfoTemplate = theJinjaEnvironment.get_template('templates/genInfo.html')
#         self.response.write(genInfoTemplate.render())
#
# class AllergyInfoPage(webapp2.RequestHandler):
#     def get(self):
#         allergyInfoTemplate = theJinjaEnvironment.get_template('templates/allergyInfo.html')
#         self.response.write(allergyInfoTemplate.render())
# # posts the selected recipe- if there is a link, goes to the link. if not, go to recipe html template
#     def post(self):
#         recipeTemplate = theJinjaEnvironment.get_template('templates/recipe.html')
#         allergyName = self.request.get("allergyName")
#
#         self.response.write(recipeTemplate.render())
#
# class AllergySubmitPage(webapp2.RequestHandler):
#     def get(self):
#         allergySubmitTemplate = theJinjaEnvironment.get_template('templates/allergySubmit.html')
#         self.response.write(allergySubmitTemplate.render())

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/submitRecipe', RecipeSubmitPage),
    # ('/genInfo', GenInfoPage),
    # ('/allergyInfo', AllergyInfoPage),
    # ('/submitAllergy', AllergySubmitPage),
], debug=True)
