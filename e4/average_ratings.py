import pandas as pd
import difflib
import sys

movieRatings = pd.read_csv(sys.argv[2])

def getRating(movie_title):
    arr = movieRatings.loc[movieRatings['title'] == movie_title]['rating'].values
    if len(arr)< 1:
        return 0
    return arr[0]

def main():
    movie_listdf = pd.read_table(sys.argv[1])
    movie_list = movie_listdf['13th'].shift(1)
    movie_list.iloc[0] = '13th'
    mvf = movie_list.apply(lambda x: difflib.get_close_matches(x, movieRatings['title']))
    mvfs = mvf.apply(lambda x: pd.Series(x))
    tmpRatings = mvfs.applymap(getRating)
    avgRatings = tmpRatings.mean(axis=1).round(2)
    output = pd.DataFrame({'title' : movie_list, 'ratings' : avgRatings})
    output = output[['title', 'ratings']]
    output.to_csv('output.csv')

if __name__ == '__main__':
    main()
