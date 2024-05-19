import pandas as pd

movie_data = pd.read_excel("movie_titles.xlsx", header=None)
movie_data.rename(columns={0: 'index', 1: "Year", 2: 'title'}, inplace=True)
movie_data.drop([3, 4, 5], axis=1, inplace=True)
movie_id_title = movie_data.set_index('index')['title'].to_dict()
movie_id_year = movie_data.set_index('index')['Year'].to_dict()

# Load Dataset
files=['combined_data_1.txt','combined_data_2.txt','combined_data_3.txt','combined_data_4.txt']
# create an csv file
data =open('data.csv',mode='w')
data.write(','.join(['Movie_id','User id','rating,Date']))
data.write('\n')
for i in files:
    with open(i) as f:
        for line in f:
            line=line.strip()
            if(line.endswith(':')):
                movie_id=line.replace(':','')
            else:
                row=[x for x in line.split(',')]
                row.insert(0,movie_id)
                data.write(','.join(row))
                data.write('\n')
data.close()

df=pd.read_csv('data.csv')

# Sort by User_id and rating (descending order to get highest ratings first)
df = df.sort_values(by=['User id', 'rating'], ascending=[True, False])

# Group by User_id and retain only the first 5 rows for each user
df = df.groupby('User id').head(5)

def format_movie_info(row):
    movie_id = row['Movie_id']
    title = movie_id_title[movie_id]  # Assuming movie_id_title(movie_id) returns the title for a given movie ID
    year = movie_id_year[movie_id]    # Assuming movie_id_year(movie_id) returns the year for a given movie ID
    return f"\"[{movie_id}] {title} ({int(year)})\""

df['formatted_info'] = df.apply(format_movie_info, axis=1)
result = df.groupby('User id')['formatted_info'].agg(list).reset_index()

result.to_excel("users_top_5_movies.xlsx", index=False)
