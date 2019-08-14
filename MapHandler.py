from flask_googlemaps import Map
import googlemaps

class MapHandler():
    def __init__(self, location="", data={}):
        # Default map of USA
        if location is "":
            lat = 37.0902
            long = -95.7129
            zoom = 4
            markers = []
        # City Map containing markers of facilities
        else:
            search = self.get_geocode(location)[0]
            lat = search['geometry']['location']['lat']
            long = search['geometry']['location']['lng']
            zoom = 12
            markers = []
            for mark in data:
                dfr_url = data[mark]['dfr_url']
                if data[mark]['CenterLatitude'] == 0 and data[mark]['CenterLongitude'] ==0:
                    geo = self.get_geocode(mark)[0]
                    data_lat = geo['geometry']['location']['lat']
                    data_lng = geo['geometry']['location']['lng']
                else:
                    data_lat = data[mark]['CenterLatitude']
                    data_lng = data[mark]['CenterLongitude']
                infobox_details = f'Facility Name: {mark}' + "\n"
                markers.append({
                    'icon': "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
                    'lat': data_lat,
                    'lng': data_lng,
                    'infobox': infobox_details + f"<a href='{dfr_url}' target='_blank'> Facility Details </a>"
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
        Helper function used to create Google Map Obj
        :return Google Map object:
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
        """
        Helper function to read api key from file.
        Sorry I didn't have a more creative way to do this.
        :param txt_file - containing key:
        :return void:
        """
        import os
        if os.path.exists(os.getcwd()+'/'+txt_file):
            with open(txt_file, 'r') as file:
                key = file.read()
            return key
        else:
            print("Error: need api key")

    def get_geocode(self, location):
        """
        Use googlemaps geocoding api to get lat & long coordinates
        :param location - to get geocode for:
        :return geo_results - google geocode response:
        """
        key = self.get_api_key('api_key.txt')
        gmap_geo = googlemaps.Client(key=key)
        geo_results = gmap_geo.geocode(location)
        return geo_results
