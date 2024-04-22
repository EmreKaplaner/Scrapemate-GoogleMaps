#!/Users/emre/opt/anaconda3/envs/SP/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:03:07 2024

@author: emre
"""

import pandas as pd
import re
import googlemaps
gmaps = googlemaps.Client(key='YOUR-GOOGLEMAPS-API-KEY')


def get_best_reviews(df, gmaps):
    # Lists to collect rows
    cleansed_rows = []
    failed_fetches_rows = []

    for index, row in df.iterrows():
        reviews_link = str(row['reviews_link']) if pd.notnull(row['reviews_link']) else None
        if reviews_link:
            place_id_match = re.search(r'placeid=([^&]+)', reviews_link)
            if place_id_match:
                place_id = place_id_match.group(1)
                try:
                    place_details = gmaps.place(place_id=place_id)
                    reviews = place_details['result'].get('reviews', [])
                    five_star_reviews = [review['text'] for review in reviews if review.get('rating') == 5]
                    four_star_reviews = [review['text'] for review in reviews if review.get('rating') == 4]

                    best_review = ''
                    if five_star_reviews:
                        best_review = max(five_star_reviews, key=len)
                    elif four_star_reviews:
                        best_review = max(four_star_reviews, key=len)

                    if best_review:
                        # Add to the cleansed list if there's a best review
                        cleansed_rows.append({**row, 'Best_Review': best_review})
                    else:
                        # Add to the failed list if no suitable review is found
                        failed_fetches_rows.append(row)
                except googlemaps.exceptions.ApiError as e:
                    print(f"Error fetching reviews for link {reviews_link}: {e}")
                    failed_fetches_rows.append(row)
            else:
                failed_fetches_rows.append(row)
        else:
            failed_fetches_rows.append(row)

    # Convert lists to DataFrames
    final_cleansed = pd.DataFrame(cleansed_rows)
    failed_fetches = pd.DataFrame(failed_fetches_rows, columns=df.columns)

    return final_cleansed, failed_fetches



#gmaps = googlemaps.Client(key='AIzaSyAjgbniKi3bAiv6qdiB_vrrwgpqM2VtFXg')
#data_test = pd.read_csv("/Users/emre/Desktop/ESO_Softwares/google-maps-scraper-main/output_magi_paris/magi_paris_results.csv")
#test1 , test2 = get_best_reviews(data_test,gmaps)





