import unicodedata as ud
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

PATH2CHROMEDRIVER = '/Users/thomasaeyo/Desktop/Easy-Recipe/chromedriver'
UNITS = open('unit_of_measurements.txt').readlines()
FOOD_TYPES = open('food_types.txt').readlines()

BASE_URL = 'http://www.maangchi.com/'

def main():
	driver = init_driver()
	df = fetch_recipe_urls(driver)

	print df

def init_driver():
	driver = webdriver.Chrome(executable_path=PATH2CHROMEDRIVER)
	driver.wait = WebDriverWait(driver, 5)
	return driver

def fetch_recipe_urls(driver):
	df = pd.DataFrame(columns=['english_name', 'korean_name' ,'type'])
	english_names = []
	urls = []
	korean_names = []
	types = []
	for food_type in FOOD_TYPES:
		recipes = get_recipe_names_by_food_type(driver,food_type)
		unzipped = zip(*recipes)
		english_names.extend(unzipped[0])
		urls.extend(unzipped[1])
		korean_names.extend(unzipped[2])
		types.extend([food_type.split('\n')[0]]*len(recipes))

	df = pd.DataFrame({'english_name':english_names, 'korean_name':korean_names, 'type':types, 'url':urls})
	df.to_csv('maangchi_foods', sep='\t')
	return df



def get_recipe_names_by_food_type(driver,food_type):	
	url = BASE_URL + ('recipes/%s' % food_type)
	driver.get(url)
	recipe_urls_names = driver.find_elements_by_xpath("//div[starts-with(@id, 'post')]/a")
	recipe_korean_names = driver.find_elements_by_xpath("//div[starts-with(@id, 'post')]/p")
	recipes = []
	for i in xrange(len(recipe_urls_names)):
		recipes.append(
			(recipe_urls_names[i].get_attribute('title'), 
			 recipe_urls_names[i].get_attribute('href'), 
			 recipe_korean_names[i].text.split('\n')[1])
			)
	return recipes

if __name__ == "__main__":
	main()











# # later
# """
# 	3 types of Ingredients:
# 		- (number) (unit) (ingredient '(explanation)') '(- detail)'
# 			- number could be a mixed fraction
# 		- (number - number) (unit) (ingredient '(explanation)') '(- option)'
# 			- be careful with 'cups of water'
# 		- (ingredient '(explanation)') '(- option)'
# """

# # requires: list of WebElements
# # saves ingredients to the database
# def parseIngredients(ingredient_webelems):
# 	for ingredient_webelem in ingredient_webelems:
# 		temp = ingredient_webelem.text.split(' - ')
# 		ingredient = temp[0]

# def getUnit(s):
# 	for unit in unit_of_measurements:
# 		if ' {} '.format(unit) in s:
# 			return unit
# 	return ''

# # 1. number
# # 2. fraction
# # 3. number - number
# # returns: (lowerBound,upperBound)
# def getAmount(s):
# 	temp = s.split(' - ')
# 	if len(temp) == 1:
# 		return (parse_number(temp[0]), parse_number(temp[0]))
# 	else:
# 		return (parse_number(temp[0]), parse_number(temp[1]))

# def parse_number(n):
# 	temp = n.split('\\')
# 	if len(temp) != 1:
# 		return ud.numeric(temp[0]) + ud.numeric('\{}'.format(temp[1]))
# 	return ud.numeric(n)