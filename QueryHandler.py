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
        get_systems_url = f'https://ofmpub.epa.gov/echo/sdw_rest_services.get_systems?output=JSON&p_fea=W&p_feay=3&p_qs={self.search}'
        try:
            response = requests.get(get_systems_url).json()
        except response.raise_for_status() as e:
            return []

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
        dfr_url = f'https://ofmpub.epa.gov/echo/dfr_rest_services.get_dfr?p_id={facility["PWSId"]}'
        response = requests.get(dfr_url).json()
        for field in fields:
            if field in response['Results']['Demographics'].keys():
            #if(len(response['Results']['Demographics'].keys()) > 0):
                data[field] = response['Results']['Demographics'][field]
            else:
                data[field] = 0
        data['dfr_url'] = facility['DfrUrl']
        return data

    def get_map_data(self):
        """
        Public method to be called to get list of places for the map handler to plot
        :return dict:
        """
        data = {}
        water_systems = self.query_and_get_water_systems()
        for sys in water_systems:
            dfr_details = self.query_and_get_dfr(sys)
            if len(dfr_details.keys()) > 0:
                data[sys['PWSName']] = dfr_details
        return data


