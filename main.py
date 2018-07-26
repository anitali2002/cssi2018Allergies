import webapp2
import os
import jinja2
import ast
from models import Recipe
from models import Allergy
from models import Questions
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
    allergy = None

    for i in range(len(allergyDatabase)):
        if (allergyDatabase[i].allergy == allergySearch):
            allergy = allergyDatabase[i]

    return allergy

# Finds and returns a list of recipes that fist the allergen-free parameter in the recipes database
def recipesSearch(allergenFree):
    recipesDatabase = Recipe.query().fetch()
    recipes = []

    for i in range(len(recipesDatabase)):
        if (allergenFree in recipesDatabase[i].allergenFree):
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
    def get(self):
        self.post()

    def post(self):
        recipeSubmitTemplate = theJinjaEnvironment.get_template('templates/recipeSubmit.html')

        allergyName = self.request.get("allergyName")

        templateDict = {
            "allergyName": allergyName
        }

        self.response.write(recipeSubmitTemplate.render(templateDict))

class GenInfoPage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        genInfoTemplate = theJinjaEnvironment.get_template('templates/genInfo.html')

        questionsDatabase = Questions.query().fetch()

        userQuestion = self.request.get("userQuestion")

        question = None

        for i in range(len(questionsDatabase)):
            if (questionsDatabase[i].question == userQuestion):
                question = questionsDatabase[i]

        if question == None and not userQuestion == "":
            question = Questions(question = userQuestion)
            question.put()

        answerName = self.request.get("answerName")
        answer = self.request.get("answer")
        questionKey = self.request.get("questionKey")

        if (not answerName == "" and not answer == ""):
            for i in range(len(questionsDatabase)):
                if (questionsDatabase[i].question == questionKey):
                    question = questionsDatabase[i]
            question.answerNames.append(answerName)
            question.answers.append(answer)
            question.put()

        questionsDatabase = Questions.query().fetch()

        questionsDatabase.append(question)

        print(questionsDatabase)

        templateDict = {
            "questionsDatabase": questionsDatabase
        }

        self.response.write(genInfoTemplate.render(templateDict))

class AllergyInfoPage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        allergyTemplate = theJinjaEnvironment.get_template('templates/allergyInfo.html')

        allergyName = self.request.get("allergyName")

        allergy = allergySearch(allergyName)

        # posts the selected recipe- if there is a link, goes to the link. if not, go to recipe html template
        if (allergy == None):
            self.redirect("/submitAllergy")
            return

        ingredientsSearch = self.request.get("ingredients") + ",-" + allergyName
        typeSearch = self.request.get("type")

        allergy = allergySearch(allergyName)
        print(allergy)

        if (allergy == ""):
            self.redirect("/submitAllergy")

        # comments about the allergy
        commentName = self.request.get("commentName")
        comment = self.request.get("comment")

        if (not commentName == "" and not comment == ""):
            allergy.commentNames.append(commentName)
            allergy.comments.append(comment)

        allergy.put()

        templateDict = {
            "allergyName": allergy.allergy,
            "symptoms": allergy.symptoms,
            "images": allergy.images
            "toAvoid": allergy.toAvoid,
            "dataRecipes": recipesSearch(allergy.allergy),
            "apiRecipes": recipeFetch(ingredientsSearch, typeSearch),
            "commentName": allergy.commentNames,
            "comment": allergy.comments
        }

        self.response.write(allergyTemplate.render(templateDict))

# allergy submit page will just go back home
class AllergySubmitPage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        allergySubmitTemplate = theJinjaEnvironment.get_template('templates/allergySubmit.html')
        self.response.write(allergySubmitTemplate.render())

class RecipePage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        recipeTemplate = theJinjaEnvironment.get_template('templates/recipe.html')

        recipeName = self.request.get("recipeName")

        recipesDatabase = Recipe.query().fetch()

        recipe = None

        for i in range(len(recipesDatabase)):
            if (recipesDatabase[i].title == recipeName):
                recipe = recipesDatabase[i]

        allergyName = self.request.get("allergyName")

        templateDict = {
            "allergyName": allergyName,
            "title": recipe.title,
            "allergenFree": recipe.allergenFree,
            "otherTags": recipe.otherTags,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "imageLink": recipe.image
        }

        self.response.write(recipeTemplate.render(templateDict))

class ThanksPage(webapp2.RequestHandler):
    def post(self):
        thanksTemplate = theJinjaEnvironment.get_template('templates/thanks.html')

        allergyName = self.request.get("allergyName")
        submission = self.request.get("submission")

        message = ""
        destination = ""

        if (submission == "recipe"):
            #recipe submit
            title = self.request.get("title")
            link = self.request.get("link")
            image = self.request.get("image")
            allergenFree = self.request.get("allergenFree")
            ingredients = self.request.get("ingredients") #list
            ingredients = formatString(ingredients)
            otherTags = self.request.get("otherTags") #list
            otherTags = formatString(otherTags)
            steps = self.request.get("steps") #list
            steps = formatString(steps)

            recipe = Recipe(title = title, allergenFree = allergenFree)

            for ingredient in ingredients:
                recipe.ingredients.append(ingredient)
            for otherTag in otherTags:
                recipe.otherTags.append(otherTag)
            for step in steps:
                recipe.steps.append(step)

            recipe.put()

            message = "Thanks for submitting an new recipe."
            destination = "/allergyInfo?allergyName=" + allergenFree

        if (submission == "allergy"):
            # allergy submit
            allergy = self.request.get("allergen")
            symptoms = self.request.get("symptoms")
            toAvoid = self.request.get("toAvoid")
            images = self.request.get("allergenImg")
            images = formattedString.split(";")


            allergy = Allergy(allergy = allergy, symptoms = symptoms, toAvoid = toAvoid)

            for link in images:
                allergy.images.append(link)

            allergy.put()

            message = "Thanks for submitting an new allergy."
            destination = "/"

        templateDict = {
            # "allergyName": allergyName,
            "message": message,
            "destination": destination
        }

        self.response.write(thanksTemplate.render(templateDict))

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/submitRecipe', RecipeSubmitPage),
    ('/genInfo', GenInfoPage),
    ('/allergyInfo', AllergyInfoPage),
    ('/submitAllergy', AllergySubmitPage),
    ('/recipe', RecipePage),
    ('/thanks', ThanksPage)
], debug=True)
