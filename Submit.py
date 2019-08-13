from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from QueryHandler import QueryHandler
from MapHandler import MapHandler

class Submit(MethodView):
    def get(self):
        return render_template('submit.html')

    def post(self):
        location = request.form['location']
        query = QueryHandler(location)
        data = query.get_map_data()
        mymap = MapHandler(location, data)
        return render_template('index.html', mymap=mymap.map, details=data, total=len(data.keys()))
