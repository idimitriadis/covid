import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def merge_data():
    covid = pd.read_excel('data/COVID-19-geographic-disbtribution-worldwide-2020-03-13.xls')
    covid['CountryExp'] = covid['CountryExp'].apply(lambda x: x.upper())
    covid_countries = set(covid['CountryExp'].tolist())
    whr2019 = pd.read_csv('data/world-happiness-report-2019.csv')
    whr2019 = whr2019.rename(columns={"Country (region)": "CountryExp","Log of GDP\nper capita":"Log of GDP per capita","Healthy life\nexpectancy":"Healthy life expectancy"})
    whr2019['CountryExp'] = whr2019['CountryExp'].apply(lambda x: x.upper())
    whr_countries = set(whr2019['CountryExp'].tolist())
    # print (covid_countries-whr_countries)
    # print (whr2019.columns)
    human_freedom = pd.read_csv('data/human_freedom.csv')
    human_freedom = human_freedom.filter(['countries', 'hf_score'])
    econ_freedom = pd.read_csv('data/economic_freedom.csv')
    econ_freedom = econ_freedom.filter(['countries','ECONOMIC FREEDOM'])
    freedoms = pd.merge(econ_freedom,human_freedom,on="countries")
    freedoms = freedoms.rename(columns={'countries':'CountryExp'})
    freedoms['CountryExp'] = freedoms['CountryExp'].apply(lambda x: x.upper())
    # print (freedoms.shape)
    # print (covid.shape)
    # print (whr.shape)
    df = pd.merge(covid,whr2019 , on="CountryExp")
    # df['DateRep'] = pd.to_datetime(df['DateRep'])
    df_final = pd.merge(df,freedoms,on="CountryExp",how='outer')
    df_final = df_final.filter(['DateRep','CountryExp','NewConfCases','NewDeaths','ECONOMIC FREEDOM','hf_score','Log of GDP per capita','Healthy life expectancy',
        'Corruption','Freedom','Positive affect','Negative_affect','Social support','Ladder','Generosity'])
    # print (df.shape)
    return df_final


def get_dates(df):
    df = df[pd.notnull(df['DateRep'])]
    df['DateRep']=df['DateRep'].astype(str)
    df = df.sort_values(by='DateRep', ascending=False)
    dates = df['DateRep']
    return {'first': datetime.strptime(dates.iloc[-1], '%Y-%m-%d').strftime('%d-%m-%Y'), 'last': datetime.strptime(dates.iloc[0], '%Y-%m-%d').strftime('%d-%m-%Y')}

def get_total_cases(df):#
    return df['NewConfCases'].sum()

def get_total_deaths(df):#
    return df['NewDeaths'].sum()

def get_total_cases_per_day(df):#
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_day(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country_per_day(df):#
    df1 = df.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country_per_day(df):#
    df1 = df.groupby(['DateRep', 'CountryExp'])['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country(df):
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_hf(df):
    df1 = df.groupby(['CountryExp','hf_score','ECONOMIC FREEDOM'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country(df):
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_cases_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df2

def get_deaths_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewDeaths'].sum().reset_index()
    return df2

def get_total_distribution_of_cases(df):
    dfa = get_total_cases_per_country(df)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_cases_per_specific_country(df,country):
    dfa = get_cases_per_specific_country(df,country)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths(df):
    dfa = get_total_deaths_per_country(df)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths_per_specific_country(df,country):
    dfa = get_deaths_per_specific_country(df,country)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_cases_per_capita(df):
    df1 = df.groupby('Log of GDP per capita')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_life_expectancy(df):
    df1 = df.groupby('Healthy life expectancy')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_generosity(df):
    df1 = df.groupby('Generosity')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_social_support(df):
    df1 = df.groupby('Social support')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_corruption(df):
    df1 = df.groupby('Corruption')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_freedom(df):
    df1 = df.groupby('Freedom')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_human_freedom(df):
    # print (df['hf_score'],df['NewConfCases'])
    df['NewConfCases']+=1
    # df['NewConfCases']=df['NewConfCases'].apply(np.log10)
    df1 = df.groupby('hf_score')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_economic_freedom(df):
    df1 = df.groupby('ECONOMIC FREEDOM')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_rank(df):
    df1 = df.groupby('Ladder')['NewConfCases'].sum().reset_index()
    return df1

def get_countries_per_capita(df):
    df = df.dropna()
    df = df[df['Log of GDP per capita']>-1]
    df1 = df.groupby('CountryExp')['Log of GDP per capita'].mean().to_frame('capita').reset_index()
    return df1

df = merge_data()
print (get_total_cases_per_country_hf(df))
# print (get_cases_per_human_freedom(df))
# # print ( get_cases_per_human_freedom(df))
# print (get_total_distribution_of_cases_per_specific_country(df,'GREECE'))
# get_countries_per_capita(df)