
"""
    Visualize given specific data frames in graphs
"""

from WebWorks import WebWorks
import pandas as pd


class Graphs:
    def __init__(self) -> None:
        self.columns = WebWorks().columns   # TODO: fix the thread stopping error - Timers cannot be stopped from another thread

    def above_80_in_all_days(self, df: pd.DataFrame, compare_to_all: bool = True) -> pd.DataFrame.plot:
        df['Greater than 80'] = df[self.columns[1]].apply(lambda x: 1 if x > 80 else 0)
        if compare_to_all:
            df['All'] = df[self.columns[1]].apply(lambda x: 1)
            df = df.groupby(self.columns[3], as_index=False).agg({'Greater than 80': 'sum', 'All': 'sum'})
        else:
            df = df.groupby(self.columns[3], as_index=False).agg({'Greater than 80': 'sum'})
        df = df.sort_values(by=self.columns[3], ascending=True)
        df[self.columns[3]] = df[self.columns[3]].apply(lambda x: str(x)[:10])

        ax = df.plot(kind='bar', x=self.columns[3], title='Games with critic scores of above 80 per days')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of games')    # TODO: reshape the graph so it shows x labels correctly
        return ax


if __name__ == '__main__':
    print()

    main_page = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0'
    browser = WebWorks(main_page)
    browser.debug = True
    browser.find_all_games(main_page)

    Graphs().above_80_in_all_days(browser.games)

    browser.close_connection()
