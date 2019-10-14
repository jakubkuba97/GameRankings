
"""
    Main
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class WebWorks:
    def __init__(self, start_page_url: str = '') -> None:
        from os import path
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.driver = webdriver.Chrome(r'%s\chromedriver_win32\chromedriver.exe' % str(path.dirname(path.realpath(__file__))),
                                       options=options)
        if start_page_url != '':
            self.go_to_url(start_page_url)

    def go_to_url(self, web_page_url: str) -> None:
        self.driver.get(web_page_url)
        print(self.driver.title)

    def close_connection(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    print()
    main_page_number = 0
    main_page = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=%i' % main_page_number
    browser = WebWorks(main_page)

    browser.close_connection()
