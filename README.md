# Method 1 (not secured but easy and simple) 
If you do not need secure websocket than you can follow method 1.

## run it
env/bin/python -m daphne -b 0.0.0.0 -p 9000 configurations.asgi:application
## url
url of websocket is: ws://localhost:9000/ws/<ty_pe>/<p_k>/<user_id>/

# Method 2 (secured but complex)
You can fill the variables under websocket_app/consumers.py.
If you need secure websocket than you should fill the required fields.

### websocket_app/consumers.py.
backend_base_url="http://localhost:8000/"
#### variable 1
url_for_check_permission_on_support=None
this url should work on get request and return a json with
{
    "permission":true/false,
    "other data":"other data"
}
#### variable 2
url_for_send_message_on_support=None
this url should work on post request to save the message on backend database

#### variable 3
url_for_check_permission_on_chat=None
this url should work on get request and return a json with
{
    "permission":true/false,
    "other data":"other data"
}
#### variable 4
url_for_send_message_on_chat=None
this url should work on post request to save the message on backend database

## run it
env/bin/python -m daphne -b 0.0.0.0 -p 9000 configurations.asgi:application
## url
url of websocket is: ws://localhost:9000/ws/<ty_pe>/<p_k>/<to_ken>/