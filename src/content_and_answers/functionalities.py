import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from src.sudoku.sudoku_generator import *

options = Options()
options.headless = True
driver = webdriver.Chrome("/Users/oscarmeurer/Documents2022/chromedriver", options=options)
list_city = ["paris", "lyon", "nice", "lille", "marseille"] #some big cities are exceptions


def get_meteo(city):

    """Returns the weather in french for a city """
    url = 'https://meteofrance.com/'
    driver.get(url)
    try:
        search_localisation = driver.find_element(By.CSS_SELECTOR, '#search_form_input')  # Find the search field
        search_localisation.send_keys(city)  # Enter the city in the search bar
        search_click = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        search_click.click()  # Click on search
        if city.lower() in list_city:
            search_click_second_element = driver.find_element(By.CSS_SELECTOR,
                                                              '[id*="search_result_poi_"]:nth-child(2)')
            search_click_second_element.click()  # Click on the first item in the result list
        else:
            search_click_first_element = driver.find_element(By.CSS_SELECTOR, '[id*="search_result_poi_"]')
            search_click_first_element.click()  # Click on the second item in the result list
        # scrap the city infos from the result page
        page_h1_text = driver.find_element(By.CSS_SELECTOR, '#title-block h1').text
        city_name = re.search('METEO\s([a-zA-Z\s\-]+).+', page_h1_text).group(1)
        city_temperature = driver.find_element(By.CSS_SELECTOR, '.today .weather_temp').text
        city_weather = driver.find_element(By.CSS_SELECTOR, '.today .weather_temp img').get_attribute('title')

        # Returns the temperature and the weather in the city specified by the user
        result = f'La température à {city_name.capitalize()} est de {city_temperature} avec un ciel {city_weather.lower()}.'

    except:
        result = 'Aucun résultat pour votre recherche.'

    return result


def get_horoscope(astrological_sign):
    """ Returns the daily horoscope for the astrological sign specified by the user"""

    url = f'https://www.vogue.fr/astro/horoscope/horoscope-du-jour/{astrological_sign}/aujourd-hui'
    driver.get(url)
    no_result = driver.find_element(By.CSS_SELECTOR, '.row .sections-default-text').text

    if str(no_result) == "La page que vous recherchez n'a pas été trouvée." :
        result = "Ce signe astrologique n'existe pas. Aucun résultat pour votre recherche."
    else :
        result = driver.find_element(By.CSS_SELECTOR, '.row .sections-default-text').text

    return result


def get_joke():
    """Returns a joke"""

    url = 'https://www.jimmy-lelievre.com/blague.html'
    driver.get(url)
    time.sleep(1)
    try: #tries to get the header and the content
        try:  # to get the header
            header_content = driver.find_element(By.XPATH, '//*[@id="header"]').get_attribute('innerHTML')
            header = header_content.replace("&nbsp;", "")
        except:
            print("no header")

        try:  # to get the content
            content = driver.find_element(By.XPATH, '//*[@id="content"]').get_attribute('innerHTML')
            solution = content.replace("&nbsp;", "")
        except:
            print('')
    except:
        pass

    return header + "\n" + solution


def get_definition(word_to_define):
    """Returns a definition for a specific word"""

    url = f"https://dictionnaire.lerobert.com/definition/{word_to_define}"
    driver.get(url)
    no_result = driver.find_element(By.CSS_SELECTOR, '.ws-c .def span').text

    # Fill in the definition
    if str(no_result) == 'Nous n’avons pas encore de résultat à vous proposer pour ce mot.':
        result = no_result
    else:
        type_word_defined = driver.find_element(By.CSS_SELECTOR, '.d_cat').text
        definition_word_defined = driver.find_element(By.CSS_SELECTOR, '.d_ptma').text
        result = f"""La définition du mot {word_to_define} d'après le dictionnaire Robert est :
        Genre : {type_word_defined}
        {definition_word_defined}"""
        # Grammatical class of the word

    return result

def launch_sudoku(input):

    with open(f'src/sudoku/{input}.sudoku','r') as boards_file:
        game = SudokuGame(boards_file)
        return game


