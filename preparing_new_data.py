import warnings
warnings.filterwarnings('ignore')

import pandas as pd

movies_df = pd.read_csv(r"path\movies_metadata.csv")
new_movies_df = movies_df[["id","title","release_date"]]

# solving the problem of other data formats and None. We lost almost 50 rows which is negligible. And after that we transformed the column of year of release to datetime

from datetime import datetime

def removing_the_other_format(x):
    try:
        s = datetime.strptime(x, '%Y-%m-%d')
        return True
    except:
        return False


new_movies_df["format"] = new_movies_df["release_date"].apply(removing_the_other_format)
new_movies_df = new_movies_df.loc[new_movies_df["format"]]
new_movies_df.drop('format', axis=1, inplace=True)
new_movies_df["release_date"] = pd.to_datetime(new_movies_df["release_date"], format="%Y-%m-%d")

new_movies_df.to_csv("movies_table.csv", index=False)

ratings_df = pd.read_csv(r"path\ratings.csv")

ratings_df["timestamp"] = pd.to_datetime(ratings_df['timestamp'], unit='s')
ratings_df

ratings_df.to_csv("ratings_df.csv", index=False)
