import numpy as np
def medal_tally(df):
    df = df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    df = df.groupby("region").sum()[["Silver","Gold","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    df["Total"] = df["Silver"] + df["Bronze"] + df["Gold"]
    df["Silver"] = df["Silver"].astype("int")
    df["Gold"] = df["Gold"].astype("int")
    df["Bronze"] = df["Bronze"].astype("int")
    return df    

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,"overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,"overall")

    return years, country

def fetch_medal_country(country,year,df):
    flag =0
    df = df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    if(year=="overall" and country=="overall"):
        temp_df = df
    elif(year=="overall" and country!="overall"):
        temp_df = df[df["region"]==country]
        flag=1
    elif(year!="overall" and country=="overall"):
        temp_df = df[df["Year"]==int(year)]
    else:
        temp_df = df[(df["Year"]==int(year)) & (df["region"]==country)]
    if(flag==1):
        x=temp_df.groupby("Year").sum()[["Silver","Gold","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    else:
        x=temp_df.groupby("region").sum()[["Silver","Gold","Bronze"]].sort_values("Gold",ascending=False).reset_index()

    x["Total"] = x["Silver"] + x["Bronze"] + x["Gold"]
    return x

def participating_nations_over_time(df):
    nations_over_time=df.drop_duplicates(["Year","region"])["Year"].value_counts().reset_index().sort_values("Year")
    return nations_over_time

def number_of_events_in_olympic(df):
    events_over_time=df.drop_duplicates(["Year","Event"])["Year"].value_counts().reset_index().sort_values("Year")
    return events_over_time

def athletes_over_time(df):
    athletes_over_time=df.drop_duplicates(["Year","Name"])["Year"].value_counts().reset_index().sort_values("Year")
    return athletes_over_time  

def most_successful(df,sport):
    temp_df = df.dropna(subset=["Medal"])
    if sport!="overall":
        temp_df = temp_df[temp_df["Sport"]==sport]
    return temp_df["Name"].value_counts().reset_index().merge(df,on="Name",how="left")[["Name","Sport","Age","region"]].drop_duplicates("Name")

def year_wise_medal_tally(df,country):
    df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"],inplace=True)
    new_df = df[df["region"]==country]
    new_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return new_df
    
def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"]==country]
    x = temp_df["Name"].value_counts().reset_index().merge(df,on="Name",how="left")[["Name","Sport","Age"]].drop_duplicates("Name")
    return x.iloc[:10,:]

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final