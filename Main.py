
"""
    Main
"""

from WebWorks import WebWorks
from Graphs import Graphs


if __name__ == '__main__':
    print()

    main_page = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?page=0'
    browser = WebWorks(main_page)
    browser.debug = True
    browser.find_all_games(main_page)

    Graphs().critic_score_pie_chart(browser.games)

    browser.close_connection()
