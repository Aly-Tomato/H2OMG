"""
"""
import flask
from Index import Index
from Submit import Submit
from flask_googlemaps import GoogleMaps
import os

def get_api_key(txt_file):
    if os.path.exists(os.getcwd()+'/'+txt_file):
        with open(txt_file, 'r') as file:
            key = file.read()
        return key
    else:
        print("Error: need api key")

app = flask.Flask(__name__)       # our Flask app

# Get API key here: https://developers.google.com/maps/documentation/javascript/get-api-key
GoogleMaps(app, key=get_api_key('api_key.txt'))

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/submit.html',
                 view_func=Submit.as_view('submit'),
                 methods=["GET","POST"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

