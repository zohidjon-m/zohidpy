import pytest




def test_basic_route_adding(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from home"
    

def test_double_routing_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from home"
        
    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Hello from home2"


def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from home"

    response = test_client.get("http://testingserver/home")
    
    assert response.text == "Hello from home"
    

def test_parameterized_routing(app, test_client):
    @app.route("/hello/{name}")
    def greeting(request, response, name):
        response.text = f"Hello {name}"
        
    
    assert test_client.get("http://testingserver/hello/Jahav").text == "Hello Jahav"
    assert test_client.get("http://testingserver/hello/Dima").text == "Hello Dima"
    

def test_default_response(test_client):
    response = test_client.get("http://testingserver/nonexit")
    
    assert response.text == "Not Found."
    assert response.status_code == 404
    

def test_class_based_get(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, req, resp):
            resp.text = "Books page"
        
    assert test_client.get("http://testingserver/books").text == "Books page"
    
def test_class_based_post(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create a book"
    
    assert test_client.post("http://testingserver/books").text == "Endpoint to create a book"
  
  
def test_class_based_method_not_allowed(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create a book"
    
    
    assert test_client.get("http://testingserver/books").text == "Method Not Allowed"
    

def test_alternative_route_adding(app, test_client):
    def new_handler(req, resp):
        resp.text = "From new handler"
        
        
    app.add_route("/new-handler", new_handler)
    
    
    assert test_client.get("http://testingserver/new-handler").text == "From new handler"