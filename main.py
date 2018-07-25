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
def allergySearch(allergySearch):
    allergyDatabase = Allergy.query().fetch()
    allergySearch = self.request.get("allergySearch")
    allergy = ""
    for i in range(len(allergyDatabase)):
        if (allergyDatabase[i].allergy == allergySearch):
            allergy = allergyDatabase[i]
    return allergy

# Finds and returns a list of recipes that fist the allergen-free parameter in the recipes database
def recipesSearch(allergenFree):
    recipesDatabase = Allergy.query().fetch()
    recipes = []
    for i in range(len(recipesDatabase)):
        if (allergenFree in recipesDatabase[i].allergensFree):
            recipes.append(recipesDatabase[i])
    return recipes

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

        allergyName = self.request.get("allergyName")
        templateDict = {
            "allergyName": allergyName
        }

        title = self.response.get("title")
        # link = self.response.get("link")
        # image = self.response.get("image")
        allergensFree = self.response.get("allergensFree") #list
        allergensFree = formatString(allergensFree)
        ingredients = self.response.get("ingredients") #list
        ingredients = formatString(ingredients)
        otherTags = self.response.get("otherTags") #list
        otherTags = formatString(otherTags)
        steps = self.response.get("steps") #list
        steps = formatString(steps)

        recipe = Recipe(title = title)
        recipe.put()

        for allergen in allergensFree:
            recipe.allergensFree.append(allergen)
        for ingredient in ingredients:
            recipe.ingredients.append(ingredient)
        for otherTag in otherTags:
            recipe.otherTags.append(otherTag)
        for step in steps:
            recipe.steps.append(step)

        self.response.write(recipeSubmitTemplate.render(templateDict))

class GenInfoPage(webapp2.RequestHandler):
    def get(self):
        genInfoTemplate = theJinjaEnvironment.get_template('templates/genInfo.html')

        questionsDatabase = Questions.query().fetch()

        userQuestion = self.request.get("question")
        question = ""

        for i in range(len(questionsDatabase)):
            if (questionsDatabase[i].question == userQuestions):
                question = questionsDatabase[i]

        if question == "":
            question = Questions(question = userQuestion)




        self.response.write(genInfoTemplate.render())

class AllergyInfoPage(webapp2.RequestHandler):
    # posts the selected recipe- if there is a link, goes to the link. if not, go to recipe html template
    def post(self):
        recipeTemplate = theJinjaEnvironment.get_template('templates/recipe.html')

        allergyName = self.request.get("allergyName")
        ingredientsSearch = self.request.get("ingredients")
        typeSearch = self.request.get("type")
        commentName = self.request.get("commentNames")
        comment = self.request.get("comments")

        allergy = allergySearch(allergyName)

        allergy.commentName.append(commentName)
        allergy.comment.append(comment)

        if (allergy == ""):
            self.redirect("/submitAllergy")
        else:
            templateDict = {
                "allergy": allergy.allergy,
                # put the submit recipe button in a form with a hidden tag with allergy to be passed
                "symptoms": allergy.symptoms,
                "toAvoid": allergy.toAvoid,
                "dataRecipes": recipesSearch(allergy.allergy),
                "APIRecipes": recipeFetch(ingredientsSearch, typeSearch),
                "commentName": allergy.commentName,
                "comment": allergy.comment
            }

        self.response.write(recipeTemplate.render(templateDict))

class AllergySubmitPage(webapp2.RequestHandler):
    def post(self):
        allergySubmitTemplate = theJinjaEnvironment.get_template('templates/allergySubmit.html')

        allergy = self.request.get("allergen")
        symptoms = self.request.get("symptoms")
        toAvoid = self.request.get("toAvoid")
        image = self.request.get("allergenImg")

        allergy = Allergy(allergy = allergy, symptoms = symptoms, toAvoid = toAvoid, image = image)
        allergy.put()

        self.response.write(allergySubmitTemplate.render())

class RecipePage(webapp2.RequestHandler):
    def post(self):
        recipeTemplate = theJinjaEnvironment.get_template('templates/recipe.html')
        self.response.write(recipeTemplate.render())

class ThanksPage(webapp2.RequestHandler):
    def post(self):
        thanksTemplate = theJinjaEnvironment.get_template('templates/recipe.html')

        submission = self.request.get("submission")

        if (submission == "recipe"):
            message = "Thank you for submitting an new recipe."
        if (submission == "allergy"):
            message = "Thank you for submitting an new allergy."

        self.response.write(thanksTemplate.render())

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/submitRecipe', RecipeSubmitPage),
    ('/genInfo', GenInfoPage),
    ('/allergyInfo', AllergyInfoPage),
    ('/submitAllergy', AllergySubmitPage),
    ('/recipe', RecipePage),
    ('/thanks', ThanksPage)
], debug=True)
