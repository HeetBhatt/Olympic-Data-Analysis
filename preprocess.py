import pandas as pd



def preprocess(df1,df2):
    df = df1[df1["Season"]=="Summer"]
    df =df.merge(df2,on="NOC",how="left")
    df.drop_duplicates(inplace=True)
    df = pd.concat([df,pd.get_dummies(df["Medal"])],axis=1)
    return df