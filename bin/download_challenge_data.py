import os
import ast
import warnings
import re
from guss import GUSS
from guss.gussErrors import GussExceptions


def download_challenge_data(run=False, as_of_date=None, category=None, state_fips_list: list = None):
    if run:

        credentials = ast.literal_eval(os.environ['credentials'])
        guss = GUSS.Guss(**credentials)

        if as_of_date is None:
            as_of_date = '2024-06-30'

        if category is None:
            guss.request_param = None
        else:
            category_params = {
                'category': category
            }

        reference_df = guss.list_challenge_data(as_of_date=as_of_date,
                                                params=category_params,
                                                file_name=f"challenge_data_as_of_{as_of_date}.csv")

        num_state = len(state_fips_list)

        if num_state > 1:

            state_list_query = [f"state_fips == '{x}'" for x in state_fips_list]

            if 'all' in [x.lower() for x in state_fips_list]:

                reference_df_filtered = reference_df
            else:
                state_query = ' or '.join(state_list_query)
                reference_df_filtered = reference_df.query(f"{state_query}")

        elif num_state == 1:
            state_query = ''
            if 'all' in [x.lower() for x in state_fips_list]:
                reference_df_filtered = reference_df
            else:

                state_query = f"state_fips == '{state_fips_list[0]}'"
                reference_df_filtered = reference_df.query(f"{state_query}")
        else:
            raise GussExceptions(message="No state fips list provided")

        if len(reference_df_filtered) == 0:
            raise GussExceptions("check your query params:\n"
                                 f"{reference_df_filtered}\n"
                                 "I got no query back. Try again")
        else:
            print(f"There are about {len(reference_df_filtered)} download files using the following query:{state_query}")

        output_path = []

        for i, row in reference_df_filtered.iterrows():
            print(row)

            file_id = row['file_id']
            file_name = f"{category.replace(' ', '_').replace('-', '_')}_{row['state_fips']}_{row['state_name']}.zip"

            saved_output = guss.download_file(data_type='challenge',
                                              file_id=file_id, file_name=file_name,
                                              gis_type=None)
            output_path.append(saved_output)

        return output_path
