import os
import ast
import warnings
import re
from guss import GUSS
from guss.gussErrors import GussExceptions


def download_provider_state_coverage_data(run: bool = True,
                                          as_of_date: str = "2024-06-30", provider_id_list: list = None,
                                          state_fips_list: list = None, technology_list: list = None,
                                          technology_type: str = None, subcategory: str = None,
                                          fiveG_speed_tier_list: list = None, data_type: str = 'availability',
                                          gis_type: str = None) -> list:
    """

    :param run: bool, True if you want to run the function, False to dry run

    :param as_of_date: string, as_of_date (date format ‘YYYY-MM-DD’) - required

    :param provider_id_list: list, list of unique identifier for the service provider

    :param state_fips_list: list, a list of 2-digit FIPS code for the selected state / territory from the current U.S. Census
                            Bureau data (leading zero included)
    :param technology_list: list, a list of code for the technology with which the provider reports to provide service {300:3G, 400: LTE, 500: 5G-NR}

    :param technology_type: Type of technology (Mobile Broadband, Mobile Voice)
    :param subcategory: string, valid options: Hexagon Coverage, Raw Coverage
    :param fiveG_speed_tier_list:
    :param data_type: "35/3", "7/1"
    :param gis_type: valid options "SHP", "GPKG"
    :return: list of downloaded coverage paths.
    """

    if technology_type == 'Mobile Broadband' or technology_type == 'Mobile Voice':
        pass
    else:
        raise GussExceptions(message="Please make sure that the technology code should be:\n"
                                     "\t 1) Mobile Broadband\n\t2) Mobile Voice")

    if subcategory == "Raw Coverage" or subcategory == "Hexagon Coverage":
        pass
    else:
        raise GussExceptions(message="Please make sure that the sub category should be:\n"
                                     "\t 1) Raw Coverage\n\t2) Hexagon Coverage")

    if data_type == 'availability':
        pass
    else:
        raise GussExceptions(message="Please make sure that the data_type should be:\n"
                                     "\t 1) availability (default value)")





    if run:

        credentials = ast.literal_eval(os.environ['credentials'])
        guss = GUSS.Guss(**credentials)


        reference_df = guss.get_download_reference(as_of_date=as_of_date)

        if reference_df.empty:
            raise GussExceptions(message="Error: Check your query parameters")

        reference_df_filtered = reference_df[

            (reference_df['category'] == 'Provider')
            & (reference_df['subcategory'] == f"{subcategory}")
            & (reference_df['technology_type'] == f"{technology_type}")
            & (reference_df["file_type"] == 'gis')

            ]

        if reference_df_filtered.empty:
            raise GussExceptions(message="Error: Check your category or subcategory or technology_type,"
                                         " or file_type query parameters")

        num_provider = len(provider_id_list)
        num_state = len(state_fips_list)
        num_technology = len(technology_list)
        num_speed_tier = len(fiveG_speed_tier_list)

        provider_id_query = ''
        state_query = ''
        technology_query = ''
        speed_tier_query = ''

        if num_provider > 1:
            provider_id_list_query = [f"provider_id == '{x}'" for x in provider_id_list]
            provider_id_query = ' or '.join(provider_id_list_query)
        elif num_provider == 1:
            provider_id_query = f"provider_id == '{provider_id_list[0]}'"
        else:
            raise GussExceptions(message="No provider id list provided")

        if num_state > 1:
            state_list_query = [f"state_fips == '{x}'" for x in state_fips_list]
            state_query = ' or '.join(state_list_query)
        elif num_state == 1:
            state_query = f"state_fips == '{state_fips_list[0]}'"
        else:
            raise GussExceptions(message="No state fips list provided")

        if num_technology > 1:
            technology_list_query = [f"technology_code == '{str(x)}'" for x in technology_list]
            technology_query = ' or '.join(technology_list_query)
        elif num_technology == 1:
            technology_query = f"technology_code == '{technology_list[0]}'"
        else:
            raise GussExceptions(message="No technology id list provided")

        if num_speed_tier > 1:
            if ((400 in technology_list) or (300 in technology_list)) and not (500 in technology_list):
                speed_tier_list_query = [f"speed_tier.isna()" for x in technology_list]
            elif ((400 in technology_list) or (300 in technology_list)) and (500 in technology_list):
                speed_tier_lower_tech = [f"speed_tier.isna()" for x in [400]]
                speed_tier_5G_tech = [f"speed_tier == '{str(x)}'" for x in fiveG_speed_tier_list]
                speed_tier_list_query = speed_tier_lower_tech+speed_tier_5G_tech

            else:
                speed_tier_list_query = [f"speed_tier == '{str(x)}'" for x in fiveG_speed_tier_list]

            speed_tier_query = ' or '.join(speed_tier_list_query)
        elif num_speed_tier == 1:
            if (400 in technology_list) or (300 in technology_list):
                fiveG_speed_tier_list.append("speed_tier.isnull()")
            speed_tier_query = f"speed_tier == '{technology_list[0]}'"
        else:
            raise GussExceptions(message="No speed tier list provided")

        if ('all' in [x.lower() for x in state_fips_list]) and ('all' in [x.lower() for x in provider_id_list]):
            query_string = f"({technology_query}) and ({speed_tier_query})"
        elif 'all' in [x.lower() for x in state_fips_list]:
            query_string = f"({provider_id_query}) and ({technology_query}) and ({speed_tier_query})"
        elif 'all' in [x.lower() for x in provider_id_list]:
            query_string = f"({state_query}) and ({technology_query}) and ({speed_tier_query})"

        else:
            query_string = f"({provider_id_query}) and ({state_query}) and ({technology_query}) and ({speed_tier_query})"

        filter_df = reference_df_filtered.query(f"{query_string}").sort_values(by=['provider_id', 'state_fips', "technology_code", 'speed_tier'])


        if len(filter_df)==0:
            raise GussExceptions("check your query params:\n"
                                 f"{query_string}\n"
                                 "I got no query back. Try again")
        else:
            print(f"There are about {len(filter_df)} download files using the following query:"
                  f"\nt\{query_string}")


        output_path = []
        for i, row in filter_df.iterrows():
            print(row)

            file_id = row['file_id']
            file_name = f"{technology_type.replace(' ', '')}_{subcategory.replace(' ', '')}_{row['file_name']}.zip"

            saved_output = guss.download_file(data_type=data_type, file_id=file_id, file_name=file_name, gis_type=gis_type)
            output_path.append(saved_output)

        return output_path


