import pandas as pd


class Fipsy:
    def __init__(self):
        self.state_fips_dict = {'fips':
                                    {0: 1, 1: 2, 2: 4, 3: 5, 4: 6, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 13, 11: 15,
                                     12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21, 18: 22, 19: 23, 20: 24, 21: 25,
                                     22: 26, 23: 27, 24: 28, 25: 29, 26: 30, 27: 31, 28: 32, 29: 33, 30: 34, 31: 35,
                                     32: 36, 33: 37, 34: 38, 35: 39, 36: 40, 37: 41, 38: 42, 39: 44, 40: 45, 41: 46,
                                     42: 47, 43: 48, 44: 49, 45: 50, 46: 51, 47: 53, 48: 54, 49: 55, 50: 56, 51: 60,
                                     52: 64, 53: 66, 54: 68, 55: 69, 56: 70, 57: 72, 58: 72, 59: 78},
                                'name': {0: 'ALABAMA', 1: 'ALASKA', 2: 'ARIZONA', 3: 'ARKANSAS', 4: 'CALIFORNIA',
                                         5: 'COLORADO', 6: 'CONNECTICUT', 7: 'DELAWARE', 8: 'DISTRICT OF COLUMBIA',
                                         9: 'FLORIDA', 10: 'GEORGIA', 11: 'HAWAII', 12: 'IDAHO', 13: 'ILLINOIS',
                                         14: 'INDIANA', 15: 'IOWA', 16: 'KANSAS', 17: 'KENTUCKY', 18: 'LOUISIANA',
                                         19: 'MAINE', 20: 'MARYLAND', 21: 'MASSACHUSETTS', 22: 'MICHIGAN',
                                         23: 'MINNESOTA', 24: 'MISSISSIPPI', 25: 'MISSOURI', 26: 'MONTANA',
                                         27: 'NEBRASKA', 28: 'NEVADA', 29: 'NEW HAMPSHIRE', 30: 'NEW JERSEY',
                                         31: 'NEW MEXICO', 32: 'NEW YORK', 33: 'NORTH CAROLINA', 34: 'NORTH DAKOTA',
                                         35: 'OHIO', 36: 'OKLAHOMA', 37: 'OREGON', 38: 'PENNSYLVANIA',
                                         39: 'RHODE ISLAND', 40: 'SOUTH CAROLINA', 41: 'SOUTH DAKOTA', 42: 'TENNESSEE',
                                         43: 'TEXAS', 44: 'UTAH', 45: 'VERMONT', 46: 'VIRGINIA', 47: 'WASHINGTON',
                                         48: 'WEST VIRGINIA', 49: 'WISCONSIN', 50: 'WYOMING', 51: 'American Samoa',
                                         52: 'Federated States of Micronesia', 53: 'Guam', 54: 'Marshall Islands',
                                         55: 'Commonwealth of the Northern Mariana Islands', 56: 'Palau',
                                         57: 'Puerto Rico', 58: 'U.S. Minor Outlying Islands',
                                         59: 'U.S. Virgin Islands'}}

        self.state_df = self.make_fips_df()



    def make_fips_df(self):
        df = pd.DataFrame.from_dict(self.state_fips_dict)
        df['fips'] = [str(x).zfill(2) for x in df['fips']]
        return df


    def get_fip_list(self):
        return self.state_df['fips'].to_list()