import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals
from views import get_single_animal
from views import get_all_locations
from views import get_single_location
from views import get_all_employees
from views import get_single_employee
from views import get_all_customers
from views import get_single_customer
from views import create_animal
from views import create_location
from views import create_employee
from views import create_customer
from views import delete_animal
from views import update_animal

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple


    def do_GET(self):
        
        response = {}  # Default Response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)

            else:
                response = get_all_animals()


        if response:
            self._set_headers(200)
                #check if response is empty and set 404 if it is
        else:
            self._set_headers(404)

        #self.wfile.write(json.dumps(response).encode())

        if resource == "locations":
            if id is not None:
                response = get_single_location(id)

            else:
                response = get_all_locations()

        if resource == "employees":
            if id is not None:
                response = get_single_employee(id)

            else:
                response = get_all_employees()

        if resource == "customers":
            if id is not None:
                response = get_single_customer(id)

            else:
                response = get_all_customers()

        self.wfile.write(json.dumps(response).encode())
    

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_animal = None

        if resource == "animals":
            new_animal = create_animal(post_body)

            self.wfile.write(json.dumps(new_animal).encode())

        new_location = None

        if resource == "locations":
            new_location = create_location(post_body)


        #Verify all keys and properties exist in all resources
        if "name" in post_body and "address" in post_body:
            self._set_headers(201)
            new_location = create_location(post_body)
        else:
            self._set_headers(400)
            new_location = {
                "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
            }

        # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_location).encode())
        # Initialize new animal
        new_employee = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "employees":
            new_employee = create_employee(post_body)

        # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_employee).encode())
        # Initialize new animal
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "customers":
            new_customer = create_customer(post_body)

        # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_customer).encode())




    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
        
    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    
    def do_DELETE(self):
    # Set a 204 response code
        #self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        if resource == "customers":
            self._set_headers(405)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()