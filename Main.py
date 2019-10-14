
"""
    Search the metacritic site for all wanted games
    TODO: Save immediately as a dataframe - saving space and time
"""

from selenium import webdriver


class WebWorks:
    def __init__(self, start_page_url: str = '') -> None:
        from os import path
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.games = []
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
                    self.games.append([
                        temporary_results[0],
                        temporary_results[2],
                        float(str(temporary_results[3].splitlines()[0])[6:]),
                        temporary_results[3].splitlines()[1],
                        str(web_element.get_attribute("href"))
                    ])
                else:
                    self.games.append([
                        temporary_results[0],
                        temporary_results[2],
                        float(0.0),
                        temporary_results[3].splitlines()[1],
                        str(web_element.get_attribute("href"))
                    ])

    def go_to_url(self, web_page_url: str) -> None:
        self.driver.get(web_page_url)
        self.driver.implicitly_wait(2)
        print('Connected to page: %s' % self.driver.title)

    def close_connection(self) -> None:
        self.driver.close()

    def get_pages_number(self) -> int:
        pages_objects = self.driver.find_element_by_class_name("pages")
        pages_objects = pages_objects.find_element_by_tag_name('ul')
        pages_object = pages_objects.find_element_by_class_name('last_page')
        pages_count = pages_object.text.splitlines()[-1:][0]
        return int(pages_count)

    def print_all_games(self) -> None:
        print('\n' + ('-' * 50))
        for index, game in enumerate(self.games):
            print('%i %s' % (index + 1, game))
            print('-' * 50)

    # example: https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0
    def find_all_games(self, the_page: str) -> None:
        pages = self.get_pages_number()
        for page_number in range(pages):
            page = '%s%i' % (the_page[:-1], page_number)
            self.go_to_url(page)
            self.get_all_games_from_site()


if __name__ == '__main__':
    print()

    main_page = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0'
    browser = WebWorks(main_page)
    browser.find_all_games(main_page)
    browser.print_all_games()

    browser.close_connection()
