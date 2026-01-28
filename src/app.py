from webob import Request, Response
from parse import parse
from urllib.parse import unquote
import inspect
class ZohidPyApp:
    
    def __init__(self):
        self.routes = {}
        
     
    def __call__(self, environ, start_response):
        request = Request(environ)     
        response = self.handle_request(request)
        return response(environ, start_response)
  
  
    def handle_request(self, request):              
        """
        Handle an incoming HTTP request and return a response.
        This method routes the request to the appropriate handler based on the request
        path and method. It supports both class-based and function-based handlers.
        Args:
            request: The HTTP request object containing method, path, and other request data.
        Returns:
            Response: A Response object containing the status code, headers, and body.
                     If no handler is found, returns the default response.
                     If the handler class does not support the request method,
                     returns a 405 Method Not Allowed response.
        Behavior:
            - Finds the appropriate handler for the request using find_handler().
            - If the handler is a class, instantiates it and calls the method
              corresponding to the HTTP request method (GET, POST, etc.).
            - If the handler is a function, calls it directly.
            - If no handler is found, returns the default response via default_response().
            - If a class-based handler does not implement the requested HTTP method,
              returns a 405 Method Not Allowed response.
        """
        response = Response()
              
        handler, kwargs = self.find_handler(request)
        
        if handler is not None:
            
            if inspect.isclass(handler):
                            
                handler_method = getattr(handler(), request.method.lower(), None)
                
                if handler_method is None:
                    response.status_code = 405
                    response.text = "Method Not Allowed"
                    return response
                
                handler_method(request, response, **kwargs)

            else:
                handler(request, response,**kwargs)
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
        
    def route(self, path):        
        if path in self.routes:
            raise AssertionError(f"Duplicated route {path}. Please change the URL.")
        
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper