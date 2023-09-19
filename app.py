import streamlit as st 
import pandas as pd
import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df1 = pd.read_csv("athlete_events.csv")
df2 = pd.read_csv("noc_regions.csv")
df = preprocess.preprocess(df1,df2)

st.sidebar.title("Olympics data analysis")
user_menu = st.sidebar.radio("select an option",     
    ("Medal Tally","Overall analysis","Country Wise analysis","Athlete wise analysis")           
)
if(user_menu=="Medal Tally"):
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
  
    selected_year = st.sidebar.selectbox("select years",years)       
    selected_country = st.sidebar.selectbox("select country",country)

    if(selected_country=="overall" and selected_year=="overall"):
        st.title("Overall Medal Tally")
    elif(selected_country=="overall" and selected_year!="overall"):
        st.title("Medal Tally of {}".format(selected_year))
    elif(selected_country!="overall" and selected_year=="overall"):
        st.title("Medal Tally of {}".format(selected_country))
    else:
        st.title("Medal Tally of {} of year {}".format(selected_country,selected_year))
    medal_tally = helper.fetch_medal_country(selected_country,selected_year,df)
    st.table(medal_tally)

if(user_menu=="Overall analysis"):
    editions = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions") 
        st.title(editions)
    with col2:
        st.header("Cities") 
        st.title(cities)
    with col3:
        st.header("Sports") 
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events") 
        st.title(events)
    with col2:
        st.header("Athlete") 
        st.title(athletes)
    with col3:
        st.header("Nations") 
        st.title(nations)
    st.header("Participating Nations Over Year")
    nations_over_time=helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.header("Number of events per Year")
    events_over_time=helper.number_of_events_in_olympic(df)
    fig = px.line(events_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.header("Number of events per Year")
    athletes_over_time=helper.athletes_over_time(df)
    fig = px.line(athletes_over_time, x="Year", y="count")
    st.plotly_chart(fig)

    st.header("Number of events over time(every sports)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year","Sport","Event"])
    ax=sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0)) 
    st.pyplot(fig)

    st.header("Most Successfull athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"overall")
    
    selected_sport = st.selectbox("Select a sport",sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if(user_menu=="Country Wise analysis"):
    st.title("Country Wise analysis")
    st.sidebar.title("select country")
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox(options=country_list,label="Country")
    x=helper.year_wise_medal_tally(df,selected_country)
    
    st.header(selected_country +" year wise analysis")
    fig = px.line(x, x="Year", y="Medal")
    st.plotly_chart(fig)
    df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"],inplace=True)
    new_df = df[df["region"]==selected_country]

    st.header(selected_country +" excels in following part")
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(new_df.pivot_table(index="Sport",columns = "Year",values="Medal",aggfunc="count").fillna(0),annot=True)
    st.pyplot(fig)

    st.header("Top 10 athletes of "+selected_country)
    x=helper.most_successful_countrywise(df,selected_country)
    st.table(x)

if(user_menu=="Athlete wise analysis"):
    fig,ax=plt.subplots(figsize=(20,20))
    athlete_df = df.drop_duplicates(subset=["Name","region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    st.title("Athlete wise analysis")
    st.header("Age distribution of athletes")
    fig=ff.create_distplot([x1,x2,x3,x4],["Age_distribution","Gold Age_distribution","Silver Age_distribution","Bronze Age_distribution"],show_rug=False,show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.header("")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    # sport_list.insert(0,"overall")

    selected_sport = st.selectbox("select a sport ",sport_list)
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
