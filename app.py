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
        cols = 'A:Z'
    elif option == 'Passing':
        sheet = 'nfl_passing_formatted'
        cols = 'A:AC'
    elif option == 'Rushing':
        sheet = 'nfl_rushing_formatted'
        cols = 'A:Z'
    df = pd.read_excel(
    io="nfl_stats_fp.xlsx",
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
    data = [df.iloc[formatted_rank]['Rk'], df.iloc[formatted_rank]['Player'], df.iloc[formatted_rank]['Yds']]
    try:
        data.append(df.iloc[formatted_rank]['YdsRec'])
    except:
        data.append(df.iloc[formatted_rank]['YdsRush'])
    data.append(df.iloc[formatted_rank]['TD'])
    try:
        data.append(df.iloc[formatted_rank]['TDRec'])
    except:
        data.append(df.iloc[formatted_rank]['TDRush'])
    data.append(df.iloc[formatted_rank]['Y/G'])
    try:
        data.append(df.iloc[formatted_rank]['Y/R'])
    except:
        data.append(df.iloc[formatted_rank]['Y/A'])
    if choice == 'Rushing' or choice == 'Passing':
        data.append(df.iloc[formatted_rank]['Att'])
    else:
        data.append(df.iloc[formatted_rank]['Rec'])
    try:
        data.append(df.iloc[formatted_rank]['Int'])
        data.append(df.iloc[formatted_rank]['Fmb'])
    except:
        data.append(df.iloc[formatted_rank]['Fmb'])
    data.append(df.iloc[formatted_rank]['FPPG'])
    data.append(df.iloc[formatted_rank]['FP'])
    return data


#Helper function to create expanders
#Average
def averageExpanders(data, choice):
    #all_KPIs = avg_KPIs + choice_KPIs
    #avg_KPIs = [avg_yards_by_field, avg_td_by_field, avg_yPerG_by_field, avg_fppg_by_field, avg_fp_by_field]
    if choice == 'Passing' or 'Receiving':
        labelOtherYards = 'Rushing Yards'
        labelOtherTD = 'Rushing TD'
    else:
        labelOtherYards = 'Receiving Yards'
        labelOtherTD = 'Rushing TD'
    with st.expander(f"Average Metrics of Selected Players", expanded=True):
        if math.isnan(data[0]):
            data[:] = [0 for aa in data[:]]
        columns = [left_column, right_column, col, col2, col3, col4] = st.columns(6)
        with left_column:
            st.metric(label='Total FP', value=data[4])
        with right_column:
            st.metric(label='FPPG', value=data[3])
        columns = [farthestleft_column, left_column, midleft_column, col, middle_column, midright_column, right_column, farright_column, farthestright_column] = st.columns(9)
        with farthestleft_column:
            st.metric(label=f'{choice} Yards', value=data[0])
        with left_column:
            st.metric(label=labelOtherYards, value=data[7])
        with midleft_column:
            st.metric(label=f'{choice} TD', value=data[1])
        with col:
            st.metric(label=labelOtherTD, value=data[8])
        with middle_column:
            st.metric(label='Y/G', value=data[2])
        with midright_column:
            st.metric(label='Y/A', value=data[5])
        with right_column:
            if choice == 'Receiving':
                st.metric(label='Rec', value=data[6])
            else:
                st.metric(label='Att', value=data[6])
        if type(data) != list:
            with farright_column:
                if choice == 'Passing':
                    st.metric(label='Int', value=data[9][0])
                    with farthestright_column:
                        st.metric(label='Fmb', value=data[9][1])
                else:
                    st.metric(label='Fmb', value=data[9][0])

#Head-2-Head             
def head2headExpander(columns, values, values2, choice):
    att = 'Att'
    fmbOrInt = ['Fmb', '']
    color = 'normal'
    
    if choice == 'Rushing':
        otherChoice = 'Receiving'
    else:
        otherChoice = 'Rushing'
        if choice == 'Receiving':
            att = 'Rec'
        else:
            fmbOrInt = ['Int', 'Fmb']
            
    labels = [f'{choice} Yards', f'{otherChoice} Yards', f'{choice} TD', f'{otherChoice} TD', 'Y/G', 'Y/A', f'{att}', f'{fmbOrInt[0]}', f'{fmbOrInt[1]}']

    temp = values[:]
    temp2 = values2[:]
    for i in range(0,2): temp.pop(0)
    for i in range(0,2): temp2.pop(0)
    
    for i, v in enumerate(columns):
        if labels[i] == 'Int' or labels[i] == 'Fmb':
            color = 'inverse'
        with v:
            if type(temp[i]) == int:
                st.metric(label=labels[i], value=int(temp[i]), delta=round(temp[i]-temp2[i], 2), delta_color=color)
            else:
                st.metric(label=labels[i], value=float(temp[i]), delta=round(temp[i]-temp2[i], 2), delta_color=color)

#Helper to setup KPIs/Figs based on user choice
def choiceKPIFig(choice, df_selection):
    try:
        yPa = round(df_selection['Y/A'].mean(), 1)
        att = round(df_selection['Att'].mean(), 1)
    except:
        yPa = round(df_selection['Y/R'].mean(), 1)
        att = round(df_selection['Rec'].mean(), 1)
    try:
        otherYds = round(df_selection['YdsRush'].mean(), 1)
        otherTD = round(df_selection['TDRush'].mean(), 1)
    except:
        otherYds = round(df_selection['YdsRec'].mean(), 1)
        otherTD = round(df_selection['TDRec'].mean(), 1)
    try:
        fmbInt = [round(df_selection['Fmb'].mean(), 1) ,round(df_selection['Int'].mean(), 1)]
    except:
        fmbInt = [round(df_selection['Fmb'].mean(), 1)]
    if choice == 'Passing':
        tgt_atmps = setFig('Att', "<b>Passing Attempts by Player</b>")
        recp_rave_comp = setFig('Cmp', "<b>Completions by Player</b>")
        td = setFig('TD', "<b>Passing TD by Player</b>")
    elif choice == 'Receiving':
        tgt_atmps = setFig('Tgt', "<b>Recieving Targets by Player</b>")
        recp_rave_comp = setFig('Rec', "<b>Receptions by Player</b>")
        td = setFig('TD', "<b>Receiving TD by Player</b>")
    else:
        tgt_atmps = setFig('Att', "<b>Rushing Attempts by Player</b>")
        recp_rave_comp = setFig('Y/A', "<b>Yards per Attempt by Player</b>")
        td = setFig('TD', "<b>Rushing TD by Player</b>")
    return [yPa, att, otherYds, otherTD, fmbInt], [tgt_atmps, recp_rave_comp, td]
    
########## END HELPER FUNCTIONS ##########
                
########## SIDEBAR AND DF ##########
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
avg_fppg_by_field = round(df_selection['FPPG'].mean(), 1)
avg_fp_by_field = round(df_selection['FP'].mean(), 1)
avg_KPIs = [avg_yards_by_field, avg_td_by_field, avg_yPerG_by_field, avg_fppg_by_field, avg_fp_by_field]
# ----- FIGS/KPIs ----- #
choice_KPIs, choice_figs = choiceKPIFig(choice, df_selection)
yardsData = setFig('Yds', "<b>Yards by Player</b>")
all_KPIs = avg_KPIs + choice_KPIs

########## END KPI's ##########
    
########## CONTENT ##########
#Setup data for expanders
data = setupDetailed(df, formatted_rank, choice)
data2 = setupDetailed(df, formatted_rank2, choice)

#Create 1st and 2nd H2H expanders
with st.expander(f"Detailed {choice} of {data[1]} against {data2[1]}", expanded=True):
    st.write(f"Rank: {int(data[0])}")
    
    columns = [col1, col2, col3, col4, col5, col6] = st.columns(6)
    with col1:
        st.metric(label='Total FP', value=data[11], delta=round(data[11]-data2[11], 2))
    with col2:
        st.metric(label='FPPG', value=data[10], delta=round(data[10]-data2[10], 2))
    if choice == 'Passing':
        columns = [col1, col2, col3, col4, col5, col6, col7, col8, col9] = st.columns(9)
    else:
        columns = [col1, col2, col3, col4, col5, col6, col7, col8] = st.columns(8)
    head2headExpander(columns, data, data2, choice)
    
with st.expander(f"Detailed {choice} of {data2[1]} against {data[1]}", expanded=True):
    st.write(f"Rank: {int(data2[0])}")
    
    columns = [col1, col2, col3, col4, col5, col6] = st.columns(6)
    with col1:
        st.metric(label='Total FP', value=data2[11], delta=round(data2[11]-data[11], 2))
    with col2:
        st.metric(label='FPPG', value=data2[10], delta=round(data2[10]-data[10], 2))
    if choice == 'Passing':
        columns = [col1, col2, col3, col4, col5, col6, col7, col8, col9] = st.columns(9)
    else:
        columns = [col1, col2, col3, col4, col5, col6, col7, col8] = st.columns(8)
    head2headExpander(columns, data2, data, choice)

#Create average expanders        
averageExpanders(all_KPIs, choice)


################ Clean up averageExpanders, and possibly above h2h. Try to make the expander
#into reusable code?


#Top graphs
columns = [left_column, right_column] = st.columns(2)
data = [yardsData, choice_figs[2]]
plotFig(columns, data)

st.markdown("---")

#Bottom graphs
columns = [leftbot_column, rightbot_column] = st.columns(2)
data = [choice_figs[1], choice_figs[0]]
plotFig(columns, data)




