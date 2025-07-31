import os
import ast
import warnings
import re
import pandas as pd
import geopandas as gpd
from guss import GUSS
from guss.gussErrors import GussExceptions
from guss.GUSS import GPK_OUTPUT, SHP_OUTPUT

def download_location_fixed_coverage_by_state(run=False, as_of_date: str = '2024-06-30',
                                              data_type: object = 'availability',
                                              provider_id_list: list = None,
                                              state_fips_list: list = None,
                                              technology_list: list = None,
                                              polygonize=False,
                                              gis_type='gpkg') -> list:
    if data_type == 'availability':
        pass
    else:
        raise GussExceptions(message="Please make sure that the data_type should be:\n"
                                     "\t 1) availability (default value)")

    if run:

        credentials = ast.literal_eval(os.environ['credentials'])
        guss = GUSS.Guss(**credentials)

        category = 'Provider'
        subcategory = guss.category_subcategory[category][1]
        technology_type = guss.technology_type[1]

        reference_df = guss.get_download_reference(as_of_date=as_of_date)

        if reference_df.empty:
            raise GussExceptions(message="please check your as of date, no reference found")

        reference_df_filtered = reference_df[

            (reference_df['category'] == f'{category}')
            & (reference_df['subcategory'] == f"{subcategory}")
            & (reference_df['technology_type'] == f"{technology_type}")
            & (reference_df["file_type"] == 'csv')

            ]
        if reference_df_filtered.empty:
            raise GussExceptions(
                message="No reference after filtering. Check your category or subcategory or technology_type,"
                        " or file_type query parameters")

        num_state = len(state_fips_list)
        num_technology = len(technology_list)
        num_provider = len(provider_id_list)

        if num_state > 1:
            state_list_query = [f"state_fips == '{x}'" for x in state_fips_list]
            state_query = ' or '.join(state_list_query)
            filter_df = reference_df_filtered.query(f"{state_query}")
        elif num_state == 1:
            if 'all' in [x.lower() for x in state_fips_list]:
                filter_df = reference_df_filtered
            else:
                state_query = f"state_fips == '{state_fips_list[0]}'"
                filter_df = reference_df_filtered.query(f"{state_query}")
        else:
            raise GussExceptions(message="No state fips list provided")

        if num_technology > 1:

            technology_list = [f"{x}" for x in technology_list]

            if 'all' in [str(x).lower() for x in technology_list]:
                raise GussExceptions(message="check technology code list, 'all' should not be provided with other code "
                                             "techs")

            technology_query = "|".join(technology_list)

            technology_query = fr"\b(?:{technology_query})\b"

            filter_df = filter_df[
                filter_df['technology_code'].str.contains(technology_query, flags=re.IGNORECASE, regex=True)]

        elif num_technology == 1:
            if 'all' in [str(x).lower() for x in technology_list]:
                filter_df = reference_df_filtered
            else:
                technology_query = f"{technology_list[0]}"
                filter_df = filter_df[filter_df['technology_code'].str.contains(technology_query)]
        else:
            raise GussExceptions(message="No technology id list provided")

        if num_provider > 1:
            provider_id_list_query = [f"provider_id == '{x}'" for x in provider_id_list]
            provider_id_query = ' or '.join(provider_id_list_query)
            filter_df = filter_df.query(provider_id_query)

        elif num_provider == 1:
            if 'all' in provider_id_list:
                filter_df = filter_df
            else:
                provider_id_query = f"provider_id == '{provider_id_list[0]}'"
                filter_df = filter_df.query(provider_id_query)
        else:
            raise GussExceptions(message="No provider id list provided")

        filter_df = filter_df.sort_values(
            by=['provider_id', 'state_fips', "technology_code", 'speed_tier'])

        print(f"There are total of {len(filter_df)} number of files.")



        output_path_list = []
        for i, row in filter_df.iterrows():
            print(row['file_name'])

            file_id = row['file_id']
            file_name = f"{technology_type.replace(' ', '')}_{subcategory.replace(' ', '')}_{row['file_name']}.zip"

            saved_output = guss.download_file(data_type=data_type, file_id=file_id, file_name=file_name, gis_type=None)

            if polygonize:
                df = pd.read_csv(saved_output, compression='zip')
                df['geometry'] = df['h3_res8_id'].apply(guss.polygonize)

                gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=4326)
                if gis_type == 'gpkg':
                    output_path = os.path.join(GPK_OUTPUT, file_name.replace('.zip', '.gpkg'))
                    layer_name = file_name.replace('.zip', '.gpkg')
                    gdf.to_file(output_path, layer=layer_name)
                    print(f"GeoPackage saved to {output_path}")

                elif gis_type == 'shp':
                    output_path = os.path.join(SHP_OUTPUT, file_name.replace('.zip', '.shp'))
                    gdf.to_file(output_path)
                    print(f"shp saved to {output_path}")
                else:
                    raise GussExceptions(message="Oh no, gis_type was not provided, please indicate gis_type = 'shp' "
                                                 "or 'gpkg'")

            output_path_list.append(saved_output)


        return output_path_list
