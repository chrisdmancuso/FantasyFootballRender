import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="NFL Stats Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

#Helper function to create dataframe data for each sheet
def setDF(option):
    sheet = ''
    skip = 0
    if option == 'Receiving':
        sheet = 'nfl_receiving_formatted'
        cols = 'A:S'
    elif option == 'Passing':
        sheet = 'nfl_passing_formatted'
        cols = 'A:U'
    elif option == 'Rushing':
        sheet = 'nfl_rushing_formatted'
        cols = 'A:O'
        skip = 1
    df = pd.read_excel(
    io="nfl_stats.xlsx",
    engine="openpyxl",
    sheet_name=sheet,
    skiprows=skip,
    usecols=cols,
    nrows=50
    )
    return df

#Helper function to create figures
def setFig(category, html):
    data = (df_selection.groupby(by=['Player']).sum()[category]).sort_values(ascending=True)
    
    fig = px.bar(data,
                 x=category,
                 y=data.index,orientation="h",
                 title=html,
                 color_discrete_sequence=["#631284"] * len(data),
                 template="plotly_white",
                 height=800,
                 )

    fig.update_layout(
        autosize=False,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=True))
    )
    return fig

#Helper function to plot figures
def plotFig(columns, data):
    count = 0
    for c in columns:
        try:
            data[count].update_yaxes(automargin=True, dtick=1)
            c.plotly_chart(data[count], use_container_width=True)
            count+=1
        except:
            print("OH GEEZ")

#Helper function to setup sidebar
def setupSidebar():
    choice = st.sidebar.selectbox(
    "Choose a Stat:",
    ['Receiving', 'Passing', 'Rushing' ]
    )

    rank = st.sidebar.number_input(
    "Choose Rank to Display Detailed Stats:",
    min_value=1,
    max_value=50,
    step=1
    )
    return choice, rank, rank - 1

# ----- Setup sidebar components and DataFrame -----
radioGroup = st.sidebar.radio(
    "Choose view:",
    ['Top 50', 'H2H'],
    horizontal=True,
    )

def setupDetailed(df, formatted_rank, choice):
    data = [df.iloc[formatted_rank]['Rk'], df.iloc[formatted_rank]['Player'], df.iloc[formatted_rank]['Yds'], df.iloc[formatted_rank]['TD'], df.iloc[formatted_rank]['Y/G']]
    if choice == 'Rushing':
        data.append(df.iloc[formatted_rank]['Y/A'])
        data.append(df.iloc[formatted_rank]['Att'])
        data.append(df.iloc[formatted_rank]['Fmb'])
    elif choice == 'Passing':
        data.append(df.iloc[formatted_rank]['Y/A'])
        data.append(df.iloc[formatted_rank]['Att'])
        data.append(df.iloc[formatted_rank]['Int'])
    else:
        data.append(df.iloc[formatted_rank]['Y/R'])
        data.append(df.iloc[formatted_rank]['Rec'])
        data.append(df.iloc[formatted_rank]['Fmb'])
    return data
    
choice, rank, formatted_rank = setupSidebar()
print(formatted_rank)
# 2 Things, 1st, possibly use radio button to move between 2 different views, such as top 50 and h2h and maybe detailed?
# 2nd, possbily use the following code to access a specific player and display that at all times at top of page?
# Possibly replace the detailed option on the radio button? Use textinput or number input?
# df.iloc[number] grabs the object at that position which should correlate with that players rank + 1.
# example: df.iloc[0] on rushing gives Jonathon Taylor.
df = setDF(choice)
print(df.iloc[formatted_rank])
players = st.sidebar.multiselect(
    "Select Players to compare:",
    options=df['Player'].unique(),
    default=df['Player'].unique()
    )

pos = st.sidebar.multiselect(
    "Select Position(s):",
    options=df["Pos"].unique(),
    default=df["Pos"].unique()
    )

df_selection = df.query(
    "Player == @players & Pos == @pos"
    )

# ----- DETAILED -----


# ----- KPI's -----
avg_yards_by_field = round(df_selection['Yds'].mean(), 1)
avg_td_by_field = round(df_selection['TD'].mean(), 1)
avg_yPerG_by_field = round(df_selection['Y/G'].mean(), 1)

# ----- YARDS -----
yardsData = setFig('Yds', "<b>Yards by Player</b>")

# ----- TARGETS/ATTEMPTS/COMPLETIONS/TD -----
if choice == 'Receiving':
    tgt_atmps = setFig('Tgt', "<b>Recieving Targets by Player</b>")
    recp_rave_comp = setFig('Rec', "<b>Receptions by Player</b>")
    td = setFig('TD', "<b>Receiving TD by Player</b>")
elif choice == 'Passing':
    tgt_atmps = setFig('Att', "<b>Passing Attempts by Player</b>")
    recp_rave_comp = setFig('Cmp', "<b>Completions by Player</b>")
    td = setFig('TD', "<b>Passing TD by Player</b>")
else:
    tgt_atmps = setFig('Att', "<b>Rushing Attempts by Player</b>")
    recp_rave_comp = setFig('Y/A', "<b>Yards Average per Attempt by Player</b>")
    td = setFig('TD', "<b>Rushing TD by Player</b>")
# ----- CONTENT -----
# Top Detailed/Top graphs
columns = [farleft_column, left_column, midleft_column, middle_column, midright_column, right_column, farright_column, farthestright_column] = st.columns(8)
data = setupDetailed(df, formatted_rank, choice)
with farleft_column:
    st.subheader("Rank:")
    st.subheader(f'{int(data[0])}')
with left_column:
    st.subheader("Player:")
    st.subheader(f'{data[1]}')
with midleft_column:
    st.subheader("Yards:")
    st.subheader(f'{data[2]}')
with middle_column:
    st.subheader("TD:")
    st.subheader(f'{int(data[3])}')
with midright_column:
    st.subheader("Y/G:")
    st.subheader(f'{data[4]}')
with right_column:
    st.subheader("Y/A:")
    st.subheader(f'{data[5]}')
with farright_column:
    st.subheader("Att:")
    st.subheader(f'{data[6]}')
with farthestright_column:
    st.subheader("Fmb:")
    st.subheader(f'{int(data[7])}')
st.markdown("---")
columns = [left_column, middle_column, right_column] = st.columns(3)
with left_column:
    st.subheader("Average Yards of Selected:")
    st.subheader(f'{avg_yards_by_field}')
with middle_column:
    st.subheader("Average TD of Selected:")
    st.subheader(f'{avg_td_by_field}')
with right_column:
    st.subheader("Average Yards per Game of Selected")
    st.subheader(f'{avg_yPerG_by_field}')
st.markdown("---")

columns = [left_column, right_column] = st.columns(2)
data = [yardsData, td]

plotFig(columns, data)

st.markdown("---")

#Bottom graphs
columns = [leftbot_column, rightbot_column] = st.columns(2)
data = [recp_rave_comp, tgt_atmps]

plotFig(columns, data)



