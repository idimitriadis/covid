import pandas as pd
import matplotlib.pyplot as plt

def merge_data():
    whr = pd.read_csv('data/2019.csv')
    covid = pd.read_excel('data/COVID-19-geographic-disbtribution-worldwide-2020-03-13.xls')
    whr = whr.rename(columns={"Country or region": "CountryExp"})
    # print (covid.shape)
    # print (whr.shape)
    df = pd.merge(covid,whr , on="CountryExp")
    df['DateRep'] = pd.to_datetime(df['DateRep'])
    # print (df.shape)
    return df

def get_total_cases(df):
    return df['NewConfCases'].sum()

def get_total_deaths(df):
    return df['NewDeaths'].sum()

def get_total_cases_per_day(df):
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_day(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country_per_day(df):
    df1 = df.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country_per_day(df):
    df1 = df.groupby(['DateRep', 'CountryExp'])['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country(df):
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country(df):
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

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

def get_cases_per_capita(df):
    df1 = df.groupby('GDP per capita')['NewConfCases'].sum().reset_index()
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
    df1 = df.groupby('Perceptions of corruption')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_freedom(df):
    df1 = df.groupby('Freedom to make life choices')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_rank(df):
    df1 = df.groupby('Overall rank')['NewConfCases'].sum().reset_index()
    return df1

