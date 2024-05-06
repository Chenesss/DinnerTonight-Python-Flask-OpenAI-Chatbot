import urllib.parse
import requests


url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=5"

def get_yelp_businesses(location_string, category_string, radius=10, limit=5):
    base_url = f"https://api.yelp.com/v3/businesses/search?location={urllib.parse.quote(location_string)}&categories={urllib.parse.quote_plus(category_string)}&sort_by=best_match&radis={radius}&limit={limit}"
    # base_url = "https://api.yelp.com/v3/businesses/search?location=sydney&sort_by=best_match&limit=20"

    print(base_url)
    headers = {"accept": "application/json",
               "Authorization" : "<YOUR BEARER TOKEN>"}

    response = requests.get(base_url, headers=headers)
    return response.json()

# recommendations = get_yelp_businesses(location_string="San Francisco", category_string="chinese").json()

# print(recommendations)

# for business in recommendations['businesses']:
#     print(business)
#     print('\n')