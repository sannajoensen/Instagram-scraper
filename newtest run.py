# Imports
import pandas as pd
import urllib.request
from collections import Counter

from newtest import recent_post_links, insta_link_details, insta_url_to_img


example_username_urls = recent_post_links('lilmiquela', post_count=30)
print(example_username_urls)
example_username_details = [insta_link_details(url) for url in example_username_urls]
example_username = pd.DataFrame(example_username_details)
example_username.head()
csv = example_username.to_csv('/Users/Sanna/Desktop/Python/Instagram Scraper/example_username.csv')
print(csv)

# Koden er fundet på: 
# jnawjux, 2020. Found on: https://github.com/jnawjux/web_scraping_corgis?fbclid=IwAR0AUgc_J5is-CtG2Pk7DWaqfix36paSxhgAewLxDm-69awxGV3cGZ82zUs [Sidst besøgt: 20.12.2020].
# Python Simplified, 2020: https://www.youtube.com/watch?v=iJGvYBH9mcY [Sidst besøgt: 20.12.2020].
