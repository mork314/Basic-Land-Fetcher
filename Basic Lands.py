'''
Check scryfall for every card under full art basic lands excluding online promos.
Export all image urls
take those urls and check if any of them are in the spreasheet
Any that aren't in the URL collection go to spreadsheet, added at bottom
Profit?
https://api.scryfall.com/cards/search?q=type:basic+type:land+is:fullart+-is:digital+unique:prints&format=csv


'''
import pandas as pd
import numpy as np
import requests as req
import json
import gspread
gc = gspread.service_account()
sheet = gc.open("Full Art Basics (With Python!)")
worksheet = sheet.get_worksheet(0)
df = pd.read_json("https://api.scryfall.com/cards/search?q=type:basic+type:land+is:fullart+-is:digital+unique:prints&")
#print(df[['data']].to_string(index=False)) 
url_list = worksheet.col_values(1)
link_list = worksheet.col_values(2)
url_list.pop(0)
link_list.pop(0)
def add_urls(api_url, number_results):
    df = pd.read_json(api_url)
    for i in range(number_results):
        row_i_data = df['data'].iloc[i]
        url_i = row_i_data['image_uris']['normal']
        if url_i in url_list:
            None
        else:
            url_list.append(url_i)
def add_links(api_url, number_results):
    df = pd.read_json(api_url)
    for i in range(number_results):
        row_i_data = df['data'].iloc[i]
        link_i = row_i_data['scryfall_uri']
        if link_i in link_list:
            None
        else:
            link_list.append(link_i)
add_urls('https://api.scryfall.com/cards/search?q=type:basic+type:land+is:fullart+-is:digital+unique:prints&', 175)
add_links('https://api.scryfall.com/cards/search?q=type:basic+type:land+is:fullart+-is:digital+unique:prints&', 175)
more_pages = df['has_more'].iloc[0]
print(more_pages)
while more_pages == True:
    new_url = df['next_page'].iloc[0]
    print(new_url)
    number_results = int(pd.read_json(new_url)['total_cards'].iloc[0]) - 175
    add_urls(new_url, number_results)
    add_links(new_url, number_results)
    more_pages = pd.read_json(new_url)['has_more'].iloc[0]
df_2 = pd.DataFrame({'Image URL':url_list, 'Scryfall Link':link_list})
worksheet.update(([df_2.columns.values.tolist()]) + df_2.values.tolist())
