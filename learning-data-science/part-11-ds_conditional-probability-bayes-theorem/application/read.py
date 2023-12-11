"""
    m.fauzanalyafie@gmail.com
    23-Agustus-2022 18:21 PM
"""

import pandas as pd #type: ignore

class ReadData:
    
    def movierating(self):
        
        user_id = [42, 707, 454, 943, 199, 846, 406, 394, 306, 312]
        user_id = pd.DataFrame(user_id, columns = ['user_id'])

        movie_id = [281, 347, 197, 23, 539, 187, 132, 742, 1009, 8]
        movie_id = pd.DataFrame(movie_id, columns = ['movie_id'])

        title = ['River Wild, The', 'Wag the Dog', 'Graduate, The',
        'Taxi Driver', 'Mouse Hunt', 'Wizard of Oz, The', 'Godfather: Part II, The',
        'Ransom', 'Stealing Beauty', 'Babe']
        title = pd.DataFrame(title, columns = ['title'])

        year = ['1994', '1997', '1967', '1976', '1997', '1974', '1939', 
        '1996', '1996', '1995']
        year = pd.DataFrame(year, columns = ['year'])

        rating = [3, 5, 4, 4, 1, 4, 5, 5, 4, 5]
        rating = pd.DataFrame(rating, columns = ['rating'])

        df_movie = pd.concat(objs = [user_id, movie_id, title, year, rating], axis = 1, ignore_index = False)

        return df_movie
        