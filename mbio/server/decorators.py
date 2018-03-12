import sys
import json
import traceback
from functools import wraps

def handle_expcetions(f):
    """
    Handles any excepitons and returns the error message, as well as a 401
    response code back to the client.

    IMPORTANT: must only be used within BaseHTTPRequestHandler.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        handler = args[0]  # self

        try:
            f(*args, **kwargs)
        except Exception as e:
            handler.send_response(500)
            handler.send_header('Content-type','application/json')
            handler.end_headers()

            ret_json = {'error': 'An internal application error has occured.'}
            ret_json = json.dumps(ret_json)
            handler.wfile.write(ret_json.encode())

            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stdout)
            print(str(e))

    return decorated_function
