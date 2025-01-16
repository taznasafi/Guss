import requests
import pandas as pd
import warnings
import json
import os
import ast
from guss.gussErrors import GussExceptions
from guss.GEO_CENSEY import Fipsy

from . import DATA_INPUT, DATA_OUTPUT, CSV_OUTPUT, GPK_OUTPUT, SHP_OUTPUT


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
        self.category = {1: 'Summary', 2: "State", 3: "Provider"}
        self.subcategory = {1: "summary by Geography Type - CensusPlace",
                            2: "Summary by Geography Type - Other Geographies",
                            3: "Summary by Geography Type - Census Place",
                            4: "Provider Summary by Geography Type",
                            5: "Provider Summary",
                            6: "Provider List",
                            7: "Location Coverage",
                            8: "Hexagon Coverage",
                            9: "Location Coverage",
                            10: "Hexagon Coverage",
                            11: "Raw Coverage",
                            12: "Supporting Data"
                            }
        self.technology_type = {1: 'Fixed Broadband',
                                2: 'Mobile Broadband',
                                3: 'Mobile Voice'
                                }
        self.FiveG_speed_teir = ["35/3", "7/1"]





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

    def api_request(self):
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

            return r

        # error handling
        except requests.exceptions.HTTPError as errh:
            raise GussExceptions(message=errh.__str__())
        except requests.exceptions.ConnectionError as errc:
            raise GussExceptions(errc.__str__())
        except requests.exceptions.Timeout as errt:
            raise GussExceptions(errt.__str__())
        except requests.exceptions.RequestException as err:
            raise GussExceptions(err.__str__())

    def get_request(self, return_df=None, gis_data_type=None, save_file=False, file_name=None):

        try:

            self.response = self.api_request()

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
            else:
                if save_file and file_name:
                    output = os.path.join(CSV_OUTPUT, file_name)
                    self.save_file(self.response.content, output_path=CSV_OUTPUT, file_name=file_name)
                    return output

            if save_file and file_name:
                if str(gis_data_type).lower() == 'gpkg':
                    self.save_file(response=self.response.content, output_path=GPK_OUTPUT, file_name=file_name)
                    return os.path.join(GPK_OUTPUT, file_name)

                elif str(gis_data_type).lower() == 'shp':
                    self.save_file(response=self.response.content, output_path=SHP_OUTPUT, file_name=file_name)
                    return os.path.join(SHP_OUTPUT, file_name)
                else:
                    return warnings.warn(
                        "please indicate the what type of GIS data that is, options are:\n1)\tGPKG\n2)\tSHP")

            return self.response.json()

        # error handling

        except GussExceptions as e:
            raise GussExceptions(f"error: {e}")

    def get_as_of_dates(self):

        # get as of Dates
        self.url_endpoint = '/api/public/map/listAsOfDates'
        aod_list = self.get_request(return_df=True, save_file=True, file_name="as_of_date.csv")
        return aod_list

    def get_download_reference(self, as_of_date=None):

        # set get method
        self.request_type = "GET"
        # get List of Availability Data for Downloads
        if as_of_date is None:
            as_of_date = '2024-06-30'

        self.url_endpoint = f'/api/public/map/downloads/listAvailabilityData/{as_of_date}'
        reference_df = self.get_request(return_df=True, save_file=True,
                                        file_name=f"download_reference_list_as_of_date_{as_of_date}.csv")
        return reference_df

    def download_file(self, data_type, file_id, file_name, gis_type):

        if str(data_type).lower() == "availability":
            pass
        elif str(data_type).lower() == 'challenge':
            pass
        else:
            raise GussExceptions(f"data_type: {data_type}-- it should be either : availability or challenge")

        file_type = ""
        if gis_type is not None:
            if gis_type.lower() == "shp":
                file_type = '1'
                self.url_endpoint = f"/api/public/map/downloads/downloadFile/{data_type}/{file_id}/{file_type}"
            elif gis_type.lower() == 'gpkg':
                file_type = '2'
                self.url_endpoint = f"/api/public/map/downloads/downloadFile/{data_type}/{file_id}/{file_type}"
        else:
            self.url_endpoint = f"/api/public/map/downloads/downloadFile/{data_type}/{file_id}"


        saved_output = self.get_request(save_file=True, return_df=False, file_name=file_name, gis_data_type=gis_type)

        return saved_output
