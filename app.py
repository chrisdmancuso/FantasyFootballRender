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
                 color_discrete_sequence=["#FF4B4B"] * len(data),
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
            print("ERROR")

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

    rank2 = st.sidebar.number_input(
    "Choose Rank to Display Detailed Stats:",
    min_value=2,
    max_value=50,
    step=1,
    key=1
    )
    return choice, rank, rank2, rank - 1, rank2 - 1

# ----- Setup sidebar components and DataFrame -----

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
    
choice, rank, rank2, formatted_rank, formatted_rank2 = setupSidebar()
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
if choice == 'Receiving':
    avg_yPerA_by_field = round(df_selection['Y/R'].mean(), 1)
    avg_atts_by_field = round(df_selection['Rec'].mean(), 1)
else:
    avg_yPerA_by_field = round(df_selection['Y/A'].mean(), 1)
    avg_atts_by_field = round(df_selection['Att'].mean(), 1)
if choice == 'Passing':
    avg_fmbInt_by_field = round(df_selection['Int'].mean(), 1)
else:
    avg_fmbInt_by_field = round(df_selection['Fmb'].mean(), 1)
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
data = setupDetailed(df, formatted_rank, choice)
data2 = setupDetailed(df, formatted_rank2, choice)
columns = [left_column, right_column] = st.columns(2)
with left_column:
    st.subheader(f"Rank:  {int(data[0])}")
with right_column:
    st.subheader(f"Player:  {data[1]}")
    
columns = [left_column, midleft_column, middle_column, midright_column, right_column, farright_column] = st.columns(6)
with left_column:
    st.metric(label='Yards', value=int(data[2]), delta=round(data[2]-avg_yards_by_field, 2))
with midleft_column:
    st.metric(label='TD', value=int(data[3]), delta=round(data[3]-avg_td_by_field, 2))
with middle_column:
    st.metric(label='Y/G', value=data[4], delta=round(data[4]-avg_yPerG_by_field, 2))
with midright_column:
    st.metric(label='Y/A', value=data[5], delta=round(data[5]-avg_yPerA_by_field, 2))
with right_column:
    if choice == 'Receiving':
        st.metric(label='Rec', value=data[6], delta=round(data[6]-avg_atts_by_field, 2))
    else:
        st.metric(label='Att', value=data[6], delta=round(data[6]-avg_atts_by_field, 2))
with farright_column:
    if choice == 'Passing':
        st.metric(label='Int', value=data[7], delta=round(data[7]-avg_fmbInt_by_field, 2))
    else:
        st.metric(label='Fmb', value=data[7], delta=round(data[7]-avg_fmbInt_by_field, 2))
        
st.markdown("---")

columns = [left_column, right_column] = st.columns(2)
with left_column:
    st.subheader(f"Rank:  {int(data2[0])}")
with right_column:
    st.subheader(f"Player:  {data2[1]}")
    
columns = [left_column, midleft_column, middle_column, midright_column, right_column, farright_column] = st.columns(6)
with left_column:
    st.metric(label='Yards', value=int(data2[2]), delta=round(data2[2]-avg_yards_by_field, 2))
with midleft_column:
    st.metric(label='TD', value=int(data2[3]), delta=round(data2[3]-avg_td_by_field, 2))
with middle_column:
    st.metric(label='Y/G', value=data2[4], delta=round(data2[4]-avg_yPerG_by_field, 2))
with midright_column:
    st.metric(label='Y/A', value=data2[5], delta=round(data2[5]-avg_yPerA_by_field, 2))
with right_column:
    if choice == 'Receiving':
        st.metric(label='Rec', value=data2[6], delta=round(data2[6]-avg_atts_by_field, 2))
    else:
        st.metric(label='Att', value=data2[6], delta=round(data2[6]-avg_atts_by_field, 2))
with farright_column:
    if choice == 'Passing':
        st.metric(label='Int', value=data2[7], delta=round(data2[7]-avg_fmbInt_by_field, 2))
    else:
        st.metric(label='Fmb', value=data2[7], delta=round(data2[7]-avg_fmbInt_by_field, 2))
        
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



