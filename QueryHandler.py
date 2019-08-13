"""
Sends and receives queries made to the EPA ECHO Rest API

File: QueryHandler.py
"""
import requests

class QueryHandler():
    def __init__(self, search):
       self.search = search


    def query_and_get_water_systems(self):
        """
        Sends requests to EPA's Drinking Water System Search REST Services
        :return list of water_systems:
        """
        # Use get_systems to validate passed query params to obtain QID
        self.search = self.search.replace(" ", "%20")
        self.search = self.search.replace(",", "%2C")
        get_systems_url = f'https://ofmpub.epa.gov/echo/sdw_rest_services.get_systems?output=JSON&p_health=Y&p_qs={self.search}'
        response = requests.get(get_systems_url).json()

        # Use get_qid with returned QID to paginate through water systems
        qid = response['Results']['QueryID']
        get_qid_url = f'https://ofmpub.epa.gov/echo/sdw_rest_services.get_qid?qid={qid}&pageno=1'
        response = requests.get(get_qid_url).json()
        water_systems = response['Results']['WaterSystems']
        return water_systems

    def query_and_get_dfr(self, facility):
        """
        Send requests to the EPA's Detailed Facility Report Rest Services
        :return (lat, long) of facility:
        """
        data = {}
        fields = ['CenterLatitude', 'CenterLongitude']
        dfr_url = f'https://ofmpub.epa.gov/echo/dfr_rest_services.get_dfr?p_id={facility}'
        response = requests.get(dfr_url).json()
        for field in fields:
            data[field] = response['Results']['Demographics'][field]
        return data

    def get_map_data(self):
        """
        Public method to be called to get list of places for the map handler to plot
        :return dict:
        """
        data = {}
        water_systems = self.query_and_get_water_systems()
        for sys in water_systems:
            data[sys['PWSName']] = self.query_and_get_dfr(sys['PWSId'])
        return data


