from waitress import serve
from src.app import ZohidPy


app = ZohidPy()


# /home
@app.route("/home")
def home(request, response):
    response.text = "hellp form home page"

# / about
@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"
    
@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"hello {name}"
    
    
    
    
@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


@app.route("/template")
def template_handler(req, resp):
      resp.body=app.template(
          "home.html",
          context={"new_title":"New Title", "new_body":"New body"}
      )         
        
        
        
        
        
        
        
        
        
        
# prevent favicon.ico spam
@app.route("/favicon.ico")
def favicon(request, response):
    response.status = 204  # No Content
    response.text = ""

serve(app, listen="localhost:8000")
'''
/home : home,
"/about": about
'''