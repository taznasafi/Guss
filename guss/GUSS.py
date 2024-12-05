import requests
import pandas as pd
import warnings
import json
import os
import ast
from guss.gussErrors import GussExceptions
from guss.GEO_CENSEY import Fipsy

from . import DATA_INPUT, DATA_OUTPUT,CSV_OUTPUT, GPK_OUTPUT, SHP_OUTPUT

class Guss:

    def __init__(self, **credentials):
        self.__username = credentials['USERNAME']
        self.__hash_value = credentials['HASH_VALUE']
        self.__baseUrl = os.environ['BASE_URL']
        self.__url_endpoint = None
        self.__request_type = None
        self.__request_header = None
        self.__request_param = None
        self.__response = None

    @property
    def baseUrl(self):
        return self.__baseUrl

    @baseUrl.setter
    def baseUrl(self, value):
        self.__baseUrl = value

    @property
    def url_endpoint(self):
        return self.__url_endpoint

    @url_endpoint.setter
    def url_endpoint(self, value):
        self.__url_endpoint = value

    @url_endpoint.getter
    def url_endpoint(self):
        return self.__url_endpoint

    @property
    def request_type(self):
        return self.__request_type

    @request_type.setter
    def request_type(self, value):
        self.__request_type = value

    @property
    def request_header(self):
        return self.__request_header

    @request_header.setter
    def request_header(self, value):
        self.__request_header = value

    @property
    def request_param(self):
        return self.__request_param

    @request_param.setter
    def request_param(self, value):
        self.__request_param = value

    @request_param.getter
    def request_param(self):
        return self.__request_param

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, value):
        self.__response = value

    @response.getter
    def response(self):
        return self.__response

    def __repr__(self):
        return f"method: {self.request_type}, request_base_url: {self.baseUrl}, requst_end_point: {self.url_endpoint}, request_param: {self.request_param}"

    # saves output file in location
    def save_file(self, response, output_path, file_name):
        output = os.path.join(output_path, file_name)
        with open(output, 'wb') as f:
            f.write(response)
        print(f"Saved File to: {output}")

    def send_request(self, return_df=None, save_file=False, file_name=None, gis_data_type=None):

        try:

            self.request_header = {
                'username': self.__username,
                'hash_value': self.__hash_value
            }

            url = f"{self.baseUrl}{self.url_endpoint}"

            if self.request_type == "GET":

                r = requests.get(url=url, headers=self.request_header)

            else:
                r = requests.request(method="GET", url=url, params=self.request_param, headers=self.request_header)



            # error handling
            status = r.status_code
            if status >= 400 and status < 500:
                r.raise_for_status()

            self.response = r

            if return_df:
                df = pd.json_normalize(self.response.json()["data"])
                if "as_of_date" in df.columns:
                    df['as_of_date'] = [pd.to_datetime(x).strftime("%Y-%m-%d") for x in df['as_of_date']]
                if save_file and file_name:
                    output = os.path.join(CSV_OUTPUT, file_name)
                    df.to_csv(output)
                else:
                    return warnings.warn("please enter a filename")
                return df

            if save_file and file_name:
                if str(gis_data_type).lower() == 'gpkg':
                    self.save_file(response=self.response.content, output_path=GPK_OUTPUT, file_name=file_name)
                    return os.path.join(GPK_OUTPUT, file_name)

                elif str(gis_data_type).lower() == 'shp':
                    self.save_file(response=self.response.content, output_path=SHP_OUTPUT, file_name=file_name)
                    return os.path.join(SHP_OUTPUT, file_name)
                else:
                    return warnings.warn("please indicate the what type of GIS data that is, options are:\n1)\tGPKG\n2)\tSHP")

            return r.json()

        # error handling
        except requests.exceptions.HTTPError as errh:
            raise GussExceptions(message=errh.__str__())
        except requests.exceptions.ConnectionError as errc:
            raise GussExceptions(errc.__str__())
        except requests.exceptions.Timeout as errt:
            raise GussExceptions(errt.__str__())
        except requests.exceptions.RequestException as err:
            raise GussExceptions(err.__str__())

    def get_as_of_dates(self):

        # get as of Dates
        self.url_endpoint = '/api/public/map/listAsOfDates'
        aod_list = self.send_request(return_df=True, save_file=True, file_name="as_of_date.csv")
        return aod_list

    def get_download_reference(self, as_of_date=None):

        # set get method
        self.request_type = "GET"
        # get List of Availability Data for Downloads
        if as_of_date is None:
            as_of_date = '2024-06-30'

        self.url_endpoint = f'/api/public/map/downloads/listAvailabilityData/{as_of_date}'
        reference_df = self.send_request(return_df=True, save_file=True,
                                         file_name=f"download_reference_list_as_of_date_{as_of_date}.csv")
        return reference_df



