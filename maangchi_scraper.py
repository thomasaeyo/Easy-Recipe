from BeautifulSoup import BeautifulSoup
import requests
import pandas as pd
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

FOOD_TYPES = open('food_types.txt').readlines()
BASE_URL = 'http://www.maangchi.com/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}

def main():
	fetch_recipe_urls()

def fetch_recipe_urls():
	df = pd.DataFrame(columns=['english_name', 'korean_name' ,'type', 'url'])
	for food_type in FOOD_TYPES:
		df = df.append(get_recipe_names_by_food_type(food_type.split('\n')[0]))
	
	df.to_csv('maangchi_foods.csv', sep='\t', encoding='utf-8')
	return df

def get_recipe_names_by_food_type(food_type):	
	url = BASE_URL + ('recipes/%s' % food_type)
	response = requests.get(url, headers=HEADERS)

	soup = BeautifulSoup(response.text)
	recipes = soup.findAll(id=re.compile('^post-'))
	recipe_urls = []
	recipe_english_names = []
	recipe_korean_names = []
	for i in xrange(len(recipes)):
		recipe_urls.append(recipes[i].a['href'])
		recipe_english_names.append(recipes[i].a['title'])
		recipe_korean_names.append(str(recipes[i].p).split('<br />\n')[1][:-4])
	types = [food_type] * len(recipe_urls)
	return pd.DataFrame({'english_name':recipe_english_names, 'korean_name':recipe_korean_names, 'type':types, 'url':recipe_urls})


if __name__ == "__main__":
	main()