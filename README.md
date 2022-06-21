# Fantasy Football Stats - Heroku App
### An interactive dashboard created using Streamlit, Pandas, and Plotly. Hosted by Heroku.

This project utilized Google Sheets to clean up and format csv data from [Pro Football Reference](https://www.pro-football-reference.com/) into [xlsx format](nfl_stats_fp.xlsx), which was then read into Python as a [Pandas](https://pandas.pydata.org/) Dataframe using the [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) engine. [Streamlit](https://streamlit.io/) was then used to handle state changes based on user input, and display the corresponding Pandas data and [Plotly](https://plotly.com/python/) graphs.

Explore the site [here](https://statsfantasyfootball.herokuapp.com/)

(As a free [Heroku](https://www.heroku.com/home) app, the app will enter a sleep state after 30 minutes when not in use. It will take some time to spin up on initiation and may appear like it's unresponsive, but it will load.)
#
![herokuStats](https://user-images.githubusercontent.com/31321037/174680455-7148fc91-ee08-4eee-ad20-df5af934033f.png)
