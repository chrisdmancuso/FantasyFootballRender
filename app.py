import pandas as pd
import plotly.express as px
import streamlit as st
import math
import warnings
warnings.filterwarnings('ignore')

# ----- Initial Page Setup ----- #
st.set_page_config(page_title="NFL Stats Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)


########## HELPER FUNCTIONS ##########
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
    for i, c in enumerate(columns):
        try:
            data[i].update_yaxes(automargin=True, dtick=1)
            c.plotly_chart(data[i], use_container_width=True)
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

#Helper function to setup detailed df
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
    data.append(df.iloc[formatted_rank]['G'])
    return data


#Helper function to create expanders
#Average
def averageExpanders(data, yards, td, yg, ya, att, fmb, choice):
    with st.expander(f"Average Metrics of Selected Players", expanded=True):
        if math.isnan(yards):
            yards = td = yg = ya = att = fmb = 0
        columns = [left_column, midleft_column, middle_column, midright_column, right_column, farright_column] = st.columns(6)
        with left_column:
            st.metric(label='Yards', value=yards)
        with midleft_column:
            st.metric(label='TD', value=td)
        with middle_column:
            st.metric(label='Y/G', value=yg)
        with midright_column:
            st.metric(label='Y/A', value=ya)
        with right_column:
            if choice == 'Receiving':
                st.metric(label='Rec', value=att)
            else:
                st.metric(label='Att', value=att)
        with farright_column:
            if choice == 'Passing':
                st.metric(label='Int', value=fmb)
            else:
                st.metric(label='Fmb', value=fmb)

#Head-2-Head             
def head2HeadExpanders(data, opp, yards, td, yg, ya, att, fmb, games, choice):
    labelVal = f"Detailed {choice} Stats of {data[1]} compared to {opp}"
    with st.expander(labelVal, expanded=True):
        st.write(f"Rank: {int(data[0])}")
        if choice == 'Passing':
            fppg = round((.04 * (data[4])) + (4 * (data[3]/data[8])) - ((data[7]/data[8])), 2)
            oppFppg = round((.04 * (yards/games)) + (4 * (td/games)) - ((fmb/games)), 2)
        else:
            fppg = round((.1 * (data[4])) + (6 * (data[3]/data[8])) - (2 *(data[7]/data[8])), 2)
            oppFppg = round((.1 * (yards/games)) + (6 * (td/games)) - (2 *(fmb/games)), 2)
        # Add average fantasy points per game to h2hexpander. Something like (yards/games * .1 or .25) + (td/games * 6 or 4 ) - (fmb/games * 2) - (ints/games)
        st.metric(label='FPPG', value=fppg, delta=round(fppg-oppFppg, 2))
        columns = [left_column, midleft_column, middle_column, midright_column, right_column, farright_column] = st.columns(6)
        with left_column:
            st.metric(label='Yards', value=int(data[2]), delta=int(data[2]-yards))
        with midleft_column:
            st.metric(label='TD', value=int(data[3]), delta=int(data[3]-td))
        with middle_column:
            st.metric(label='Y/G', value=data[4], delta=round(data[4]-yg, 2))
        with midright_column:
            st.metric(label='Y/A', value=data[5], delta=round(data[5]-ya, 2))
        with right_column:
            if choice == 'Receiving':
                st.metric(label='Rec', value=int(data[6]), delta=int(data[6]-att))
            else:
                st.metric(label='Att', value=int(data[6]), delta=int(data[6]-att))
        with farright_column:
            if choice == 'Passing':
                st.metric(label='Int', value=int(data[7]), delta=int(data[7]-fmb), delta_color="inverse")
            else:
                st.metric(label='Fmb', value=int(data[7]), delta=int(data[7]-fmb), delta_color="inverse")
                
########## END HELPER FUNCTIONS ##########
                
########## SIDEBAR ##########
choice, rank, rank2, formatted_rank, formatted_rank2 = setupSidebar()
df = setDF(choice)

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
########## END SIDEBAR ##########

########## KPI's ##########
# ----- Averages ----- #
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
    
# ----- YARDS ----- #
yardsData = setFig('Yds', "<b>Yards by Player</b>")

# ----- TARGETS/ATTEMPTS/COMPLETIONS/TD ----- #
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
    recp_rave_comp = setFig('Y/A', "<b>Yards per Attempt by Player</b>")
    td = setFig('TD', "<b>Rushing TD by Player</b>")

########## END KPI's ##########
    
########## CONTENT ##########
#Setup data for expanders
data = setupDetailed(df, formatted_rank, choice)
data2 = setupDetailed(df, formatted_rank2, choice)

#Create 1st and 2nd H2H expanders
head2HeadExpanders(data, data2[1], data2[2], data2[3], data2[4], data2[5], data2[6], data2[7], data[8], choice)
head2HeadExpanders(data2, data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], choice)

#Create average expanders        
averageExpanders(data2, avg_yards_by_field, avg_td_by_field, avg_yPerG_by_field, avg_yPerA_by_field, avg_atts_by_field, avg_fmbInt_by_field, choice)

#Top graphs
columns = [left_column, right_column] = st.columns(2)
data = [yardsData, td]
plotFig(columns, data)

st.markdown("---")

#Bottom graphs
columns = [leftbot_column, rightbot_column] = st.columns(2)
data = [recp_rave_comp, tgt_atmps]
plotFig(columns, data)



