# ZohidPy

[![PyPI
version](https://img.shields.io/pypi/v/zohidpy.svg)](https://pypi.org/project/zohidpy/)
[![License](https://img.shields.io/badge/license-Apache-blue.svg)](LICENSE)
![purpose](https://img.shields.io/badge/purpose-learning-green)


> A lightweight WSGI web framework built from scratch to understand how web
frameworks work internally.

ZohidPy is intentionally small and explicit.\
It is designed for learning, experimentation, and understanding routing,
middleware, request/response handling, templating, and static file
serving without heavy abstractions.

------------------------------------------------------------------------


## Installation

``` bash
pip install zohidpy
```

------------------------------------------------------------------------

## Quick Start

``` python
from waitress import serve
from zohidpy.app import ZohidPy

app = ZohidPy()

@app.route("/home")
def home(request, response):
    response.text = "Hello from ZohidPy!"

if __name__ == "__main__":
    serve(app, listen="localhost:8000")
```

Run:

``` bash
python main.py
```

Visit:

http://localhost:8000/home

------------------------------------------------------------------------

## Features

-   Function-based routing
-   Class-based routing
-   Dynamic URL parameters
-   JSON / Text / HTML response helpers
-   Jinja2 template rendering
-   Static file serving (WhiteNoise)
-   Middleware system
-   Custom exception handlers
-   Built-in test client
-   Fully WSGI compatible

------------------------------------------------------------------------

## Routing

### Function-Based Routing

``` python
@app.route("/home")
def home(request, response):
    response.text = "Hello from home"
```

### Dynamic Routes

``` python
@app.route("/hello/{name}")
def greet(request, response, name):
    response.text = f"Hello {name}"
```

### Class-Based Routing

``` python
@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Create a book"
```

If a method is not defined, the framework returns:

    405 Method Not Allowed

### Restricting Allowed Methods

``` python
@app.route("/home", allowed_methods=["post"])
def home(request, response):
    response.text = "POST only"
```

------------------------------------------------------------------------

## Response Helpers

### JSON

``` python
resp.json = {"name": "zohid"}
```

Automatically sets:

    Content-Type: application/json

### Plain Text

``` python
resp.text = "Hello world"
```

Sets:

    Content-Type: text/plain

### HTML

``` python
resp.html = "<h1>Hello</h1>"
```

Sets:

    Content-Type: text/html

------------------------------------------------------------------------

## Templates (Jinja2)

Default directory:

    templates/

Example:

``` python
@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "home.html",
        context={"title": "My Page"}
    )
```

Custom template directory:

``` python
app = ZohidPy(templates_dir="my_templates")
```

------------------------------------------------------------------------

## Static Files

Static files are served using WhiteNoise.

Default directory:

    static/

Accessible via:

    /static/filename.css

Custom directory:

``` python
app = ZohidPy(static_dir="assets")
```

------------------------------------------------------------------------

## Middleware

Create middleware by subclassing `Middleware`:

``` python
from zohidpy.middleware import Middleware

class LoggingMiddleware(Middleware):
    def process_request(self, req):
        print("Request:", req.url)

    def process_response(self, req, resp):
        print("Response generated")

app.add_middleware(LoggingMiddleware)
```

Middleware lifecycle:

1.  process_request
2.  route handler
3.  process_response

------------------------------------------------------------------------

## Custom Exception Handling

``` python
def on_exception(req, resp, exc):
    resp.text = "Something went wrong"

app.add_exception_handler(on_exception)
```

------------------------------------------------------------------------

## Testing

ZohidPy includes a built-in test client:

``` python
test_client = app.test_session()
```

Example test:

``` python
def test_home(app, test_client):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello"

    response = test_client.get("http://testingserver/home")
    assert response.text == "Hello"
```

------------------------------------------------------------------------

## Deployment

ZohidPy is fully WSGI-compatible.

### Waitress

``` bash
waitress-serve --listen=0.0.0.0:8000 main:app
```

### Gunicorn

``` bash
gunicorn main:app
```

------------------------------------------------------------------------

## Internal Architecture Overview

High-level request flow:

1.  WSGI entry point receives request
2.  Static files handled via WhiteNoise
3.  Middleware layer executes
4.  Route resolution via pattern matching
5.  Handler execution
6.  Response object constructs final WebOb response

The design favors clarity over abstraction.

------------------------------------------------------------------------

##  License
This project is licensed under the **Apache License 2.0** — see the [LICENSE](./LICENSE) file for details.

---

##  Author
**Zohidjon Mahmudjonov**  
- GitHub: [@zohidjon-m](https://github.com/zohidjon-m)  
- Email: zohidjon.mah@gmail.com