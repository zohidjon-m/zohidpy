from waitress import serve
from app import ZohidPyApp


app = ZohidPyApp()



serve(app, listen="localhost:8000")