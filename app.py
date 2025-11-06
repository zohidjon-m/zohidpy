from webob import Request, Response

class ZohidPyApp:
    
    def __init__(self):
        self.routes = {}
        
     
    def __call__(self, environ, start_response):
        request = Request(environ)     
        response = self.handle_request(request)
        return response(environ, start_response)
  
  
    def handle_request(self, request):              
        response = Response()
        
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response                

        self.default_response(response)
        return response
         

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."
        
    
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper
