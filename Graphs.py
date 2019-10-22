
"""
    Visualize given specific data frames in graphs
"""

from WebWorks import WebWorks
import pandas as pd
import matplotlib.pyplot as plt


class Graphs:
    def __init__(self) -> None:
        self.columns = WebWorks().columns

    def critic_score_pie_chart(self, df: pd.DataFrame, show_as_image: bool = True) -> pd.DataFrame.plot:
        results = pd.DataFrame(columns=['90-100', '80-89', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '0-9', 'No.', 'All'])
        results['90-100'] = df[self.columns[1]].apply(lambda x: 1 if x >= 90 else 0)
        results['80-89'] = df[self.columns[1]].apply(lambda x: 1 if 80 <= x < 90 else 0)
        results['70-79'] = df[self.columns[1]].apply(lambda x: 1 if 70 <= x < 80 else 0)
        results['60-69'] = df[self.columns[1]].apply(lambda x: 1 if 60 <= x < 70 else 0)
        results['50-59'] = df[self.columns[1]].apply(lambda x: 1 if 50 <= x < 60 else 0)
        results['40-49'] = df[self.columns[1]].apply(lambda x: 1 if 40 <= x < 50 else 0)
        results['30-39'] = df[self.columns[1]].apply(lambda x: 1 if 30 <= x < 40 else 0)
        results['20-29'] = df[self.columns[1]].apply(lambda x: 1 if 20 <= x < 30 else 0)
        results['10-19'] = df[self.columns[1]].apply(lambda x: 1 if 10 <= x < 20 else 0)
        results['0-9'] = df[self.columns[1]].apply(lambda x: 1 if x < 10 else 0)
        results['No.'] = df[self.columns[1]].apply(lambda x: 0)
        results['All'] = df[self.columns[1]].apply(lambda x: 1)
        results = results.groupby('No.').agg({'90-100': 'sum', '80-89': 'sum', '70-79': 'sum', '60-69': 'sum', '50-59': 'sum',
                                              '40-49': 'sum', '30-39': 'sum', '20-29': 'sum', '10-19': 'sum', '0-9': 'sum', 'All': 'count'})

        # TODO: fix this graph
        ax = plt.pie(
            results.iloc[0, :10],
            labels=['90-100', '80-89', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '0-9'],
            autopct='%1.1f%%'
        )

        if show_as_image:
            print('Drawing a graph...')
            plt.show()
        return ax

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
