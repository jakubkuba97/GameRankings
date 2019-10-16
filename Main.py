
"""
    Visualize given specific data frames in graphs
"""

from WebWorks import WebWorks
import pandas as pd


class Graphs:
    def __init__(self) -> None:
        self.columns = WebWorks().columns

    def above_80_in_all_days(self, df: pd.DataFrame) -> None:
        pass


if __name__ == '__main__':
    print()

    main_page = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0'
    browser = WebWorks(main_page)
    browser.debug = True
    browser.find_all_games(main_page)

    browser.close_connection()
