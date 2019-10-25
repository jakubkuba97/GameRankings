
"""
    Search the metacritic site for all games
"""

from selenium import webdriver
import pandas as pd


class WebWorks:
    def __init__(self, start_page_url: str = '') -> None:
        from os import path
        import sys
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.debug = False
        self.columns = [
            'Title',            # 0
            'Critic score',     # 1
            'User score',       # 2
            'Release date',     # 3
            'Metacritic link'   # 4
        ]
        self.games = pd.DataFrame(columns=self.columns)
        self.driver = None
        # pyinstaller --hidden-import matplotlib-venn -F Main.py
        if getattr(sys, 'frozen', False):
            self.driver = webdriver.Chrome(r'%s\chromedriver_win32\chromedriver.exe' % path.dirname(sys.executable),
                                           options=options)
        elif __file__:
            self.driver = webdriver.Chrome(r'%s\chromedriver_win32\chromedriver.exe' % str(path.dirname(path.realpath(__file__))),
                                           options=options)
        if start_page_url != '':
            self.go_to_url(start_page_url)
            print()

    def get_all_games_from_site(self) -> None:
        list_of_all_games_on_site = self.driver.find_elements_by_tag_name('a')
        for web_element in list_of_all_games_on_site:
            parent_element = web_element.find_element_by_xpath('..')
            if '/game/' in web_element.get_attribute("href") and (
                    len(web_element.text) > 1
                    ) and (
                    'basic_stat' in str(parent_element.get_attribute('class'))
                    ):
                grandparent_element = parent_element.find_element_by_xpath('..')
                temporary_results = []
                for all_info in grandparent_element.find_elements_by_tag_name('div'):
                    temporary_results.append(all_info.text)
                if 'tbd' not in str(temporary_results[3].splitlines()[0]):
                    self.games = self.games.append({
                        str(self.columns[0]): str(temporary_results[0]),
                        str(self.columns[1]): int(temporary_results[2]),
                        str(self.columns[2]): float(str(temporary_results[3].splitlines()[0])[6:]),
                        str(self.columns[3]): self.convert_to_date(temporary_results[3].splitlines()[len(temporary_results[3].splitlines()) - 1]),
                        str(self.columns[4]): str(web_element.get_attribute("href"))
                    }, ignore_index=True)
                else:
                    self.games = self.games.append({
                        str(self.columns[0]): str(temporary_results[0]),
                        str(self.columns[1]): int(temporary_results[2]),
                        str(self.columns[2]): float(0.0),
                        str(self.columns[3]): self.convert_to_date(temporary_results[3].splitlines()[len(temporary_results[3].splitlines()) - 1]),
                        str(self.columns[4]): str(web_element.get_attribute("href"))
                    }, ignore_index=True)

    def go_to_url(self, web_page_url: str) -> None:
        self.driver.get(web_page_url)
        self.driver.implicitly_wait(2)
        print('\tConnected to page: %s' % self.driver.title)

    def close_connection(self) -> None:
        self.driver.close()

    def get_pages_number(self) -> int:
        pages_objects = self.driver.find_element_by_class_name("pages")
        pages_objects = pages_objects.find_element_by_tag_name('ul')
        pages_object = pages_objects.find_element_by_class_name('last_page')
        pages_count = pages_object.text.splitlines()[-1:][0]
        return int(pages_count)

    def print_all_games(self) -> None:
        print(self.games)

    @staticmethod
    def convert_to_date(word: str) -> pd.Timestamp:
        day = int(word[word.index(',') - 2:word.index(',')])
        month = word[:word.index(',') - 2]
        if 'Jan' in month:
            month = 1
        elif 'Feb' in month:
            month = 2
        elif 'Mar' in month:
            month = 3
        elif 'Apr' in month:
            month = 4
        elif 'May' in month:
            month = 5
        elif 'Jun' in month:
            month = 6
        elif 'Jul' in month:
            month = 7
        elif 'Aug' in month:
            month = 8
        elif 'Sep' in month:
            month = 9
        elif 'Oct' in month:
            month = 10
        elif 'Nov' in month:
            month = 11
        elif 'Dec' in month:
            month = 12
        else:
            print('\n\t--- Wrong conversion of a month! Unknown month case! ---\n')
            month = 0
        year = int(word[word.index(',') + 1:])
        return pd.Timestamp(year, month, day)

    # example: https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0
    def find_all_games(self, the_page: str) -> None:
        if not self.debug:
            pages = self.get_pages_number()
            for page_number in range(pages):
                page = '%s%i' % (the_page[:-1], page_number)
                self.go_to_url(page)
                self.get_all_games_from_site()
        else:
            for page_number in range(1):
                page = '%s%i' % (the_page[:-1], page_number)
                self.go_to_url(page)
                self.get_all_games_from_site()
        print()
