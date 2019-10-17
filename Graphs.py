
"""
    Visualize given specific data frames in graphs
"""

from WebWorks import WebWorks
import pandas as pd
import matplotlib.pyplot as plt


class Graphs:
    def __init__(self) -> None:
        self.columns = WebWorks().columns

    def above_80_in_all_days(self, df: pd.DataFrame, compare_to_all: bool = True, show_as_image: bool = True) -> pd.DataFrame.plot:
        df['Greater than 80'] = df[self.columns[1]].apply(lambda x: 1 if x > 80 else 0)
        if compare_to_all:
            df['All'] = df[self.columns[1]].apply(lambda x: 1)
            df = df.groupby(self.columns[3], as_index=False).agg({'Greater than 80': 'sum', 'All': 'sum'})
        else:
            df = df.groupby(self.columns[3], as_index=False).agg({'Greater than 80': 'sum'})
        df = df.sort_values(by=self.columns[3], ascending=True)
        df[self.columns[3]] = df[self.columns[3]].apply(lambda x: str(x)[:10])

        _, ax = plt.subplots()
        if compare_to_all:
            ax = df.plot(kind='bar', x=self.columns[3], ax=ax,
                         y='All', width=0.85, color='red')
        ax = df.plot(kind='bar', x=self.columns[3], ax=ax, title='Games with critic scores of above 80 per days',
                     y='Greater than 80', width=0.85, color=('green' if compare_to_all else 'orange'))
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of games')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=50, horizontalalignment='right')
        ax.tick_params(axis="x", labelsize=7.5)

        if show_as_image:
            print('Drawing a graph...')
            plt.show()
        return ax
