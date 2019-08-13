from flask import render_template
from flask.views import MethodView
from MapHandler import MapHandler

class Index(MethodView):
    def get(self):
        mymap = MapHandler()
        return render_template('index.html', mymap=mymap.map, details={})
