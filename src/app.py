from webob import Request, Response
from parse import parse
from urllib.parse import unquote
import inspect
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
import os
from whitenoise import WhiteNoise
class ZohidPy:
    
    def __init__(self, templates_dir="templates", static_dir = "static"):
        self.routes = {}
        self.exception_handler = None
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        project_root = os.path.normpath(os.path.join(base_dir, ".."))
        
        if not os.path.isabs(templates_dir):
            templates_dir = os.path.join(project_root, templates_dir)
        if not os.path.isabs(static_dir):
            static_dir = os.path.join(project_root, static_dir)

        templates_dir = os.path.normpath(os.path.abspath(templates_dir))
        static_dir = os.path.normpath(os.path.abspath(static_dir))

        self.template_env = Environment(loader=FileSystemLoader(templates_dir))
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

     
    def __call__(self, environ, start_response):
       return self.whitenoise(environ, start_response)
    
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