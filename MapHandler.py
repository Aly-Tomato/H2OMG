from flask_googlemaps import Map
import googlemaps

class MapHandler():
    def __init__(self, location="", data={}):
        if location is "":
            lat = 37.0902
            long = -95.7129
            zoom = 4
            markers = []
        else:
            search = self.get_geocode(location)[0]
            lat = search['geometry']['location']['lat']
            long = search['geometry']['location']['lng']
            zoom = 12
            markers = []
            for mark in data:
                dfr_url = data[mark]['dfr_url']
                markers.append({
                    'icon': "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
                    'lat': data[mark]['CenterLatitude'],
                    'lng': data[mark]['CenterLongitude'],
                    'infobox': f"<a href='{dfr_url}' target='_blank'> Facility Details </a>"
                })
        self.map_config={
            'lat': lat,
            'long': long,
            'zoom': zoom,
            'markers': markers
        }
        self.map = self.get_map()

    def get_map(self):
        """
        Helper function to determine which type of recipes should be selected
        :param type: Type of recipe ex. 'Vegetarian', 'Gluten Free', 'Pescatarian', None
        :return: Google Map object
        """
        return Map(
            identifier="view-side",
            lat=self.map_config['lat'],
            lng=self.map_config['long'],
            zoom=self.map_config['zoom'],
            markers=self.map_config['markers'],
            style="height:60%; width:75%; margin:1;"
        )

    def get_api_key(self, txt_file):
        import os
        if os.path.exists(os.getcwd()+'/'+txt_file):
            with open(txt_file, 'r') as file:
                key = file.read()
            return key
        else:
            print("Error: need api key")

    def get_geocode(self, location):
        """ use googlemaps geocoding api to get lat & long coordinates
        :param county:
        :return:
        """
        key = self.get_api_key('api_key.txt')
        gmap_geo = googlemaps.Client(key=key)
        geo_results = gmap_geo.geocode(location)
        return geo_results
