from bin.download_mb_coverage import download_provider_state_coverage_data
from bin.download_fixed_coverage import download_location_fixed_coverage_by_state
from bin.download_challenge_data import download_challenge_data


from guss.gussErrors import GussExceptions

### how to use Guss to download bdc data

# reference df is

"""

:param run: bool, True if you want to run the function, False for dry run

:param as_of_date: string, as_of_date (date format ‘YYYY-MM-DD’) - required

:param provider_id_list: list, list of unique identifier for the service provider. if all Fips code is desired, then option of 
                        ["ALL"] is advised.

:param state_fips_list: list, a list of 2-digit FIPS code for the selected state / territory from the current U.S. Census
                        Bureau data, please include leading zero. if all Fips code is desired, then option of 
                        ["ALL"] is advised.
                        
:param technology_list: list, a list of code for the technology with which the provider reports to provide service {300:3G, 400: LTE, 500: 5G-NR}

:param technology_type: Type of technology ('Mobile Broadband', 'Mobile Voice')
:param subcategory: string, valid options: 'Hexagon Coverage', 'Raw Coverage'
:param FiveG_speed_tier_list: "35/3", "7/1"
:param gis_type: valid options: "SHP", "GPKG"


Example of Top 4 nationwide provider id = {"ATT": 130077,
            "T-Mobile":130403, "Verizon": 131425, "US Cellular": 131310}


"""

if __name__ == '__main__':

    try:

        # hexagon coverage shp
        output_raw_coverage_path_list = download_provider_state_coverage_data(run=True, as_of_date="2024-06-30",
                                                                              provider_id_list=['all'],
                                                                              state_fips_list=["11"],
                                                                              technology_list=[400, 300, 500],
                                                                              technology_type="Mobile Broadband",
                                                                              subcategory='Hexagon Coverage',
                                                                              fiveG_speed_tier_list=['7/1', '35/3'],
                                                                              gis_type="shp")

        # raw coverage gpkg
        output_hexagon_coverage_path_list = download_provider_state_coverage_data(run=True, as_of_date="2024-06-30",
                                                                                  provider_id_list=['130077', '130403',
                                                                                                    '131425', '131310'],
                                                                                  state_fips_list=["11"],
                                                                                  technology_list=[400, 300, 500],
                                                                                  technology_type="Mobile Broadband",
                                                                                  subcategory='Raw Coverage',
                                                                                  fiveG_speed_tier_list=['7/1', '35/3'],
                                                                                  gis_type="gpkg")

        # fixed coverage csv
        output_fixed_coverage_availiablity = download_location_fixed_coverage_by_state(run=True,
                                                                                      as_of_date='2024-06-30',
                                                                                      provider_id_list=['all'],
                                                                                      state_fips_list=['11'],
                                                                                      technology_list=[10,40,50,60,61,70,71,72,0]
                                                                                      )

        out_challenge_data = download_challenge_data(run=True,
                                                     as_of_date='2024-06-30',
                                                     category='Mobile Challenge - Resolved',
                                                     state_fips_list=["all"])



    except GussExceptions as e:
        print(f"error: {e}")
