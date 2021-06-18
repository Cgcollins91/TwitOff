import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

base_path = '/Users/chriscollins/Documents/lambda/Build_Week_1/AirBnB/'
pickle_path = base_path + 'AirBnB.pkl'


def load_data(how):
    if how == 'fresh':
        nc_path = base_path + 'asheville_nc_listings.csv'
        austin_path = base_path + 'austin_tx_listings.csv'
        broward_path = base_path + 'broward_fl_listings.csv'
        cambridge_path = base_path + 'cambridge_ma_listings.csv'
        chicago_path = base_path + 'chicago_il_listings.csv'
        columbus_path = base_path + 'columbus_oh_listings.csv'

        nc_df = pd.read_csv(nc_path)
        austin_df = pd.read_csv(austin_path)
        cambridge_df = pd.read_csv(cambridge_path)
        broward_df = pd.read_csv(broward_path)
        chicago_df = pd.read_csv(chicago_path)
        columbus_df = pd.read_csv(columbus_path)

        df = pd.concat([nc_df, austin_df, cambridge_df, broward_df, chicago_df, columbus_df])

        drop_cols = ['host_picture_url', 'host_thumbnail_url', 'listing_url', 'picture_url', 'host_has_profile_pic']

        df = air_bnb_df.drop(columns=drop_cols)
        df.to_pickle(pickle_path)
        print("Saved Pickle Successfully")
        print(air_bnb_df.head())
        print(air_bnb_df.columns)

    else:
        df = pd.read_pickle(pickle_path)
        print(air_bnb_df.head())

    return df

# air_bnb_df = load_data("fresh")


air_bnb_df = load_data("from pickle")


