from webob import Request, Response

class ZohidPyApp:
    def __call__(self, environ, start_response):
      request = Request(environ)
      
      response = Response()
      
      response = self.handle_request(request)
      
      return response(environ, start_response)
  
  
    def handle_request(self, request):
        print(request.environ)
        user_agent = request.environ.get("HTTP_USER_AGENT", "User Agent is not found")
        
        
        response = Response()
        response.text = f"Hello mu friend with user agen {user_agent}"
        
        return response