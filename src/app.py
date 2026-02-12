from webob import Request, Response
from parse import parse
from urllib.parse import unquote
import inspect
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from whitenoise import WhiteNoise
from .middleware import Middleware
class ZohidPy:
    
    def __init__(self, templates_dir="templates", static_dir = "static", root_dir=None):
        self.routes = {}
        self.exception_handler = None
        self.middleware = Middleware(self)
        
        root = Path(root_dir) if root_dir else Path(__file__).resolve().parent.parent

        templates_path = (Path(templates_dir) if Path(templates_dir).is_absolute() else root / templates_dir).resolve()
        static_path = (Path(static_dir) if Path(static_dir).is_absolute() else root / static_dir).resolve()

        self.template_env = Environment(loader=FileSystemLoader(str(templates_path)))
        self.whitenoise = WhiteNoise(self.wsgi_app, root=str(static_path), prefix = "/static")
     
    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]
        
        if path_info.startswith("/static"):
            return self.whitenoise(environ, start_response)
        else:
            return self.middleware(environ, start_response)
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)     
        response = self.handle_request(request)
        return response(environ, start_response)
  
  
    def handle_request(self, request):              
        response = Response()
              
        handler, kwargs = self.find_handler(request)
        
        if handler is not None:
            if inspect.isclass(handler):         
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    response.status_code = 405
                    response.text = "Method Not Allowed"
                    return response
            try:    
                handler(request, response,**kwargs)
            except Exception as e:
                if self.exception_handler is not None:
                    self.exception_handler(request, response, e)
                else:
                    raise
                    
        else:   
            self.default_response(response)
        
        return response
         
    def find_handler(self, request):
        for route, handler in self.routes.items():
            parsed_result = parse(route, request.path)
            
            if parsed_result is not None:
                return handler, parsed_result.named  
            
        return None, None          
    
    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."
       
    def add_route(self, path, handler):
        if path in self.routes:
            raise AssertionError(f"Duplicated route {path}. Please change the URL.")
        self.routes[path] = handler
        
 
    def route(self, path):        
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        
        return wrapper
    
    
    def test_session(self):
        session = requests.Session()
        session.mount('http://testingserver', wsgiadapter.WSGIAdapter(self))
        return session
    
    def template(self, template_name, context=None):
        if context is None:
            context = {}
            
        return self.template_env.get_template(template_name).render(**context).encode()
    
    def add_exception_handler(self, handler):
        self.exception_handler = handler
        
    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)