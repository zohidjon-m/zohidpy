from waitress import serve
from app import ZohidPyApp


app = ZohidPyApp()


# /home
@app.route("/home")
def home(request, response):
    response.text = "hellp form home page"

# / about
@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"

# Optional: prevent favicon.ico spam
@app.route("/favicon.ico")
def favicon(request, response):
    response.status = 204  # No Content
    response.text = ""

serve(app, listen="localhost:8000")
'''
/home : home,
"/about": about
'''